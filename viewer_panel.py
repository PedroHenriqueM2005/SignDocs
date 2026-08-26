from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
                               QScrollArea, QLineEdit, QMessageBox)
from PyQt5.QtGui import QPixmap, QIntValidator
from PyQt5.QtCore import Qt
from app.config import RENDER_ZOOM


class ViewerPanel(QWidget):
    """
    Painel central único que exibe a página atual do documento selecionado
    e permite navegar entre páginas (◀ Anterior / Próxima ▶ / ir para página).
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self._document = None
        self._current_page = 0

        main_layout = QVBoxLayout(self)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setAlignment(Qt.AlignCenter)
        self.scroll_area.setStyleSheet("background:#e9e9ec; border:none;")

        self.page_label = QLabel("Selecione um documento na lista à esquerda.")
        self.page_label.setAlignment(Qt.AlignCenter)
        self.page_label.setStyleSheet("color:#555; font-size:14px;")
        self.scroll_area.setWidget(self.page_label)

        main_layout.addWidget(self.scroll_area, stretch=1)

        nav_bar = QHBoxLayout()
        self.btn_prev = QPushButton("◀ Anterior")
        self.btn_next = QPushButton("Próxima ▶")
        self.page_input = QLineEdit()
        self.page_input.setFixedWidth(50)
        self.page_input.setAlignment(Qt.AlignCenter)
        self.page_input.setValidator(QIntValidator(1, 999999))
        self.page_total_label = QLabel("/ 0")

        self.btn_prev.clicked.connect(self.go_previous)
        self.btn_next.clicked.connect(self.go_next)
        self.page_input.returnPressed.connect(self._go_to_typed_page)

        nav_bar.addStretch()
        nav_bar.addWidget(self.btn_prev)
        nav_bar.addWidget(QLabel("Página"))
        nav_bar.addWidget(self.page_input)
        nav_bar.addWidget(self.page_total_label)
        nav_bar.addWidget(self.btn_next)
        nav_bar.addStretch()

        main_layout.addLayout(nav_bar)
        self._update_nav_state()

    def show_document(self, document, start_page: int = 0):
        """Exibe um documento a partir da página informada (padrão: primeira)."""
        self._document = document
        self._current_page = min(max(0, start_page), document.page_count() - 1)
        self._render_current_page()

    def clear(self):
        self._document = None
        self._current_page = 0
        self.page_label.setPixmap(QPixmap())
        self.page_label.setText("Selecione um documento na lista à esquerda.")
        self._update_nav_state()

    def current_page(self) -> int:
        return self._current_page

    def go_previous(self):
        if self._document and self._current_page > 0:
            self._current_page -= 1
            self._render_current_page()

    def go_next(self):
        if self._document and self._current_page < self._document.page_count() - 1:
            self._current_page += 1
            self._render_current_page()

    def _go_to_typed_page(self):
        if not self._document:
            return
        try:
            target = int(self.page_input.text()) - 1
        except ValueError:
            return

        total = self._document.page_count()
        if target < 0 or target >= total:
            QMessageBox.warning(self, "Página inválida", f"Informe um número entre 1 e {total}.")
            self.page_input.setText(str(self._current_page + 1))
            return

        self._current_page = target
        self._render_current_page()

    def _render_current_page(self):
        try:
            image = self._document.render_page(self._current_page, zoom=RENDER_ZOOM)
            pixmap = QPixmap.fromImage(image)
            self.page_label.setPixmap(pixmap)
            self.page_label.resize(pixmap.size())
        except Exception as e:
            QMessageBox.critical(self, "Erro ao renderizar página", str(e))
        self._update_nav_state()

    def _update_nav_state(self):
        has_doc = self._document is not None
        total = self._document.page_count() if has_doc else 0
        self.btn_prev.setEnabled(has_doc and self._current_page > 0)
        self.btn_next.setEnabled(has_doc and self._current_page < total - 1)
        self.page_input.setEnabled(has_doc)
        self.page_input.setText(str(self._current_page + 1) if has_doc else "")
        self.page_total_label.setText(f"/ {total}")