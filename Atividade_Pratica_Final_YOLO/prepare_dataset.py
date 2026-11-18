"""Prepara os dados com controle de duplicações antes dos splits."""
from pathlib import Path
import argparse, sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from corrigir_dados import prepare
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('source',type=Path);p.add_argument('--output',type=Path,default=Path('dataset/ready'));args=p.parse_args()
    prepare(args.source,args.output,'final')
