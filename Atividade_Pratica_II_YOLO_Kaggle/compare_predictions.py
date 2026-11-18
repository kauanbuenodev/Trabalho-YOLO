"""Compara previsões exportadas contra rótulos de teste com IoU >= 0.50."""
from pathlib import Path

ROOT = Path("dataset/yolo")
PRED = Path("runs/detect/resultados")
SAMPLES = [
    "riped_tomato_15",
    "riped_tomato_17",
    "unriped_tomato_2",
    "unriped_tomato_39",
    "unriped_tomato_61",
]


def read_boxes(path: Path, predicted: bool):
    boxes = []
    if not path.exists():
        return boxes
    for line in path.read_text(encoding="utf-8").splitlines():
        values = line.split()
        cls = int(values[0])
        xywh = list(map(float, values[1:5]))
        conf = float(values[5]) if predicted and len(values) > 5 else 1.0
        boxes.append((cls, xywh, conf))
    return boxes


def iou(a, b):
    ax, ay, aw, ah = a
    bx, by, bw, bh = b
    left, top = max(ax-aw/2, bx-bw/2), max(ay-ah/2, by-bh/2)
    right, bottom = min(ax+aw/2, bx+bw/2), min(ay+ah/2, by+bh/2)
    intersection = max(0.0, right-left) * max(0.0, bottom-top)
    union = aw*ah + bw*bh - intersection
    return intersection/union if union else 0.0


def score(gt, pred):
    unmatched = set(range(len(gt)))
    tp = fp = 0
    for cls, box, _ in sorted(pred, key=lambda item: item[2], reverse=True):
        matches = [(iou(box, gt[i][1]), i) for i in unmatched if gt[i][0] == cls]
        best = max(matches, default=(0.0, -1))
        if best[0] >= .5:
            tp += 1
            unmatched.remove(best[1])
        else:
            fp += 1
    return tp, fp, len(unmatched)


def main():
    totals = {"conf025": [0, 0, 0], "conf070": [0, 0, 0]}
    print("image,gt,tp025,fp025,fn025,tp070,fp070,fn070")
    for image in sorted((ROOT / "images/test").glob("*")):
        stem = image.stem
        gt = read_boxes(ROOT / "labels/test" / f"{stem}.txt", False)
        vals = []
        for setting in totals:
            pred = read_boxes(PRED / setting / "labels" / f"{stem}.txt", True)
            result = score(gt, pred)
            totals[setting] = [a+b for a, b in zip(totals[setting], result)]
            vals.extend(result)
        if stem in SAMPLES:
            print(f"{stem},{len(gt)},{','.join(map(str, vals))}")
    print("ALL19,gt,tp025,fp025,fn025,tp070,fp070,fn070")
    print(f"ALL19,,{','.join(map(str, totals['conf025'] + totals['conf070']))}")


if __name__ == "__main__":
    main()
