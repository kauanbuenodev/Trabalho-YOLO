"""Confere arquivos, anotações e separação por SHA-256 e pHash."""
from pathlib import Path
import argparse, hashlib, json, re
ROOT=Path(__file__).resolve().parent.parent
PROJECTS={'1':('Atividade_Pratica_YOLO_Windows','datasets/coco8'),'2':('Atividade_Pratica_II_YOLO_Kaggle','dataset/yolo'),'final':('Atividade_Pratica_Final_YOLO','dataset/ready')}

def check(activity,figures=True):
    name,folder=PROJECTS[activity]; project=ROOT/name; data=project/folder
    errors=[]; counts={}; hashes={}; phashes={}; minimum=None
    info=None if activity=='1' else json.loads((project/'evidencias/preparacao_corrigida.json').read_text(encoding='utf-8'))
    expected={'train':4,'val':4} if info is None else info['splits']
    lookup={} if info is None else {r['original']:int(r['phash'],2) for r in info['groups']}
    for split,count in expected.items():
        images=data/('unseen/images' if split=='ineditas' else f'images/{split}')
        labels=data/('unseen/labels_referencia' if split=='ineditas' else f'labels/{split}')
        files=sorted(p for p in images.iterdir() if p.suffix.lower() in {'.jpg','.jpeg','.png'})
        counts[split]=len(files); classes=set()
        if count!=len(files):errors.append(f'{split}: quantidade inesperada')
        for image in files:
            digest=hashlib.sha256(image.read_bytes()).hexdigest()
            if digest in hashes:errors.append(f'Imagem duplicada: {image.name}')
            hashes[digest]=(split,image.name)
            if info:
                record=next((r for r in info['manifest'] if r['imagem']==image.name and r['divisao']==split),None)
                if not record or record['sha256']!=digest:errors.append(f'Imagem diverge do manifesto: {image.name}')
                phashes[image.name]=(split,lookup[image.name])
            label=labels/(image.stem+'.txt')
            if not label.is_file():errors.append(f'Anotação ausente: {image.name}');continue
            for line in label.read_text(encoding='utf-8').splitlines():
                values=line.split()
                if len(values)!=5:errors.append(f'Formato inválido: {label.name}');continue
                classes.add(int(values[0]))
                if any(not 0<=float(v)<=1 for v in values[1:]) or float(values[3])<=0 or float(values[4])<=0:errors.append(f'Caixa inválida: {label.name}')
        if info and classes!={0,1}:errors.append(f'Classes ausentes em {split}')
    pairs=list(phashes.items())
    for i,(aname,(asplit,ahash)) in enumerate(pairs):
        for bname,(bsplit,bhash) in pairs[:i]:
            if asplit==bsplit:continue
            distance=(ahash^bhash).bit_count()
            minimum=distance if minimum is None else min(minimum,distance)
            if distance<=8:errors.append(f'Similaridade entre divisões: {aname} / {bname}')
    if figures:
        for target in re.findall(r'!\[[^\]]*\]\(([^)]+)\)',(project/'relatorio.md').read_text(encoding='utf-8')):
            if not(project/target).is_file():errors.append(f'Figura ausente: {target}')
        for target in ['relatorio.pdf','enunciado.pdf','modelo/best.pt','modelo/yolo26n.pt']:
            if not(project/target).is_file():errors.append(f'Arquivo ausente: {target}')
    return {'activity':activity,'splits':counts,'unique_sha256':len(hashes),'min_phash_cross_split':minimum,'errors':errors}

def main():
    p=argparse.ArgumentParser();p.add_argument('--atividade',choices=PROJECTS);p.add_argument('--somente-dados',action='store_true');args=p.parse_args()
    records=[check(a,not args.somente_dados) for a in ([args.atividade] if args.atividade else PROJECTS)]
    if not args.atividade:
        lines=['# Conferência da entrega corrigida','','A divisão foi refeita antes dos novos treinamentos. Foram conferidos pares imagem/anotação, classes, caixas, integridade SHA-256 e distância de pHash entre divisões.','','| Atividade | Divisões | Imagens distintas | Menor distância pHash entre divisões | Problemas |','|---|---|---:|---:|---:|']
        for r in records:
            splits='; '.join(f'{k}: {v}' for k,v in r['splits'].items())
            distance=r['min_phash_cross_split'] if r['min_phash_cross_split'] is not None else 'não aplicado'
            lines.append(f"| {r['activity']} | {splits} | {r['unique_sha256']} | {distance} | {len(r['errors'])} |")
        lines+=['','O critério conservador de similaridade agrupa pHash com distância de Hamming ≤ 8. Quando a coluna Problemas é zero, não há sobreposições pelos critérios aplicados. Essa checagem não prova independência de todas as cenas possíveis; recomenda-se também avaliar fotos externas ao dataset.','','Os mapas de exclusão e manifestos completos estão em evidencias/preparacao_corrigida.json de cada atividade. Os resultados antigos com vazamento foram substituídos após os novos treinamentos.']
        for r in records:lines.extend('- '+e for e in r['errors'])
        (ROOT/'docs/CONFERENCIA.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    print(json.dumps(records,ensure_ascii=False,indent=2))
    raise SystemExit(1 if any(r['errors'] for r in records) else 0)
if __name__=='__main__':main()
