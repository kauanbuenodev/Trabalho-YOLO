"""Converte os três relatórios Markdown em HTML imprimível com figuras."""
from __future__ import annotations

import html
import re
from pathlib import Path

PROJECTS = [
    Path("Atividade_Pratica_YOLO_Windows"),
    Path("Atividade_Pratica_II_YOLO_Kaggle"),
    Path("Atividade_Pratica_Final_YOLO"),
]


def inline(value: str) -> str:
    value = html.escape(value, quote=False)
    value = re.sub(r"`([^`]+)`", r"<code>\1</code>", value)
    value = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", value)
    value = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', value)
    return value


def convert(markdown: str) -> str:
    lines = markdown.splitlines()
    out: list[str] = []
    paragraph: list[str] = []
    list_kind: str | None = None
    in_code = False
    code: list[str] = []

    def flush_paragraph() -> None:
        if paragraph:
            out.append("<p>" + inline(" ".join(paragraph)) + "</p>")
            paragraph.clear()

    def close_list() -> None:
        nonlocal list_kind
        if list_kind:
            out.append(f"</{list_kind}>")
            list_kind = None

    i = 0
    while i < len(lines):
        line = lines[i]
        if line.startswith("```"):
            flush_paragraph(); close_list()
            if in_code:
                out.append("<pre><code>" + html.escape("\n".join(code)) + "</code></pre>")
                code.clear()
            in_code = not in_code
            i += 1
            continue
        if in_code:
            code.append(line); i += 1; continue
        if not line.strip():
            flush_paragraph(); close_list(); i += 1; continue
        image = re.fullmatch(r"!\[([^\]]*)\]\(([^)]+)\)", line.strip())
        if image:
            flush_paragraph(); close_list()
            alt, src = image.groups()
            out.append(f'<figure><img src="{html.escape(src, quote=True)}" alt="{html.escape(alt, quote=True)}"><figcaption>{html.escape(alt)}</figcaption></figure>')
            i += 1; continue
        heading = re.match(r"^(#{1,6})\s+(.*)$", line)
        if line.startswith("> "):
            flush_paragraph(); close_list()
            out.append("<blockquote>" + inline(line[2:]) + "</blockquote>")
            i += 1; continue
        if heading:
            flush_paragraph(); close_list()
            level = len(heading.group(1))
            out.append(f"<h{level}>{inline(heading.group(2))}</h{level}>")
            i += 1; continue
        if line.startswith("|") and i + 1 < len(lines) and re.match(r"^\|?\s*:?-{3,}", lines[i + 1]):
            flush_paragraph(); close_list()
            headers = [x.strip() for x in line.strip().strip("|").split("|")]
            out.append("<table><thead><tr>" + "".join(f"<th>{inline(x)}</th>" for x in headers) + "</tr></thead><tbody>")
            i += 2
            while i < len(lines) and lines[i].startswith("|"):
                cells = [x.strip() for x in lines[i].strip().strip("|").split("|")]
                out.append("<tr>" + "".join(f"<td>{inline(x)}</td>" for x in cells) + "</tr>")
                i += 1
            out.append("</tbody></table>"); continue
        unordered = re.match(r"^\s*[-*]\s+(.*)$", line)
        ordered = re.match(r"^\s*\d+\.\s+(.*)$", line)
        if unordered or ordered:
            flush_paragraph()
            new_kind = "ul" if unordered else "ol"
            if list_kind != new_kind:
                close_list(); out.append(f"<{new_kind}>"); list_kind = new_kind
            out.append("<li>" + inline((unordered or ordered).group(1)) + "</li>")
            i += 1; continue
        close_list()
        paragraph.append(line.strip())
        i += 1
    flush_paragraph(); close_list()
    if in_code:
        out.append("<pre><code>" + html.escape("\n".join(code)) + "</code></pre>")
    return "\n".join(out)


STYLE = """
@page { size: A4; margin: 17mm 16mm; }
body { font: 10pt Arial, sans-serif; color: #202124; line-height: 1.42; }
h1, h2, h3 { color: #174a68; page-break-after: avoid; }
h1 { font-size: 21pt; border-bottom: 2px solid #174a68; padding-bottom: 5px; }
h2 { font-size: 15pt; margin-top: 22px; }
h3 { font-size: 12pt; margin-top: 16px; }
p { margin: 7px 0; }
table { width: 100%; border-collapse: collapse; margin: 10px 0 16px; font-size: 9pt; }
th, td { border: 1px solid #aab4bd; padding: 5px 6px; text-align: left; vertical-align: top; }
th { background: #e9f1f5; }
figure { margin: 14px 0 20px; text-align: center; page-break-inside: avoid; }
img { max-width: 100%; max-height: 155mm; object-fit: contain; }
figcaption { color: #5d6770; font-size: 8pt; margin-top: 4px; }
code, pre { background: #f2f4f5; font-family: Consolas, monospace; }
code { padding: 1px 3px; }
pre { white-space: pre-wrap; padding: 8px; font-size: 8.5pt; }
a { color: #145b86; }
blockquote { margin: 12px 0; padding: 9px 12px; border-left: 3px solid #ab7419; background: #fff8eb; }
"""


def main() -> None:
    for project in PROJECTS:
        source = project / "relatorio.md"
        title = source.read_text(encoding="utf-8").splitlines()[0].lstrip("# ")
        body = convert(source.read_text(encoding="utf-8"))
        document = f"<!doctype html><html lang='pt-BR'><meta charset='utf-8'><title>{html.escape(title)}</title><style>{STYLE}</style><body>{body}</body></html>"
        (project / "relatorio.html").write_text(document, encoding="utf-8")
        print(project / "relatorio.html")


if __name__ == "__main__":
    main()
