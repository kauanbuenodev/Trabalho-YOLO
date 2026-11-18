"""Executa novamente treino, validação e predições com a divisão corrigida."""
from pathlib import Path
import argparse
import contextlib
import json
import os
import shutil
import sys
import hashlib

ROOT = Path(__file__).resolve().parent.parent


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("atividade", choices=["2", "final"])
    args = parser.parse_args()
    activity = args.atividade
    project = ROOT / ("Atividade_Pratica_II_YOLO_Kaggle" if activity == "2" else "Atividade_Pratica_Final_YOLO")
    os.chdir(project)
    data = project / ("dataset/yolo" if activity == "2" else "dataset/ready")
    evidence = project / "evidencias"
    # Rejeitar sobreposição exata ou perceptual antes de carregar o modelo.
    info = json.loads((evidence / "preparacao_corrigida.json").read_text(encoding="utf-8"))
    from conferir_entrega import check
    verification = check(activity, figures=False)
    if verification['errors']:
        raise ValueError(verification['errors'])
    groups = {}
    for entry in info["manifest"]:
        digest = entry["sha256"]
        if digest in groups: raise ValueError("Duplicação na divisão preparada")
        groups[digest] = entry["divisao"]
    # Manter experimentos antigos fora da cópia destinada à publicação.
    old = project / "runs"
    history = ROOT.parent / "Historico_Correcao_YOLO" / project.name / "runs"
    if old.exists():
        if old.resolve().parent != project.resolve() or not history.resolve().is_relative_to(ROOT.parent.resolve() / "Historico_Correcao_YOLO"):
            raise ValueError("Caminho de histórico inválido")
        if history.exists(): raise ValueError("Histórico existente: não sobrescrevi")
        history.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(old), str(history))
    from ultralytics import YOLO
    config = (data / "data.yaml").read_text(encoding="utf-8").splitlines()
    config[0] = "path: " + data.as_posix()
    config_path = evidence / "data_execucao.yaml"
    config_path.write_text("\n".join(config)+"\n",encoding="utf-8")
    size = 416 if activity == "2" else 640
    results = project / "runs/detect/resultados"
    name = "treinamento_corrigido" if activity == "2" else "treino_final_corrigido"
    train_dir = results / name
    def progress(trainer):
        if trainer.epoch >= trainer.epochs:
            return
        metrics = {k:round(float(v),4) for k,v in trainer.metrics.items() if "metrics/" in k}
        print(f"Atividade {activity} | epoca {trainer.epoch+1}/20 | {metrics}", file=sys.__stdout__,flush=True)
    with (evidence / "execucao_corrigida.txt").open("w",encoding="utf-8") as logfile, contextlib.redirect_stdout(logfile), contextlib.redirect_stderr(logfile):
        model = YOLO(str(project / "modelo/yolo26n.pt"))
        model.add_callback("on_fit_epoch_end",progress)
        model.train(data=str(config_path),epochs=20,imgsz=size,batch=4,device="cpu",workers=0,seed=42 if activity=="2" else 2026,project=str(results),name=name)
        shutil.copy2(train_dir / "weights/best.pt", project / "modelo/best.pt")
        shutil.copy2(train_dir / "results.csv", evidence / "resultados_treinamento.csv")
        shutil.copy2(train_dir / "args.yaml", evidence / "argumentos_treinamento.yaml")
        best = YOLO(str(project / "modelo/best.pt"))
        validation = best.val(data=str(config_path),split="val",imgsz=size,device="cpu",workers=0,project=str(results),name="validacao_corrigida")
        metrics = {"val": {k:float(v) for k,v in validation.results_dict.items()}}
        if activity == "2":
            test = best.val(data=str(config_path),split="test",imgsz=size,device="cpu",workers=0,project=str(results),name="avaliacao_teste")
            metrics["test"]={k:float(v) for k,v in test.results_dict.items()}
        source = data / ("images/test" if activity == "2" else "unseen/images")
        for conf,output_name in ([(.25,"conf025"),(.70,"conf070")] if activity=="2" else [(.25,"imagens_ineditas")]):
            best.predict(source=str(source),conf=conf,imgsz=size,device="cpu",save=True,save_txt=True,save_conf=True,project=str(results),name=output_name)
    metrics["train_dir"]=name
    metrics["epochs"]=20
    metrics["imgsz"]=size
    metrics["best_sha256"]=hashlib.sha256((project/"modelo/best.pt").read_bytes()).hexdigest()
    (evidence / "metricas_corrigidas.json").write_text(json.dumps(metrics,indent=2),encoding="utf-8")
    print(json.dumps(metrics,indent=2),file=sys.__stdout__,flush=True)


if __name__ == "__main__":
    main()
