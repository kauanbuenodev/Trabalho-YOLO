# 03 — Projeto final

Treinamento de um detector de tomates maduros e não maduros e análise das previsões.

**Aluno:** Kauan Reis Bueno · **Turma:** 8 Período · **Data:** 17/11/2026

[Página inicial](../README.md) · [Relatórios das três atividades](../relatorios/README.md)

## Relatório e enunciado

- **[Abrir relatório em PDF](../relatorios/03_Projeto_Final_YOLO.pdf)**
- [Ler relatório com figuras no GitHub](relatorio.md)
- [Consultar enunciado](enunciado.pdf)

## Dados e evidências

| Material | Acesso |
|---|---|
| Melhor checkpoint | [modelo/best.pt](modelo/best.pt) |
| Pesos iniciais | [modelo/yolo26n.pt](modelo/yolo26n.pt) |
| Imagens e anotações | [Dataset](dataset/ready/) |
| Métricas e parâmetros | [Evidências](evidencias/) |
| Gráficos do treinamento | [Treinamento](runs/detect/resultados/treino_final_corrigido/) |
| Imagens detectadas | [Resultados](runs/detect/resultados/) |
| Comandos utilizados | [comandos.txt](comandos.txt) |

## Reprodução

Na raiz do repositório, após instalar as dependências indicadas no README inicial:

```powershell
.\.venv\Scripts\python.exe executar.py final inferir
.\.venv\Scripts\python.exe executar.py final avaliar
```

As novas execuções são salvas em `novas_execucoes/` na raiz.

## Separação dos dados

O dataset foi revisado antes deste novo treinamento: 78 imagens representativas, distribuídas em {'train': 58, 'val': 15, 'ineditas': 5}. A conferência não identificou sobreposições entre divisões pelos critérios SHA-256 e pHash aplicados. Consulte [a verificação](../docs/CONFERENCIA.md).
