import os

APP_NAME = "Visualizador de Documentos"
APP_VERSION = "1.0.0"

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CACHE_DIR = os.path.join(BASE_DIR, ".cache")       # PDFs convertidos de Office
DB_PATH = os.path.join(BASE_DIR, "app_data.db")    # histórico de arquivos recentes

os.makedirs(CACHE_DIR, exist_ok=True)

# Mapeia extensão -> categoria de tratamento
SUPPORTED_EXTENSIONS = {
    ".pdf": "pdf",
    ".docx": "office",
    ".doc": "office",
    ".xlsx": "office",
    ".xls": "office",
    ".pptx": "office",
    ".ppt": "office",
    ".txt": "text",
    ".jpg": "image",
    ".jpeg": "image",
    ".png": "image",
    ".bmp": "image",
}

RENDER_ZOOM = 2.0            # fator de zoom para renderização em alta resolução
THUMBNAIL_SIZE = (120, 160)  # tamanho da miniatura na barra lateral
PAGE_CANVAS_SIZE = (827, 1169)  # tamanho aproximado de página A4 (para paginar .txt)
MAX_RECENT_FILES = 15