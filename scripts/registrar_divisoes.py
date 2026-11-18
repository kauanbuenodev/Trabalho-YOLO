"""Registra as listas de arquivos dos conjuntos já preparados."""
from pathlib import Path
import csv

ROOT = Path(__file__).resolve().parent.parent
DATASETS = {
    "Atividade_Pratica_YOLO_Windows": "datasets/coco8",
    "Atividade_Pratica_II_YOLO_Kaggle": "dataset/yolo",
    "Atividade_Pratica_Final_YOLO": "dataset/ready",
}


def main():
    for activity, folder in DATASETS.items():
        project = ROOT / activity
        data = project / folder
        with (project / "evidencias/divisoes.csv").open("w", encoding="utf-8", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["divisao", "imagem", "anotacao"])
            for image in sorted(data.rglob("*")):
                if image.suffix.lower() not in {".jpg", ".jpeg", ".png"}:
                    continue
                relative = image.relative_to(data)
                if relative.parts[0] == "unseen":
                    split = "ineditas"
                    label = data / "unseen/labels_referencia" / (image.stem + ".txt")
                elif relative.parts[0] == "images":
                    split = relative.parts[1]
                    label = data / "labels" / split / (image.stem + ".txt")
                else:
                    continue
                writer.writerow([split, relative.as_posix(), label.relative_to(data).as_posix()])


if __name__ == "__main__":
    main()
