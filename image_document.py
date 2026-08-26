from PyQt5.QtGui import QImage
from app.core.document import Document
from app.core.exceptions import CorruptedFileError


class ImageDocument(Document):
    """Documento de imagem única (jpg, png, bmp) tratado como 1 página."""

    def __init__(self, file_path: str):
        super().__init__(file_path)
        self._image = QImage(file_path)
        if self._image.isNull():
            raise CorruptedFileError("Não foi possível carregar a imagem.")

    def page_count(self) -> int:
        return 1

    def render_page(self, index: int, zoom: float = 1.0) -> QImage:
        if index != 0:
            raise IndexError("Esta imagem possui apenas 1 página.")
        return self._image

    def close(self):
        pass