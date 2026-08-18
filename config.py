"""
Configurações globais da aplicação.
Centraliza constantes usadas em todo o projeto para facilitar manutenção.
"""
from pathlib import Path

APP_NAME = "Visualizador Universal de Documentos"
APP_VERSION = "1.0.0"

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = str(BASE_DIR / "data" / "app_data.db")

# Tamanho da janela principal
WINDOW_DEFAULT_SIZE = (1200, 750)
WINDOW_MIN_SIZE = (900, 600)

# Tamanho padrão dos thumbnails na barra lateral (largura, altura)
THUMBNAIL_SIZE = (70, 90)

# Número de linhas por "página virtual" para formatos sem paginação nativa (TXT/DOCX)
LINES_PER_PAGE_TEXT = 40

# Limite de tamanho de arquivo em MB (proteção contra arquivos corrompidos/enormes)
MAX_FILE_SIZE_MB = 200

# Extensões conhecidas pela aplicação (usadas no filtro do diálogo de abertura).
# Note que .doc, .xls e .ppt aparecem aqui apenas para o usuário poder selecioná-los
# no explorador de arquivos — o factory bloqueia esses formatos legados com uma
# mensagem explicativa, pois exigem bibliotecas adicionais não incluídas.
SUPPORTED_EXTENSIONS = {
    "pdf", "docx", "doc", "xlsx", "xls", "pptx", "ppt", "txt", "jpg", "jpeg", "png"
}

FILE_DIALOG_EXTENSIONS = sorted(SUPPORTED_EXTENSIONS)