# 01 — YOLO no Windows

Configuração do ambiente, inferência com YOLO26n e treinamento experimental no COCO8.

**Aluno:** Kauan Reis Bueno · **Turma:** 8 Período · **Data:** 17/11/2026

[Página inicial](../README.md) · [Relatórios das três atividades](../relatorios/README.md)

## Relatório e enunciado

- **[Abrir relatório em PDF](../relatorios/01_YOLO_Windows.pdf)**
- [Ler relatório com figuras no GitHub](relatorio.md)
- [Consultar enunciado](enunciado.pdf)

## Dados e evidências

| Material | Acesso |
|---|---|
| Melhor checkpoint | [modelo/best.pt](modelo/best.pt) |
| Pesos iniciais | [modelo/yolo26n.pt](modelo/yolo26n.pt) |
| Imagens e anotações | [Dataset](datasets/coco8/) |
| Métricas e parâmetros | [Evidências](evidencias/) |
| Gráficos do treinamento | [Treinamento](runs/detect/resultados/treino_coco8/) |
| Imagens detectadas | [Resultados](runs/detect/resultados/) |
| Comandos utilizados | [comandos.txt](comandos.txt) |

## Reprodução

Na raiz do repositório, após instalar as dependências indicadas no README inicial:

```powershell
.\.venv\Scripts\python.exe executar.py 1 inferir
.\.venv\Scripts\python.exe executar.py 1 avaliar
```

As novas execuções são salvas em `novas_execucoes/` na raiz.
