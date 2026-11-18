# Conferência da entrega corrigida

A divisão foi refeita antes dos novos treinamentos. Foram conferidos pares imagem/anotação, classes, caixas, integridade SHA-256 e distância de pHash entre divisões.

| Atividade | Divisões | Imagens distintas | Menor distância pHash entre divisões | Problemas |
|---|---|---:|---:|---:|
| 1 | train: 4; val: 4 | 8 | não aplicado | 0 |
| 2 | train: 55; val: 15; test: 8 | 78 | 14 | 0 |
| final | train: 58; val: 15; ineditas: 5 | 78 | 14 | 0 |

O critério conservador de similaridade agrupa pHash com distância de Hamming ≤ 8. Quando a coluna Problemas é zero, não há sobreposições pelos critérios aplicados. Essa checagem não prova independência de todas as cenas possíveis; recomenda-se também avaliar fotos externas ao dataset.

Os mapas de exclusão e manifestos completos estão em evidencias/preparacao_corrigida.json de cada atividade. Os resultados antigos com vazamento foram substituídos após os novos treinamentos.
