"""Reproduz inferência, avaliação e treinamento dos projetos incluídos."""
from pathlib import Path
import argparse
import os
import runpy
import sys

ROOT = Path(__file__).resolve().parent
PROJECTS = {"1": "Atividade_Pratica_YOLO_Windows", "2": "Atividade_Pratica_II_YOLO_Kaggle", "final": "Atividade_Pratica_Final_YOLO"}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("atividade", choices=PROJECTS)
    parser.add_argument("acao", choices=["inferir", "avaliar", "comparar", "treinar"])
    args = parser.parse_args()
    project = ROOT / PROJECTS[args.atividade]
    os.chdir(project)
    if args.acao == "comparar":
        if args.atividade == "1":
            print("As comparações da atividade 1 estão em runs/detect/resultados/pessoa_025 e pessoa_070.")
            return
        runpy.run_path(str(project / ("compare_predictions.py" if args.atividade == "2" else "compare_unseen.py")), run_name="__main__")
        return
    if args.atividade in {"2", "final"}:
        sys.path.insert(0,str(ROOT / "scripts"))
        from conferir_entrega import check
        verification=check(args.atividade,figures=False)
        if verification['errors']:
            raise SystemExit('Dados divergentes ou sobrepostos: '+ '; '.join(verification['errors']))
    from ultralytics import YOLO
    output = ROOT / "novas_execucoes" / args.atividade
    output.mkdir(parents=True, exist_ok=True)
    if args.atividade == "1":
        data_root = project / "datasets/coco8"
        size, epochs, batch = 320, 3, 2
        source = project / "imagens"
    else:
        data_root = project / ("dataset/yolo" if args.atividade == "2" else "dataset/ready")
        size, epochs, batch = (416 if args.atividade == "2" else 640), 20, 4
        source = data_root / ("images/test" if args.atividade == "2" else "unseen/images")
    if args.acao == "inferir":
        model = YOLO(str(project / "modelo/best.pt"))
        for conf in ([.25, .70] if args.atividade in {"1", "2"} else [.25]):
            model.predict(source=str(source), conf=conf, imgsz=size, device="cpu", save=True, save_txt=True, save_conf=True, project=str(output), name=f"conf{conf:.2f}")
        if args.atividade == "1":
            YOLO(str(project / "modelo/yolo26n.pt")).predict(source=str(source), conf=.25, device="cpu", save=True, project=str(output), name="pre_treinado")
        return
    if args.atividade == "1":
        # Os nomes e IDs do COCO permanecem os mesmos do treino original.
        import ultralytics
        original = Path(ultralytics.__file__).parent / "cfg/datasets/coco8.yaml"
        from ultralytics.utils import YAML
        config = YAML.load(original)
        config.pop("download", None)
    else:
        config = {"train": "images/train", "val": "images/val", "names": {0: "nao_maduro", 1: "maduro"}}
        if args.atividade == "2":
            config["test"] = "images/test"
    from ultralytics.utils import YAML
    config["path"] = data_root.as_posix()
    yaml_path = output / "data_execucao.yaml"
    YAML.save(yaml_path, config)
    if args.acao == "avaliar":
        YOLO(str(project / "modelo/best.pt")).val(data=str(yaml_path), split="test" if args.atividade == "2" else "val", imgsz=size, device="cpu", workers=0, project=str(output), name="avaliacao")
    else:
        YOLO(str(project / "modelo/yolo26n.pt")).train(data=str(yaml_path), epochs=epochs, imgsz=size, batch=batch, device="cpu", workers=0, seed=42 if args.atividade == "2" else (2026 if args.atividade == "final" else 0), project=str(output), name="treino")


if __name__ == "__main__":
    main()
