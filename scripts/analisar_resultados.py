"""Compara caixas, registra erros e monta painéis com referência e predição."""
from pathlib import Path
import csv
import json
import argparse

ROOT = Path(__file__).resolve().parent.parent


def boxes(path, predicted=False):
    if not path.exists(): return []
    return [(int(a[0]),list(map(float,a[1:5])),float(a[5]) if predicted else 1.) for a in (line.split() for line in path.read_text(encoding="utf-8").splitlines())]


def iou(a,b):
    ax,ay,aw,ah=a; bx,by,bw,bh=b
    area=max(0,min(ax+aw/2,bx+bw/2)-max(ax-aw/2,bx-bw/2))*max(0,min(ay+ah/2,by+bh/2)-max(ay-ah/2,by-bh/2))
    union=aw*ah+bw*bh-area
    return area/union if union else 0.


def score(gt,pred):
    remaining=set(range(len(gt))); unmatched=[]; tp=0
    for cls,box,confidence in sorted(pred,key=lambda x:x[2],reverse=True):
        best=max([(iou(box,gt[i][1]),i) for i in remaining if gt[i][0]==cls],default=(0.,-1))
        if best[0]>=.5:
            tp+=1; remaining.remove(best[1])
        else: unmatched.append((cls,box,confidence))
    class_errors=0; wrong_class_candidates=set(remaining)
    for cls,box,_ in unmatched:
        best=max([(iou(box,gt[i][1]),i) for i in wrong_class_candidates if gt[i][0]!=cls],default=(0.,-1))
        if best[0]>=.5:
            class_errors+=1; wrong_class_candidates.remove(best[1])
    return {"tp":tp,"fp":len(unmatched),"fn":len(remaining),"erros_classe":class_errors,"pred":len(pred)}


def analyze(activity, panels=True):
    project=ROOT/("Atividade_Pratica_II_YOLO_Kaggle" if activity=="2" else "Atividade_Pratica_Final_YOLO")
    data=project/("dataset/yolo" if activity=="2" else "dataset/ready")
    images=data/("images/test" if activity=="2" else "unseen/images")
    labels=data/("labels/test" if activity=="2" else "unseen/labels_referencia")
    results=project/"runs/detect/resultados"
    settings=["conf025","conf070"] if activity=="2" else ["imagens_ineditas"]
    records=[]
    for image in sorted(images.iterdir()):
        gt=boxes(labels/(image.stem+".txt"))
        row={"imagem":image.name,"gt":len(gt),"classes":sorted({x[0] for x in gt})}
        for setting in settings:
            row[setting]=score(gt,boxes(results/setting/"labels"/(image.stem+".txt"),True))
        records.append(row)
    totals={s:{k:sum(r[s][k] for r in records) for k in ["tp","fp","fn","erros_classe","pred"]} for s in settings}
    total_gt=sum(r["gt"] for r in records)
    if activity=="2":
        chosen=[]
        for cls in [0,1]:
            choices=sorted((r for r in records if cls in r['classes']),key=lambda r:(r['conf025']['fp']+r['conf025']['fn'],r['imagem']))
            if choices and choices[0] not in chosen: chosen.append(choices[0])
        for row in sorted(records,key=lambda r:(-(r['conf025']['fp']+r['conf025']['fn']+r['conf070']['fn']),r['imagem'])):
            if row not in chosen: chosen.append(row)
            if len(chosen)==5:break
    else: chosen=records
    record={"activity":activity,"total_gt":total_gt,"images":len(records),"totals":totals,"records":records,"samples":[r['imagem'] for r in chosen],"iou":.5}
    evidence=project/"evidencias"
    (evidence/"comparacao_corrigida.json").write_text(json.dumps(record,indent=2,ensure_ascii=False),encoding='utf-8')
    csv_path=evidence/("comparacao_confianca.csv" if activity=="2" else "comparacao_ineditas.csv")
    with csv_path.open('w',encoding='utf-8',newline='') as f:
        writer=csv.writer(f); writer.writerow(['imagem','gt']+[f'{s}_{k}' for s in settings for k in ['pred','tp','fp','fn','erros_classe']])
        for r in records:writer.writerow([r['imagem'],r['gt']]+[r[s][k] for s in settings for k in ['pred','tp','fp','fn','erros_classe']])
        writer.writerow(['TOTAL',total_gt]+[totals[s][k] for s in settings for k in ['pred','tp','fp','fn','erros_classe']])
    if panels:
        from PIL import Image,ImageDraw,ImageFont,ImageOps
        try: font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',18)
        except OSError:font=ImageFont.load_default()
        target=evidence/"comparacoes_visuais"; target.mkdir(exist_ok=True)
        for row in chosen:
            source=Image.open(images/row['imagem']).convert('RGB')
            ref=source.copy(); draw=ImageDraw.Draw(ref)
            w,h=ref.size
            try: ref_font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',max(18,round(w/45)))
            except OSError: ref_font=font
            for cls,(cx,cy,bw,bh),_ in boxes(labels/(Path(row['imagem']).stem+'.txt')):
                color='#138a36' if cls==0 else '#e75b14'
                x1,y1=(cx-bw/2)*w,(cy-bh/2)*h; x2,y2=(cx+bw/2)*w,(cy+bh/2)*h
                draw.rectangle((x1,y1,x2,y2),outline=color,width=max(2,round(w/250)))
                draw.text((x1,max(0,y1-getattr(ref_font,'size',18)-4)),['nao_maduro','maduro'][cls],fill=color,font=ref_font)
            tiles=[('Original',source),('Anotacao de referencia',ref)]
            for setting in settings:
                prediction=results/setting/(Path(row['imagem']).stem+'.jpg')
                tiles.append((('Predicao conf=0.25' if setting in ['conf025','imagens_ineditas'] else 'Predicao conf=0.70'),Image.open(prediction).convert('RGB')))
            sheet=Image.new('RGB',(480*len(tiles),430),'white'); canvas=ImageDraw.Draw(sheet)
            for i,(title,tile) in enumerate(tiles):
                tile=ImageOps.contain(tile,(470,360)); sheet.paste(tile,(i*480+(480-tile.width)//2,45+(360-tile.height)//2)); canvas.text((i*480+12,12),title,fill='black',font=font)
            canvas.text((12,407),row['imagem'],fill='black',font=font)
            sheet.save(target/(Path(row['imagem']).stem+'.jpg'),quality=90)
    print(json.dumps({k:v for k,v in record.items() if k!='records'},indent=2,ensure_ascii=False))
    return record


def main():
    p=argparse.ArgumentParser(); p.add_argument('atividade',choices=['2','final']); p.add_argument('--sem-paineis',action='store_true'); args=p.parse_args()
    analyze(args.atividade,panels=not args.sem_paineis)


if __name__=='__main__':main()
