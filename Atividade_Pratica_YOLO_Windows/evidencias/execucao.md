# Registro da execução da atividade 1

- Ambiente: Windows 11; Python 3.12.10; Ultralytics 8.4.214; PyTorch 2.15.0+cpu; AMD Ryzen 5 5500U; CPU; sem GPU/CUDA.
- `yolo checks`: Setup complete.
- Primeira predição automática: `bus.jpg`: 4 pessoas e 1 ônibus; `zidane.jpg`: 2 pessoas e 1 gravata.
- Treino: YOLO26n pré-treinado, COCO8, CPU, 3 épocas, `imgsz=320`, `batch=2`, `workers=0`.
- Validação COCO8: 4 imagens, 17 instâncias; Precision 0,705; Recall 0,633; mAP50 0,796; mAP50-95 0,576.
- Pesos: `modelo/best.pt`; original: `runs/detect/resultados/treino_coco8/weights/best.pt`.
- Imagens próprias, `conf=0.25`: cachorro.png → dog (0,795); carro.jpeg → car (0,863); pessoa.jpg → person (0,889).
- `pessoa.jpg`: 1 person com conf=0,25 e também 1 person com conf=0,70.
- `pessoa.jpg` com `best.pt` do COCO8: 1 person.

Resultados anotados: `runs/detect/resultados/`. Esse registro é uma transcrição resumida das saídas do terminal, não uma captura de tela.
