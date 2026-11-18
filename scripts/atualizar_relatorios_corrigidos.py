"""Preenche os relatórios com as métricas e comparações da nova execução."""
from pathlib import Path
import json
import re
import argparse

ROOT=Path(__file__).resolve().parent.parent
NAMES={'2':'Atividade_Pratica_II_YOLO_Kaggle','final':'Atividade_Pratica_Final_YOLO'}
IDENTITY='**Nome:** Kauan Reis Bueno  \n**Turma:** 8 Período  \n**Data:** 17/11/2026\n'
URL='https://www.kaggle.com/datasets/sumn2u/riped-and-unriped-tomato-dataset/versions/2'


def number(x):return f'{x:.3f}'.replace('.',',')
def metric_line(m):
    return f"Precision **{number(m['metrics/precision(B)'])}**, Recall **{number(m['metrics/recall(B)'])}**, mAP50 **{number(m['metrics/mAP50(B)'])}** e mAP50-95 **{number(m['metrics/mAP50-95(B)'])}**."


def update(activity):
    project=ROOT/NAMES[activity]
    def read(name):return json.loads((project/'evidencias'/name).read_text(encoding='utf-8'))
    data=read('preparacao_corrigida.json'); metrics=read('metricas_corrigidas.json'); analysis=read('comparacao_corrigida.json')
    splits=data['splits']; objects=data['boxes']; train=metrics['train_dir']
    head='# Relatório técnico — '+('Atividade prática II: YOLO + Kaggle' if activity=='2' else 'Atividade prática final: detecção com YOLO')+'\n\n'+IDENTITY
    preparation=f"""## Projeto e preparação dos dados

O projeto localiza tomates e distingue dois estágios de maturação: `0: nao_maduro` (original `unriped`) e `1: maduro` (original `riped`). A localização é representada por caixas delimitadoras.

Fonte: **Ripe and Unripe Tomatoes Dataset**, de Suman Kunwar, [Kaggle]({URL}). Licença declarada: **CC BY-SA 4.0**. O conjunto original contém 177 arquivos de imagem; a finalidade é apoiar aplicações de visão computacional na agricultura.

A revisão identificou cópias idênticas e versões muito semelhantes de uma mesma fotografia. Antes da nova divisão, foram calculados SHA-256 e hash perceptual (pHash, 64 bits). Arquivos com mesmo SHA-256 ou distância de Hamming de pHash ≤ 8 foram agrupados. Foi mantida uma imagem por grupo, escolhendo o arquivo com mais caixas válidas e desempate pelo nome. A anotação usada é a do próprio arquivo selecionado; não foram combinadas caixas de imagens diferentes.

Foram encontrados 89 arquivos distintos por SHA-256. Após o agrupamento visual, restaram **78 imagens representativas**. A escolha de um subconjunto menor evita que cópias ou versões da mesma fotografia atravessem os grupos de treino e avaliação. Uma caixa de altura zero identificada na origem foi descartada durante a conferência das anotações. Os representantes selecionados contêm 459 caixas válidas no total.

A divisão usa ordem determinística e estratificação pela classe majoritária, preservando as duas classes em cada grupo. O mapa dos 177 arquivos para seus representantes e a divisão exata estão em `evidencias/preparacao_corrigida.json` e `evidencias/divisoes.csv`.

| Divisão | Imagens | Objetos anotados |
|---|---:|---:|
"""
    for split,count in splits.items():preparation+=f"| {split} | {count} | {objects[split]} |\n"
    preparation+='\nA conferência após a preparação não encontrou duplicações exatas nem pares com distância pHash ≤ 8 entre divisões. Esse critério não garante ausência de toda semelhança possível entre cenas. O teste em fotografias de outras fontes continua sendo uma melhoria recomendada.\n'
    if activity=='final':preparation+='\nAs 58 imagens de treino e 15 de validação somam **73 imagens anotadas**, acima do mínimo de 60. As **cinco imagens inéditas** foram reservadas antes do treinamento e não aparecem, nem por cópia ou pelo critério de similaridade aplicado, no treino ou na validação deste modelo.\n'
    folder='dataset/yolo' if activity=='2' else 'dataset/ready'
    preparation+=f"\n### Estrutura e configuração\n\n```text\n{folder}/\n├── images/train/\n├── images/val/\n"
    preparation+=('├── images/test/\n├── labels/train/\n├── labels/val/\n├── labels/test/\n' if activity=='2' else '├── labels/train/\n├── labels/val/\n├── unseen/images/\n├── unseen/labels_referencia/\n')
    preparation+='└── data.yaml\n```\n\n```yaml\n'+(project/folder/'data.yaml').read_text(encoding='utf-8')+'```\n'
    source_folder=project/folder/('images/test' if activity=='2' else 'unseen/images')
    label_folder=project/folder/('labels/test' if activity=='2' else 'unseen/labels_referencia')
    example=analysis['samples'][0]; annotation=(label_folder/(Path(example).stem+'.txt')).read_text(encoding='utf-8').strip()
    preparation+=f"\nExemplo de anotação correspondente a `{example}` (classe, centro X, centro Y, largura e altura normalizados):\n\n```text\n{annotation}\n```\n"
    training=f"""
## Treinamento e avaliação

Modelo: **YOLO26n** com pesos pré-treinados de origem; os pesos antigos treinados com a divisão inadequada não foram reutilizados. Foram executadas **20 épocas**, `imgsz={metrics['imgsz']}`, `batch=4`, `device=cpu`, `workers=0` e `seed={data['seed']}`. Ambiente: Windows 11, Python 3.12.10, Ultralytics 8.4.214 e PyTorch 2.15.0+cpu, em AMD Ryzen 5 5500U.

Os pesos do melhor checkpoint estão em `modelo/best.pt`. A seleção do checkpoint usou a validação; a divisão de teste/reserva não participou da atualização dos pesos nem da escolha do checkpoint.

**Validação:** {metric_line(metrics['val'])}
"""
    if activity=='2':training+='\n**Teste separado:** '+metric_line(metrics['test'])+f" O teste contém {splits['test']} imagens e {objects['test']} objetos anotados.\n"
    training+='\nPrecision mede a proporção de previsões corretas entre as detecções emitidas; Recall mede a fração dos objetos reais que o modelo encontrou. mAP50 é a média, entre classes, da área sob a curva de precisão e revocação com correspondência de caixas em IoU ≥ 0,50. mAP50-95 agrega vários limiares de IoU e exige localização mais rigorosa. Os valores do Ultralytics não são a mesma coisa que a contagem fixa de TP/FP/FN em `conf=0.25`.\n'
    training+=f"\n![Curvas do novo treinamento](runs/detect/resultados/{train}/results.png)\n"
    settings=['conf025','conf070'] if activity=='2' else ['imagens_ineditas']
    totals=analysis['totals']
    results='\n## Resultados nas imagens reservadas\n\n'
    results+='A comparação usa classe correta e IoU ≥ 0,50, com pareamento de uma previsão por objeto. Erros de classe aparecem como falso positivo e falso negativo; a coluna de erro de classe indica esse subconjunto, sem somá-lo novamente aos totais.\n\n'
    if activity=='2':
        a,b=totals['conf025'],totals['conf070']
        results+='| Configuração | Caixas previstas | TP | FP | FN | Erros de classe |\n|---|---:|---:|---:|---:|---:|\n'
        for setting,label in [('conf025','conf=0,25'),('conf070','conf=0,70')]:
            t=totals[setting];results+=f"| {label} | {t['pred']} | {t['tp']} | {t['fp']} | {t['fn']} | {t['erros_classe']} |\n"
        confidence=f"Ao elevar o limiar de 0,25 para 0,70, as caixas previstas passaram de {a['pred']} para {b['pred']}. Os verdadeiros positivos passaram de {a['tp']} para {b['tp']} e os falsos positivos de {a['fp']} para {b['fp']}; os falsos negativos passaram de {a['fn']} para {b['fn']}. Isso mostra a perda de detecções corretas e a redução de parte das detecções incorretas."
        results+='\n'+confidence+'\n\n### Cinco exemplos com referência e previsões\n\n'
        results+='| Imagem | TP / FP / FN em 0,25 | TP / FP / FN em 0,70 | Erros de classe em 0,25 / 0,70 |\n|---|---|---|---|\n'
    else:
        a=totals['imagens_ineditas']
        results+=f"Nas cinco imagens inéditas, há **{analysis['total_gt']} objetos anotados**. Em `conf=0.25`, o modelo retornou **{a['tp']} TP, {a['fp']} FP e {a['fn']} FN**, com {a['erros_classe']} erro(s) de classe identificado(s) no pareamento.\n\n"
        results+='| Imagem | Objetos de referência | TP | FP | FN | Erros de classe |\n|---|---:|---:|---:|---:|---:|\n'
    selected=[r for name in analysis['samples'] for r in analysis['records'] if r['imagem']==name]
    for row in selected:
        if activity=='2':
            x,y=row['conf025'],row['conf070'];results+=f"| {row['imagem']} | {x['tp']} / {x['fp']} / {x['fn']} | {y['tp']} / {y['fp']} / {y['fn']} | {x['erros_classe']} / {y['erros_classe']} |\n"
        else:
            x=row['imagens_ineditas'];results+=f"| {row['imagem']} | {row['gt']} | {x['tp']} | {x['fp']} | {x['fn']} | {x['erros_classe']} |\n"
    results+='\nCada painel apresenta a imagem original, as caixas da anotação de referência e as previsões do modelo.\n'
    for row in selected:results+=f"\n### {row['imagem']}\n\n![Original, referência e predições de {row['imagem']}](evidencias/comparacoes_visuais/{Path(row['imagem']).stem}.jpg)\n"
    if activity=='2':
        questions=f"""
## Respostas às sete questões

1. **Dataset escolhido:** conjunto público de tomates de Suman Kunwar no Kaggle, com 177 arquivos originais e anotações de detecção YOLO. Foram utilizadas 78 imagens representativas após remover cópias exatas e versões próximas. Classes: não maduro e maduro. A finalidade original é apoiar reconhecimento de maturação em aplicações agrícolas; licença CC BY-SA 4.0 e fonte indicadas na seção inicial.
2. **Bounding box e normalização:** uma caixa delimita a região ocupada pelo objeto. No YOLO, centro e dimensões são divididos pela largura/altura da imagem, gerando coordenadas de 0 a 1 independentes da resolução em pixels.
3. **Função de data.yaml:** define os caminhos de treino, validação e teste e o nome de cada ID de classe. Uma ordem incorreta associa caixas a nomes errados e pode produzir classes trocadas.
4. **Treinamento e inferência:** treinamento ajusta os pesos da rede usando exemplos anotados. Inferência aplica os pesos salvos a novas entradas, sem ajustá-los. O treino parte dos pesos pré-treinados e gera um checkpoint específico para as duas classes.
5. **Boa precisão com objetos omitidos:** sim. Precision alta indica poucos falsos positivos, mas Recall baixo indica muitos objetos reais sem detecção. Um limiar alto pode produzir exatamente essa combinação.
6. **Generalização:** acertar poucos exemplos não garante funcionamento em iluminação, fundo, escala e ângulo diferentes. Separar cenas semelhantes e usar dados independentes é necessário para avaliar essa capacidade. Mesmo corrigido, o teste de oito imagens é pequeno.
7. **Experimento de confiança:** {confidence} As tabelas, painéis e arquivos CSV registram as evidências.
"""
    else:
        questions=f"""
## Respostas às seis questões

1. **Problema escolhido:** localizar tomates e distinguir maduros e não maduros, como demonstração de visão computacional aplicada à agricultura.
2. **Imagens e classes:** dos 177 arquivos públicos originais, foram selecionadas 78 imagens após controle de duplicações. Foram usadas 58 para treino e 15 para validação, totalizando 73 imagens anotadas, além de cinco inéditas reservadas. Classes: `nao_maduro` e `maduro`; origem e licença indicadas no início.
3. **Modelo e épocas:** YOLO26n com pesos pré-treinados de origem, 20 épocas, resolução 640, lote 4 e CPU. O treinamento foi refeito após a correção dos dados.
4. **Métricas:** {metric_line(metrics['val'])} Precision mede acerto entre as detecções emitidas; Recall mede cobertura dos objetos anotados; mAP50 integra precisão e revocação por classe em IoU 0,50.
5. **Objetos nas imagens inéditas:** {analysis['total_gt']} objetos anotados, {a['tp']} correspondências corretas, {a['fp']} falsos positivos e {a['fn']} omissões em conf=0,25 e IoU ≥ 0,50. Os cinco painéis mostram os resultados e a tabela registra as falhas.
6. **Dificuldades e melhorias:** o dataset de origem tinha duplicações e uma caixa de altura zero; a preparação foi corrigida antes deste treino. A quantidade de cenas distintas e a reserva final são pequenas. Mais fotografias independentes e variadas, revisão de anotações e ajuste cuidadoso de resolução/épocas podem melhorar a cobertura e a localização.
"""
    end=f"""
## Conclusão e arquivos da entrega

A execução corrigida usa conjuntos separados pelos critérios de duplicação aplicados. As métricas anteriores, calculadas com vazamento de dados, foram substituídas pelos resultados apresentados neste relatório. O conjunto é pequeno e as métricas não garantem desempenho em qualquer ambiente; ainda são desejáveis exemplos de fontes e condições diferentes.

Os arquivos estão organizados na pasta da atividade:

- **Dados:** `{folder}/`, com imagens, anotações e `data.yaml`.
- **Modelo:** `modelo/best.pt`, obtido neste treinamento de 20 épocas.
- **Preparação e execução:** `prepare_dataset.py`, scripts compartilhados na pasta `scripts/` da raiz e `comandos.txt`.
- **Evidências:** `evidencias/preparacao_corrigida.json`, `metricas_corrigidas.json`, `resultados_treinamento.csv`, comparações CSV/JSON e os cinco painéis visuais.
- **Treinamento e detecções:** `runs/detect/resultados/`.

Os resultados foram gerados nas execuções registradas. As evidências incluem logs textuais, gráficos e imagens; não são capturas literais de tela do terminal.
"""
    (project/'relatorio.md').write_text(head+'\n'+preparation+training+results+questions+end,encoding='utf-8')
    cmds=f"""# Execução corrigida — PowerShell na raiz do repositório
# A preparação recebe a pasta detection extraída do dataset original.
python scripts/corrigir_dados.py {activity} CAMINHO_DA_PASTA_DETECTION
python scripts/conferir_entrega.py --atividade {activity} --somente-dados
python scripts/treinar_corrigido.py {activity}
python scripts/analisar_resultados.py {activity}
python scripts/registrar_divisoes.py

# Configuração efetiva: YOLO26n inicial, 20 épocas, imgsz={metrics['imgsz']}, batch=4, CPU, workers=0, seed={data['seed']}.
# Modelo entregue: {NAMES[activity]}/modelo/best.pt.
# Avaliação/novas inferências: python executar.py {activity} avaliar / inferir.
"""
    (project/'comandos.txt').write_text(cmds,encoding='utf-8')
    # Os nomes dos diretórios das figuras devem acompanhar os novos experimentos.
    path=project/'README.md'; text=path.read_text(encoding='utf-8')
    text=text.replace('treinamento1-2/','treinamento_corrigido/').replace('treino_final/','treino_final_corrigido/')
    text=text.replace('## Limitação da avaliação\n\nA auditoria encontrou imagens idênticas em divisões diferentes. Consulte [a conferência dos dados](../docs/CONFERENCIA.md) e [as correções necessárias](../docs/ESTADO_DA_ENTREGA.md) antes de interpretar as métricas como avaliação independente.',f"## Separação dos dados\n\nO dataset foi revisado antes deste novo treinamento: 78 imagens representativas, distribuídas em {splits}. A conferência não identificou sobreposições entre divisões pelos critérios SHA-256 e pHash aplicados. Consulte [a verificação](../docs/CONFERENCIA.md).")
    path.write_text(text,encoding='utf-8')
    print(project/'relatorio.md')


def main():
    p=argparse.ArgumentParser();p.add_argument('atividade',choices=['2','final','todas']);args=p.parse_args()
    for activity in (NAMES if args.atividade=='todas' else [args.atividade]):update(activity)


if __name__=='__main__':main()
