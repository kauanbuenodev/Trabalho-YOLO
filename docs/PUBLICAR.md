# Publicar no repositório criado no GitHub

Repositório: https://github.com/kauanbuenodev/Trabalho-YOLO.

Após a primeira publicação, atualize com `git add .`, `git commit` e `git push`. O script `python scripts/exportar_pdfs.py` atualiza os PDFs nas pastas das atividades e sincroniza suas cópias em `relatorios/`. Execute `python scripts/gerar_inventario.py` depois das alterações para atualizar os hashes.

Esta pasta é a raiz que deve ser enviada. Ela já inclui as três atividades e o README inicial. Publique os arquivos dentro dela.

Com o Git instalado, abra um terminal nesta pasta. Substitua `URL_DO_REPOSITORIO` pelo endereço HTTPS do repositório criado:

```powershell
git init -b main
git add .
git commit -m "Adiciona tres atividades YOLO, relatorios e resultados"
git remote add origin URL_DO_REPOSITORIO
git push -u origin main
```

Estes comandos pressupõem um repositório remoto vazio. Se você tiver criado o remoto com um README ou outros arquivos, integre esse conteúdo antes do push. A autenticação será feita na sua conta GitHub.

Após publicar, abra o README pela página do GitHub e confira os links dos três relatórios. Se o repositório for privado, conceda acesso ao professor pela configuração de colaboradores.

A identificação já está preenchida: Kauan Reis Bueno, 8 Período, 17/11/2026. Se editar os arquivos `relatorio.md`, regenere HTML/PDF no Windows com Chrome instalado:

```powershell
python scripts/exportar_pdfs.py
python scripts/conferir_entrega.py
```

Depois atualize os arquivos no Git. Os modelos e dados anotados já estão incluídos; não precisa enviar ambientes virtuais ou o ZIP antigo junto.
