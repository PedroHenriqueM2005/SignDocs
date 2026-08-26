from PyQt5.QtGui import QImage, QPainter, QTextDocument
from PyQt5.QtCore import QSizeF, Qt
from app.core.document import Document
from app.core.exceptions import CorruptedFileError
from app.config import PAGE_CANVAS_SIZE


class TextDocument(Document):
    """
    Arquivos .txt não têm páginas nativas. Usamos QTextDocument do Qt,
    que calcula automaticamente a quebra de páginas quando definimos
    um tamanho fixo de página (setPageSize).
    """

    def __init__(self, file_path: str):
        super().__init__(file_path)
        try:
            with open(file_path, "r", encoding="utf-8", errors="replace") as f:
                content = f.read()
        except Exception as e:
            raise CorruptedFileError(f"Não foi possível ler o arquivo de texto: {e}")

        self._qtdoc = QTextDocument()
        self._qtdoc.setPlainText(content)
        w, h = PAGE_CANVAS_SIZE
        self._qtdoc.setPageSize(QSizeF(w, h))

    def page_count(self) -> int:
        return max(1, self._qtdoc.pageCount())

    def render_page(self, index: int, zoom: float = 1.0) -> QImage:
        if index < 0 or index >= self.page_count():
            raise IndexError("Página fora do intervalo.")

        w, h = PAGE_CANVAS_SIZE
        image = QImage(int(w * zoom), int(h * zoom), QImage.Format_RGB32)
        image.fill(Qt.white)

        painter = QPainter(image)
        painter.scale(zoom, zoom)
        # Desloca o conteúdo para que a página `index` fique visível na área [0, h]
        painter.translate(0, -index * h)
        self._qtdoc.drawContents(painter)
        painter.end()
        return image

    def close(self):
        pass