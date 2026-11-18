"""Lista os arquivos da entrega e seus hashes SHA-256."""
from pathlib import Path
import csv
import hashlib

ROOT = Path(__file__).resolve().parent.parent


def main():
    paths = sorted(p for p in ROOT.rglob("*") if p.is_file() and not any(x in p.relative_to(ROOT).parts for x in [".git", ".venv", "__pycache__", "novas_execucoes"]) and p.suffix not in {".cache", ".pyc", ".log", ".zip"} and not ("runs" in p.relative_to(ROOT).parts and "weights" in p.relative_to(ROOT).parts) and p.name not in {"INVENTARIO.csv", "TAMANHO.md"})
    # Manter os hashes iguais aos arquivos publicados com eol=lf no Git.
    for p in paths:
        if p.suffix in {'.py','.md','.html','.csv','.yaml','.yml','.txt','.json'} or p.name in {'.gitignore','.gitattributes'}:
            content=p.read_bytes().decode('utf-8-sig').replace('\r\n','\n')
            p.write_bytes(content.encode('utf-8'))
    total = sum(p.stat().st_size for p in paths)
    with (ROOT / "docs/INVENTARIO.csv").open("w", encoding="utf-8", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["arquivo", "bytes", "sha256"])
        for p in paths:
            writer.writerow([p.relative_to(ROOT).as_posix(), p.stat().st_size, hashlib.sha256(p.read_bytes()).hexdigest()])
    biggest = max(paths, key=lambda p: p.stat().st_size)
    note = f"# Tamanho da cópia para Git\n\n{len(paths)} arquivos inventariados, {total / 1048576:.1f} MiB antes da compressão do Git.\n\nMaior arquivo: `{biggest.relative_to(ROOT).as_posix()}` ({biggest.stat().st_size / 1048576:.1f} MiB).\n\nOs hashes de todos os artefatos estão em `INVENTARIO.csv`. Arquivos idênticos entre atividades podem ser deduplicados pelo armazenamento de objetos do Git.\n"
    (ROOT / "docs/TAMANHO.md").write_text(note, encoding="utf-8")
    print(note)


if __name__ == "__main__":
    main()
