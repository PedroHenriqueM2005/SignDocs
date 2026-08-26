from abc import ABC, abstractmethod
from PyQt5.QtGui import QImage


class Document(ABC):
    """
    Interface comum que todos os tipos de documento devem implementar.
    Isso permite que a interface (ViewerPanel) trate PDF, Word, Excel,
    PowerPoint, TXT e imagens exatamente da mesma forma.
    """

    def __init__(self, file_path: str):
        self.file_path = file_path

    @abstractmethod
    def page_count(self) -> int:
        """Retorna o número total de páginas do documento."""

    @abstractmethod
    def render_page(self, index: int, zoom: float = 1.0) -> QImage:
        """Renderiza a página `index` (0-based) como QImage."""

    @abstractmethod
    def close(self):
        """Libera recursos (handles de arquivo, etc.)."""