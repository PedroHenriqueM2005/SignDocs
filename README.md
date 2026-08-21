# SignDocs - Visualizador Universal de Documentos
aplicativo desktop em Python + PySide6, com suporte a PDF, DOCX, XLSX, PPTX, TXT e imagens (JPG/PNG)

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![PySide6](https://img.shields.io/badge/UI-PySide6-green)
![License](https://img.shields.io/badge/license-MIT-lightgrey)

## Funcionalidades

-  **Múltiplos documentos abertos simultaneamente**
-  **Prévia minimalista** (thumbnail + metadados) de cada documento ao selecioná-lo
-  **Navegação por páginas** com botões Anterior/Próxima e campo "Ir para página"
-  **Histórico de arquivos recentes** persistido em banco de dados SQLite
-    Interface limpa e moderna construída com **PySide6 (Qt)**
-    **ON HOLD** Opção de assinar documentos ultilizando-se uma assinatura pré definida pelo usuario. (em desenvolvimento)

## Instalação

Pré-requisitos

- Python **3.10 ou superior**


### Passo a passo

# Crie um ambiente virtual

python -m venv venv

# Ative o ambiente virtual

# Windows:

venv\Scripts\activate

# Linux/macOS:

source venv/bin/activate

# Instale as dependências

pip install -r requirements.txt

O projeto usa pytest para testes automatizados.

# Execute todos os testes

python -m pytest -v

# Execute um arquivo de teste específico

python -m pytest tests/test_document_factory.py -v

# Execute com relatório de cobertura (requer pytest-cov)

pip install pytest-cov

python -m pytest --cov=. --cov-report=term-missing


## TEC. usadas

Python 3.10+ — linguagem principal

PySide6 — interface gráfica (Qt para Python)

PyMuPDF (fitz) — renderização de PDFs

## Autor Pedro Henrique Martins

Desenvolvido como projeto de estudo/portfólio.

python-docx — leitura de arquivos Word

openpyxl — leitura de planilhas Excel

python-pptx — leitura de apresentações PowerPoint

SQLite — persistência do histórico de arquivos recentes

pytest — testes automatizados
