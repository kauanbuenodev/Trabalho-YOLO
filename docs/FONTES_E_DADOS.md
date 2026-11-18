# Fontes e preparação dos dados

## Tomates — prática 2 e final

Suman Kunwar. **Ripe and Unripe Tomatoes Dataset**, versão 2. Kaggle: https://www.kaggle.com/datasets/sumn2u/riped-and-unriped-tomato-dataset/versions/2.

Licença declarada pelo publicador: **CC BY-SA 4.0**, https://creativecommons.org/licenses/by-sa/4.0/. A atribuição ao autor deve acompanhar as cópias. Este aviso se aplica às imagens/anotações desse dataset e às adaptações das anotações incluídas.

177 imagens, 869 caixas de origem. A caixa da linha 22 de `riped_tomato_64.txt` tinha altura zero (`0 0.766023 0.130897 0.038707 0.000000`) e foi descartada nas cópias preparadas. Restaram 868 caixas válidas. As classes foram traduzidas, preservando os IDs: `0: unriped` → `nao_maduro`, `1: riped` → `maduro`.

Cada atividade inclui a partição efetivamente usada no treinamento. Não é necessário executar os preparadores para avaliar os pesos fornecidos. Os scripts `prepare_dataset.py` documentam a preparação; para refazê-la, baixe a versão indicada e forneça a pasta `detection/` extraída. As listas de arquivos incluídas em cada split são a referência exata da execução original, pois uma nova enumeração de arquivos pode alterar a ordem anterior ao sorteio.

As cinco imagens foram reservadas por nome de arquivo. A conferência por SHA-256 encontrou cópias idênticas dessas cinco imagens em treino/validação do modelo da final; portanto, elas não são inéditas. Também existem duplicações entre divisões da prática 2. Veja os pares em `CONFERENCIA.md`. Os pesos da final partiram do YOLO26n de origem, não do modelo treinado da prática 2. Uma reexecução válida precisa agrupar imagens idênticas antes de separar os dados.

## COCO8 — atividade 1

Oito imagens fornecidas pela Ultralytics para demonstração do pipeline. A cópia inclui `datasets/coco8/README.md` e `LICENSE`, com os avisos originais.

## Modelo e fotos

YOLO26n e biblioteca Ultralytics: https://github.com/ultralytics/ultralytics e https://docs.ultralytics.com/. Consulte a licença do fornecedor para reutilização dos pesos e biblioteca. Não foi atribuída uma nova licença global aos materiais de terceiros.

As três fotos de cachorro, carro e pessoa da atividade 1 foram fornecidas pelo aluno. A procedência/autorização para redistribuição dessas fotos deve ser conferida pelo autor do repositório ao escolher a visibilidade dele.
