"""Sincroniza README e documentação com as duas execuções corrigidas."""
from pathlib import Path
import json
import re

ROOT=Path(__file__).resolve().parent.parent


def main():
    projects={'2':ROOT/'Atividade_Pratica_II_YOLO_Kaggle','final':ROOT/'Atividade_Pratica_Final_YOLO'}
    info={a:json.loads((p/'evidencias/metricas_corrigidas.json').read_text(encoding='utf-8')) for a,p in projects.items()}
    analyses={a:json.loads((p/'evidencias/comparacao_corrigida.json').read_text(encoding='utf-8')) for a,p in projects.items()}
    def f(value):return f'{value:.3f}'.replace('.',',')
    readme=ROOT/'README.md';text=readme.read_text(encoding='utf-8')
    text=re.sub(r'> \*\*Limitação identificada na conferência:\*\*[^\n]*', '> **Separação dos dados verificada:** as duplicações identificadas na origem foram tratadas antes dos novos treinamentos. As atividades 2 e final usam 78 imagens representativas, com conjuntos separados por SHA-256 e pHash. Os resultados abaixo pertencem às execuções corrigidas. [Consultar a verificação](docs/CONFERENCIA.md).',text)
    for a,label,split in [('2','02','Partição de teste · 8 imagens'),('final','03','Validação · 15 imagens')]:
        m=info[a]['test' if a=='2' else 'val'];values=[m[k] for k in ['metrics/precision(B)','metrics/recall(B)','metrics/mAP50(B)','metrics/mAP50-95(B)']]
        row=f"| {label} | YOLO26n | 20 | {split} | "+' | '.join(f(x) for x in values)+' |'
        text=re.sub(r'\| '+label+r' \| YOLO26n \|[^\n]+',row,text)
    a=analyses['final'];t=a['totals']['imagens_ineditas']
    text=re.sub(r'(?:Essas|As) métricas provêm[^\n]+', f"As métricas provêm de conjuntos diferentes. A atividade 2 usa o teste separado e a final usa a validação. Nas cinco imagens inéditas da final, foram anotados {a['total_gt']} objetos: {t['tp']} correspondências corretas, {t['fp']} falsos positivos e {t['fn']} omissões em conf=0,25, considerando classe correta e IoU ≥ 0,50. A conferência não encontrou cópias exatas nem pares semelhantes pelo critério aplicado entre essas imagens e o treino/validação. A amostra continua pequena, e não garante desempenho em qualquer cenário.",text)
    text=text.replace('treino de 20 épocas; comparação entre', 'novo treino de 20 épocas; comparação entre')
    sample2=Path(analyses['2']['samples'][0]).stem;samplef=Path(analyses['final']['samples'][0]).stem
    text=text.replace('conf025/riped_tomato_17.jpg',f'conf025/{sample2}.jpg').replace('imagens_ineditas/riped_tomato_47.jpg',f'imagens_ineditas/{samplef}.jpg')
    text=text.replace('Esses comandos reproduzem a execução documentada; a reprodução não corrige o vazamento de dados identificado.', 'Esses comandos reproduzem a execução corrigida sobre os dados já preparados, com controle de duplicações aplicado antes dos novos treinamentos.')
    text=text.replace('o treinamento da final levou aproximadamente 25 minutos.', 'o tempo de treinamento depende da quantidade de imagens e dos recursos disponíveis.')
    # Informar os totais de cada nova divisão antes de explicar a execução.
    if '### Dados utilizados após a revisão' not in text:
        text=text.replace('## Organização do repositório', '### Dados utilizados após a revisão\n\n| Atividade | Treino | Validação | Teste ou inéditas |\n|---|---:|---:|---:|\n| 02 | 55 | 15 | 8 de teste |\n| 03 | 58 | 15 | 5 inéditas |\n\nDos 177 arquivos da origem, 89 têm conteúdo distinto por SHA-256. O agrupamento de versões próximas por pHash resultou em 78 representantes. Na final, treino e validação somam 73 imagens anotadas, atendendo ao mínimo de 60 do enunciado.\n\n## Organização do repositório')
    readme.write_text(text,encoding='utf-8')
    index=ROOT/'relatorios/README.md';text=index.read_text(encoding='utf-8').replace('As limitações da avaliação das atividades 2 e final estão documentadas nos relatórios e na [auditoria](../docs/CONFERENCIA.md).','Os relatórios 2 e final foram atualizados após a correção da separação dos dados e a repetição dos treinamentos. A verificação e os limites da avaliação estão documentados em [conferência](../docs/CONFERENCIA.md).');index.write_text(text,encoding='utf-8')
    (ROOT/'docs/ESTADO_DA_ENTREGA.md').write_text('''# Estado da entrega

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
''',encoding='utf-8')
    (ROOT/'docs/FONTES_E_DADOS.md').write_text('''# Fontes e preparação dos dados

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
''',encoding='utf-8')
    print('README e documentação atualizados com os resultados corrigidos.')


if __name__=='__main__':main()
