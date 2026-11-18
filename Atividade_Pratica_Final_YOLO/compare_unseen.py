"""Compara as predições com as anotações de referência, IoU >= 0,50."""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from analisar_resultados import analyze
if __name__=='__main__':analyze('final',panels=False)
