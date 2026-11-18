"""Valida pares imagem/anotação YOLO e cria split 70/20/10 reproduzível."""
from __future__ import annotations

import argparse
import random
import shutil
from pathlib import Path

CLASSES = {0: "nao_maduro", 1: "maduro"}
IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path, help="Pasta detection do dataset extraído")
    parser.add_argument("--output", type=Path, default=Path("dataset/yolo"))
    args = parser.parse_args()
    image_root, label_root = args.source / "images", args.source / "labels"
    if not image_root.is_dir() or not label_root.is_dir():
        raise SystemExit(f"Esperava encontrar {image_root} e {label_root}")

    labels = {p.stem: p for p in label_root.rglob("*.txt")}
    images = [p for p in image_root.rglob("*") if p.is_file() and p.suffix.lower() in IMAGE_EXTS and p.stem in labels]
    if not images:
        raise SystemExit("Nenhum par imagem/.txt encontrado")
    if len({p.stem for p in images}) != len(images):
        raise SystemExit("Há nomes-base duplicados; renomeie-os antes para evitar pareamento ambíguo")

    clean_labels: dict[str, str] = {}
    removed_degenerate = 0
    for image in images:
        label = labels[image.stem]
        keep: list[str] = []
        for line_no, line in enumerate(label.read_text(encoding="utf-8").splitlines(), 1):
            parts = line.split()
            if len(parts) != 5:
                raise SystemExit(f"Anotação não é detecção YOLO: {label}:{line_no}")
            cls = int(parts[0])
            values = [float(x) for x in parts[1:]]
            if cls not in CLASSES or any(x < 0 or x > 1 for x in values):
                raise SystemExit(f"Classe/coordenadas inválidas em {label}:{line_no}: {line.strip()}")
            if values[2] == 0 or values[3] == 0:
                removed_degenerate += 1
                continue
            keep.append(line)
        clean_labels[image.stem] = "\n".join(keep) + ("\n" if keep else "")

    random.Random(42).shuffle(images)
    n = len(images)
    n_train, n_val = int(n * .70), int(n * .20)
    splits = {"train": images[:n_train], "val": images[n_train:n_train+n_val], "test": images[n_train+n_val:]}
    if min(map(len, splits.values())) == 0:
        raise SystemExit("Dataset pequeno demais para dividir em treino/validação/teste")
    if args.output.exists():
        shutil.rmtree(args.output)
    for split, split_images in splits.items():
        for image in split_images:
            dest_image = args.output / "images" / split / image.name
            dest_label = args.output / "labels" / split / f"{image.stem}.txt"
            dest_image.parent.mkdir(parents=True, exist_ok=True)
            dest_label.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(image, dest_image)
            dest_label.write_text(clean_labels[image.stem], encoding="utf-8")
    yaml = ["path: dataset/yolo", "train: images/train", "val: images/val", "test: images/test", "names:"]
    yaml += [f"  {idx}: {name}" for idx, name in CLASSES.items()]
    (args.output / "data.yaml").write_text("\n".join(yaml) + "\n", encoding="utf-8")
    print(f"Anotadas: {n}; treino: {len(splits['train'])}; validação: {len(splits['val'])}; teste: {len(splits['test'])}")
    print(f"Caixas degeneradas (largura/altura zero) removidas apenas nas cópias preparadas: {removed_degenerate}")
    print("Classes: 0=nao_maduro, 1=maduro; divisão determinística seed=42")


if __name__ == "__main__":
    main()
