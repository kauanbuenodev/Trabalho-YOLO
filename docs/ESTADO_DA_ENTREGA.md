# Estado do material

Incluído: três enunciados, relatórios com figuras em PDF/Markdown, modelos treinados, datasets efetivamente usados, predições, métricas por época, parâmetros e scripts de reprodução.

**Correção necessária antes da entrega definitiva:** a auditoria por SHA-256 identificou fotos idênticas entre treino/validação/teste da prática 2 e entre treino/validação/reserva da final. As cinco imagens da reserva final têm cópias em outras divisões. Os modelos e as métricas preservados aqui documentam a execução anterior; não constituem uma avaliação independente. É necessário agrupar as duplicações, refazer as divisões, treinar novamente e atualizar as avaliações e imagens. A lista dos pares está em `CONFERENCIA.md`.

Identificação preenchida nos três relatórios: Kauan Reis Bueno; turma 8 Período; data 17/11/2026. Os gráficos e imagens foram produzidos nas execuções; o registro textual da atividade 1 é uma transcrição resumida, não uma captura de terminal. Os prints de terminal solicitados nos enunciados ainda precisam ser adicionados se exigidos como captura literal pelo professor.

A conferência para o repositório corrigiu o total anotado da reserva inédita da final de 25 para **20 objetos** no relatório, no CSV e no script. As contagens por imagem e os 19 TP / 1 FP / 1 FN permaneceram os mesmos.

O dataset preparado está incluído sem duplicar seus arquivos originais brutos em cada atividade. Os checkpoints repetidos em `runs/.../weights/` foram concentrados em `modelo/best.pt`; `last.pt` e ambientes virtuais não integram esta cópia. Os caminhos históricos nos arquivos de parâmetros continuam documentando a execução original.
