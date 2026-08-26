import fitz  # PyMuPDF
from PyQt5.QtGui import QImage
from app.core.document import Document
from app.core.exceptions import CorruptedFileError


class PDFDocument(Document):
    """Documento PDF renderizado nativamente com PyMuPDF."""

    def __init__(self, file_path: str):
        super().__init__(file_path)
        try:
            self._doc = fitz.open(file_path)
            if self._doc.page_count == 0:
                raise CorruptedFileError("PDF sem páginas.")
        except Exception as e:
            raise CorruptedFileError(f"Não foi possível abrir o PDF: {e}")

    def page_count(self) -> int:
        return self._doc.page_count

    def render_page(self, index: int, zoom: float = 2.0) -> QImage:
        if index < 0 or index >= self.page_count():
            raise IndexError("Página fora do intervalo.")
        page = self._doc.load_page(index)
        mat = fitz.Matrix(zoom, zoom)
        pix = page.get_pixmap(matrix=mat, alpha=False)
        image = QImage(pix.samples, pix.width, pix.height, pix.stride, QImage.Format_RGB888)
        # .copy() é essencial: o buffer de `pix` pode ser liberado após a função retornar
        return image.copy()

    def close(self):
        self._doc.close()