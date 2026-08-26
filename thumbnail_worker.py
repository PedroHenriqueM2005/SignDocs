import logging
from PyQt5.QtCore import QThread, pyqtSignal, Qt
from PyQt5.QtGui import QPixmap
from app.core.document_loader import load_document
from app.utils.file_utils import get_file_metadata
from app.config import THUMBNAIL_SIZE

logger = logging.getLogger(__name__)


class DocumentLoaderWorker(QThread):
    """
    Carrega o documento e gera a miniatura em uma thread separada.
    """
    loaded = pyqtSignal(str, object, object, dict)   # path, document, pixmap, metadata
    failed = pyqtSignal(str, str)                    # path, mensagem de erro

    def __init__(self, file_path: str):
        super().__init__()
        self.file_path = file_path

    def run(self):
        try:
            document = load_document(self.file_path)
            image = document.render_page(0, zoom=1.0)
            pixmap = QPixmap.fromImage(image).scaled(
                THUMBNAIL_SIZE[0], THUMBNAIL_SIZE[1],
                Qt.KeepAspectRatio, Qt.SmoothTransformation
            )
            metadata = get_file_metadata(self.file_path)
            metadata["page_count"] = document.page_count()
            self.loaded.emit(self.file_path, document, pixmap, metadata)
        except Exception as e:
            logger.exception(f"Erro ao carregar documento: {self.file_path}")
            self.failed.emit(self.file_path, str(e))