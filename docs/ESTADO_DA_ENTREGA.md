# Estado da entrega

**Kauan Reis Bueno · 8 Período · 17/11/2026**

As duplicações da divisão anterior foram corrigidas antes de novos treinamentos. As atividades 2 e final têm novos checkpoints, métricas, predições, comparações e relatórios. Os arquivos antigos de dados e experimentos da versão anterior permanecem apenas no histórico do Git e nas cópias locais de histórico, para rastreabilidade; não integram a avaliação atual.

## Verificações concluídas

- 177 arquivos originais → 89 conteúdos distintos por SHA-256 → 78 representantes após agrupar versões próximas por pHash (distância ≤ 8).
- Uma anotação de altura zero da origem é descartada no processo de conferência.
- Atividade 2: 55 imagens de treino, 15 de validação e 8 de teste; duas classes em cada conjunto.
- Final: 58 imagens de treino e 15 de validação (73 anotadas), além de cinco inéditas reservadas antes do treino.
- Novos treinamentos de 20 épocas, partindo do YOLO26n pré-treinado de origem.
- Novos pesos, avaliações, cinco painéis visuais por atividade e comparação dos limiares 0,25/0,70 na atividade 2.
- Não foram encontrados pares sobrepostos por SHA-256 ou pHash ≤ 8 entre as divisões corrigidas.

## Limites e evidências

Os conjuntos de avaliação são pequenos. A checagem de similaridade não prova independência de toda cena possível; fotos externas são recomendadas para ampliar a avaliação. A atividade 1 preserva sua execução COCO8 e não exigiu novo treino.

Os relatórios apresentam imagens detectadas, referências anotadas, gráficos, parâmetros, métricas por época e registros textuais de execução. Capturas literais de tela do terminal solicitadas nos enunciados ainda não foram incluídas.

Os PDFs estão sincronizados nas pastas de cada atividade e em relatorios/. A divisão efetiva está em evidencias/divisoes.csv; o mapa completo da preparação e exclusões está em evidencias/preparacao_corrigida.json. Os checkpoints entregues ficam em modelo/best.pt, sem repetir os checkpoints intermediários no repositório.
