# Fontes e preparação dos dados

## Tomates — prática 2 e final

Suman Kunwar. **Ripe and Unripe Tomatoes Dataset**, versão 2. Kaggle: https://www.kaggle.com/datasets/sumn2u/riped-and-unriped-tomato-dataset/versions/2.

Licença declarada: **CC BY-SA 4.0**, https://creativecommons.org/licenses/by-sa/4.0/. A atribuição deve acompanhar cópias das imagens e anotações. Os nomes de classe foram traduzidos preservando os IDs: 0 (unriped) = nao_maduro; 1 (riped) = maduro.

O download contém 177 arquivos e 869 caixas de origem. Uma caixa tem altura zero e é removida durante a validação. Existem 89 conteúdos distintos por SHA-256; agrupando também versões visualmente próximas com pHash de 64 bits e distância ≤ 8, foram mantidos 78 representantes. Cada representante mantém suas próprias anotações. Foi escolhido o membro com mais caixas válidas por grupo, com desempate lexicográfico. Os representantes incluem 459 caixas no total.

A ordem é determinística e as partições são estratificadas pela classe majoritária da imagem. Na atividade 2, a seed 42 produz 55 treino, 15 validação e 8 teste. Na final, a seed 2026 reserva cinco imagens antes da divisão das demais em 58 treino e 15 validação. Há duas classes em cada divisão. As partições diferem entre atividades, que são experimentos separados. Os dois modelos partem do YOLO26n de origem; os pesos de uma atividade não alimentam a outra.

Os dados já preparados estão incluídos. Para reconstruí-los, baixe a versão indicada e execute scripts/corrigir_dados.py com a pasta detection extraída. O mapa de cada arquivo de origem para o representante e a lista de imagens de cada divisão estão em evidencias/preparacao_corrigida.json. O processo e as verificações de separação estão registrados em docs/CONFERENCIA.md.

O critério pHash é uma ferramenta de triagem conservadora, não uma garantia de independência de todas as cenas. As métricas devem considerar o conjunto pequeno e ser complementadas futuramente com fotos externas.

## COCO8 — atividade 1

Oito imagens fornecidas pela Ultralytics para demonstração do pipeline. Os avisos originais estão em datasets/coco8/README.md e LICENSE na pasta da atividade 1.

## Modelos e fotos da atividade 1

YOLO26n e Ultralytics: https://github.com/ultralytics/ultralytics e https://docs.ultralytics.com/. Consulte a licença do fornecedor para reutilização dos pesos e biblioteca. Não foi atribuída uma nova licença global aos materiais de terceiros.

As fotos de cachorro, carro e pessoa da atividade 1 foram fornecidas pelo aluno.
