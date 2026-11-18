"""Remove duplicações exatas e versões visualmente próximas antes dos splits."""
from pathlib import Path
import argparse
from collections import defaultdict, Counter
import hashlib
import json
import random
import shutil
import math

ROOT = Path(__file__).resolve().parent.parent
NAMES = {0: "nao_maduro", 1: "maduro"}


def prepare(source, output, activity):
    import cv2
    import numpy as np
    from PIL import Image
    source, output = Path(source).resolve(), Path(output).resolve()
    allowed = ROOT / ("Atividade_Pratica_II_YOLO_Kaggle" if activity == "2" else "Atividade_Pratica_Final_YOLO")
    if not output.is_relative_to(allowed) or output == allowed or output.is_relative_to(source) or source.is_relative_to(output):
        raise ValueError("O destino deve ficar na pasta da atividade e separado dos dados de origem")
    pairs = []
    for image in sorted((source / "images").iterdir()):
        if image.suffix.lower() not in {".jpg", ".jpeg", ".png"}:
            continue
        label = source / "labels" / f"{image.stem}.txt"
        if not label.is_file():
            raise ValueError(f"Anotação ausente: {image.name}")
        keep, removed = [], 0
        for line in label.read_text(encoding="utf-8").splitlines():
            parts = line.split()
            if len(parts) != 5 or int(parts[0]) not in NAMES:
                raise ValueError(f"Rótulo inválido: {label}")
            values = list(map(float, parts[1:]))
            if any(not math.isfinite(x) or not 0 <= x <= 1 for x in values):
                raise ValueError(f"Coordenadas inválidas: {label}")
            if values[2] == 0 or values[3] == 0:
                removed += 1
            else:
                keep.append(line)
        a = np.asarray(Image.open(image).convert("L").resize((32, 32)), dtype=np.float32)
        d = cv2.dct(a)[:8, :8].flatten()
        phash = d > np.median(d[1:])
        pairs.append({"image": image, "labels": keep, "removed": removed, "sha256": hashlib.sha256(image.read_bytes()).hexdigest(), "phash": phash})
    # Componentes conexas: mesma cópia SHA ou distância de pHash <= 8.
    parent = list(range(len(pairs)))
    def find(i):
        while parent[i] != i:
            parent[i] = parent[parent[i]]
            i = parent[i]
        return i
    for i in range(len(pairs)):
        for j in range(i):
            if pairs[i]["sha256"] == pairs[j]["sha256"] or int(np.count_nonzero(pairs[i]["phash"] != pairs[j]["phash"])) <= 8:
                parent[find(i)] = find(j)
    groups = defaultdict(list)
    for i, pair in enumerate(pairs):
        groups[find(i)].append(pair)
    selected, exclusions = [], []
    for group in groups.values():
        # Um único representante, mantendo sua própria anotação: mais caixas válidas,
        # com desempate lexicográfico para garantir repetibilidade.
        chosen = sorted(group, key=lambda p: (-len(p["labels"]), p["image"].name))[0]
        if not chosen["labels"]:
            raise ValueError("Representante sem caixas válidas")
        selected.append(chosen)
        for member in group:
            exclusions.append({"original": member["image"].name, "representante": chosen["image"].name, "sha256": member["sha256"], "phash": ''.join('1' if x else '0' for x in member['phash'])})
    selected.sort(key=lambda p: p["image"].name)
    # Estratificar pela classe majoritária da imagem para manter as duas classes.
    strata = defaultdict(list)
    for item in selected:
        majority = Counter(int(line.split()[0]) for line in item["labels"]).most_common(1)[0][0]
        strata[majority].append(item)
    rng = random.Random(42 if activity == "2" else 2026)
    splits = {"train": [], "val": [], "test" if activity == "2" else "ineditas": []}
    if activity == "2":
        for cls in sorted(strata):
            items = strata[cls]
            rng.shuffle(items)
            a, b = round(len(items)*.7), round(len(items)*.2)
            splits["train"] += items[:a]
            splits["val"] += items[a:a+b]
            splits["test"] += items[a+b:]
    else:
        for cls in sorted(strata):
            rng.shuffle(strata[cls])
        reserved = []
        for i in range(5):
            cls = sorted(strata)[i % len(strata)]
            reserved.append(strata[cls].pop())
        splits["ineditas"] = reserved
        for cls in sorted(strata):
            items = strata[cls]
            a = round(len(items)*.8)
            splits["train"] += items[:a]
            splits["val"] += items[a:]
        if len(splits["train"])+len(splits["val"]) < 60:
            raise ValueError("Menos de 60 imagens distintas para treino/validação")
    if output.exists():
        shutil.rmtree(output)
    manifest = []
    for split, items in splits.items():
        found = set()
        for item in items:
            image = item["image"]
            image_dir = output / ("unseen/images" if split == "ineditas" else f"images/{split}")
            label_dir = output / ("unseen/labels_referencia" if split == "ineditas" else f"labels/{split}")
            image_dir.mkdir(parents=True, exist_ok=True)
            label_dir.mkdir(parents=True, exist_ok=True)
            shutil.copy2(image, image_dir / image.name)
            (label_dir / f"{image.stem}.txt").write_text("\n".join(item["labels"])+"\n", encoding="utf-8")
            found.update(int(x.split()[0]) for x in item["labels"])
            manifest.append({"divisao": split, "imagem": image.name, "sha256": item["sha256"], "caixas": len(item["labels"])})
        if found != {0,1}:
            raise ValueError(f"Classes ausentes em {split}: {found}")
    relative = output.relative_to(allowed).as_posix()
    yaml = [f"path: {relative}", "train: images/train", "val: images/val"]
    if activity == "2": yaml.append("test: images/test")
    yaml += ["names:", "  0: nao_maduro", "  1: maduro"]
    (output / "data.yaml").write_text("\n".join(yaml)+"\n", encoding="utf-8")
    record = {"activity": activity, "original_images": len(pairs), "sha256_unique": len({p['sha256'] for p in pairs}), "visual_unique": len(selected), "phash_max_distance": 8, "seed": 42 if activity == "2" else 2026, "invalid_boxes_in_original": sum(p["removed"] for p in pairs), "splits": {s:len(x) for s,x in splits.items()}, "boxes": {s:sum(len(y['labels']) for y in x) for s,x in splits.items()}, "manifest": manifest, "groups": exclusions}
    (allowed / "evidencias").mkdir(exist_ok=True)
    (allowed / "evidencias/preparacao_corrigida.json").write_text(json.dumps(record, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps({k:v for k,v in record.items() if k not in ['manifest','groups']}, ensure_ascii=False, indent=2))
    return record


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("atividade", choices=["2", "final"])
    parser.add_argument("source", type=Path)
    args = parser.parse_args()
    folder = ROOT / ("Atividade_Pratica_II_YOLO_Kaggle/dataset/yolo" if args.atividade == "2" else "Atividade_Pratica_Final_YOLO/dataset/ready")
    prepare(args.source, folder, args.atividade)


if __name__ == "__main__":
    main()
