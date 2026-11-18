"""Confere pares de dados, figuras dos relatórios e modelos da entrega."""
from pathlib import Path
import csv
import hashlib
import re

ROOT = Path(__file__).resolve().parent.parent
PROJECTS = {
    "Atividade_Pratica_YOLO_Windows": ("datasets/coco8", {"train": 4, "val": 4}),
    "Atividade_Pratica_II_YOLO_Kaggle": ("dataset/yolo", {"train": 123, "val": 35, "test": 19}),
    "Atividade_Pratica_Final_YOLO": ("dataset/ready", {"train": 137, "val": 35, "ineditas": 5}),
}


def main():
    problems = []
    summaries = []
    for name, (data_folder, expected) in PROJECTS.items():
        project = ROOT / name
        data = project / data_folder
        seen = {}
        counts = {}
        duplicates = []
        for split, count in expected.items():
            folder = data / ("unseen/images" if split == "ineditas" else f"images/{split}")
            labels = data / ("unseen/labels_referencia" if split == "ineditas" else f"labels/{split}")
            images = sorted(f for f in folder.iterdir() if f.suffix.lower() in {".jpg", ".jpeg", ".png"})
            counts[split] = len(images)
            if len(images) != count:
                problems.append(f"{name}/{split}: {len(images)} imagens, esperado {count}")
            for image in images:
                label = labels / (image.stem + ".txt")
                if not label.is_file():
                    problems.append(f"Anotação ausente: {label}")
                    continue
                for line in label.read_text(encoding="utf-8").splitlines():
                    values = line.split()
                    if len(values) != 5:
                        problems.append(f"Formato inválido: {label}")
                    elif any(not 0 <= float(v) <= 1 for v in values[1:]) or float(values[3]) <= 0 or float(values[4]) <= 0:
                        problems.append(f"Caixa inválida: {label}")
                digest = hashlib.sha256(image.read_bytes()).hexdigest()
                if digest in seen and seen[digest][0] != split:
                    duplicates.append((seen[digest], (split, image.name)))
                seen[digest] = (split, image.name)
        text = (project / "relatorio.md").read_text(encoding="utf-8")
        for target in re.findall(r"!\[[^\]]*\]\(([^)]+)\)", text):
            if not (project / target).is_file():
                problems.append(f"Figura ausente: {name}/{target}")
        for target in ["relatorio.pdf", "enunciado.pdf", "modelo/best.pt", "modelo/yolo26n.pt"]:
            if not (project / target).is_file():
                problems.append(f"Arquivo ausente: {name}/{target}")
        if duplicates:
            problems.append(f"{name}: imagens idênticas em divisões diferentes: {duplicates}")
        summaries.append(f"- {name}: {counts}; figuras, pesos e PDFs presentes; {len(duplicates)} duplicações exatas entre divisões.")
    contents = "# Conferência da entrega\n\n" + "\n".join(summaries)
    contents += "\n\nA comparação de duplicações usa SHA-256 e detecta arquivos idênticos; não identifica fotos quase iguais. Esta conferência não treina novamente os modelos.\n"
    if problems:
        contents += "\n## Problemas encontrados\n\n" + "\n".join("- " + p for p in problems)
    else:
        contents += "\nConferência concluída sem arquivos obrigatórios ou anotações inválidas nos itens verificados.\n"
    (ROOT / "docs/CONFERENCIA.md").write_text(contents, encoding="utf-8")
    print(contents)
    raise SystemExit(1 if problems else 0)


if __name__ == "__main__":
    main()
