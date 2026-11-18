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
| Gráficos do treinamento | [Treinamento](runs/detect/resultados/treino_final/) |
| Imagens detectadas | [Resultados](runs/detect/resultados/) |
| Comandos utilizados | [comandos.txt](comandos.txt) |

## Reprodução

Na raiz do repositório, após instalar as dependências indicadas no README inicial:

```powershell
.\.venv\Scripts\python.exe executar.py final inferir
.\.venv\Scripts\python.exe executar.py final avaliar
```

As novas execuções são salvas em `novas_execucoes/` na raiz.

## Limitação da avaliação

A auditoria encontrou imagens idênticas em divisões diferentes. Consulte [a conferência dos dados](../docs/CONFERENCIA.md) e [as correções necessárias](../docs/ESTADO_DA_ENTREGA.md) antes de interpretar as métricas como avaliação independente.
