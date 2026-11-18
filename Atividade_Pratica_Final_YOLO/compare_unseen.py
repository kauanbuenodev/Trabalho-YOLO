"""Compara as cinco imagens inéditas com rótulos reservados, IoU >= 0.50."""
from pathlib import Path

ROOT = Path("dataset/ready/unseen")
PRED = Path("runs/detect/resultados/imagens_ineditas/labels")


def read_boxes(path: Path, predicted: bool):
    boxes = []
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


def main():
    totals = [0, 0, 0]
    total_gt = total_pred = 0
    print("image,gt,pred,tp,fp,fn")
    for image in sorted((ROOT / "images").glob("*")):
        stem = image.stem
        gt = read_boxes(ROOT / "labels_referencia" / f"{stem}.txt", False)
        pred_file = PRED / f"{stem}.txt"
        preds = read_boxes(pred_file, True) if pred_file.exists() else []
        unmatched = set(range(len(gt)))
        tp = fp = 0
        for cls, box, _ in sorted(preds, key=lambda item: item[2], reverse=True):
            candidates = [(iou(box, gt[i][1]), i) for i in unmatched if gt[i][0] == cls]
            best = max(candidates, default=(0.0, -1))
            if best[0] >= .5:
                tp += 1
                unmatched.remove(best[1])
            else:
                fp += 1
        fn = len(unmatched)
        total_gt += len(gt)
        total_pred += len(preds)
        totals = [a+b for a, b in zip(totals, (tp, fp, fn))]
        print(f"{stem},{len(gt)},{len(preds)},{tp},{fp},{fn}")
    print(f"TOTAL,{total_gt},{total_pred},{totals[0]},{totals[1]},{totals[2]}")


if __name__ == "__main__":
    main()
