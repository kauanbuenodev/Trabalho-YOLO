"""Gera os PDFs a partir do Markdown usando Chrome headless no Windows."""
from pathlib import Path
import os
import subprocess
import tempfile
import shutil
import render_reports


def main():
    root = Path(__file__).resolve().parent.parent
    os.chdir(root)
    render_reports.main()
    chrome = Path(os.environ.get("PROGRAMFILES", "C:/Program Files")) / "Google/Chrome/Application/chrome.exe"
    if not chrome.is_file():
        raise SystemExit("Chrome não encontrado. Abra relatorio.html no navegador e use Imprimir > Salvar como PDF.")
    with tempfile.TemporaryDirectory(prefix="yolo_pdf_") as profile:
        for index, project in enumerate(render_reports.PROJECTS):
            source = (project / "relatorio.html").resolve()
            output = (project / "relatorio.pdf").resolve()
            result = subprocess.run([str(chrome), "--headless", "--disable-gpu", "--no-first-run", "--no-pdf-header-footer", f"--user-data-dir={profile}", f"--print-to-pdf={output}", source.as_uri()], capture_output=True, timeout=60)
            if result.returncode or not output.is_file():
                raise SystemExit(f"Falha ao exportar {project}: {result.stderr.decode(errors='replace')}")
            central_names = ["01_YOLO_Windows.pdf", "02_YOLO_Kaggle.pdf", "03_Projeto_Final_YOLO.pdf"]
            (root / "relatorios").mkdir(exist_ok=True)
            shutil.copy2(output, root / "relatorios" / central_names[index])
            print(f"{output.name}: {project} ({output.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
