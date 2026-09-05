# SignDocs - Visualizador Universal de Documentos
aplicativo desktop em Python + PySide6, com suporte a PDF, DOCX, XLSX, PPTX, TXT e imagens (JPG/PNG)

<div align="center">

<img src="https://via.placeholder.com/1200x400/1a1a2e/eaeaea?text=SignDocs" alt="Capa do Projeto SignDocs" width="100%">

#  SignDocs

### Assinatura e gestão de documentos digitais de forma simples e segura.

<p>
    <img src="https://img.shields.io/badge/status-em%20desenvolvimento-yellow" alt="Status">
    <img src="https://img.shields.io/badge/license-MIT-blue" alt="Licença">
    <img src="https://img.shields.io/github/last-commit/PedroHenriqueM2005/SignDocs" alt="Last Commit">
</p>

</div>

---

## Sobre o Projeto

O **SignDocs** é uma solução desenvolvida para facilitar o processo de assinatura e validação de documentos digitais, eliminando a burocracia do papel e trazendo agilidade e segurança para o fluxo de aprovação de arquivos.

O objetivo principal é oferecer uma plataforma intuitiva onde usuários possam enviar, assinar e gerenciar documentos de forma centralizada.

##  Funcionalidades

-  Upload de documentos em formato PDF
-  Assinatura digital de arquivos
-  Gerenciamento de status (Pendente, Assinado, Rejeitado)
- Histórico de alterações


##  Estrutura do Projeto



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
