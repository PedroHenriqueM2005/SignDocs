from PyQt5.QtWidgets import (QWidget, QListWidget, QListWidgetItem, QHBoxLayout,
                               QVBoxLayout, QLabel, QPushButton)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QPixmap


class DocumentItemWidget(QWidget):
    """Widget customizado de cada item: miniatura + nome + tamanho + nº páginas + fechar."""

    close_requested = pyqtSignal(str)

    def __init__(self, file_path: str, pixmap: QPixmap, metadata: dict, parent=None):
        super().__init__(parent)
        self.file_path = file_path

        layout = QHBoxLayout(self)
        layout.setContentsMargins(6, 6, 6, 6)

        thumb_label = QLabel()
        thumb_label.setPixmap(pixmap)
        thumb_label.setFixedSize(pixmap.size())
        thumb_label.setStyleSheet("border: 1px solid #ccc; background:#fff;")
        layout.addWidget(thumb_label)

        info_layout = QVBoxLayout()
        name_label = QLabel(metadata["name"])
        name_label.setStyleSheet("font-weight: bold;")
        name_label.setWordWrap(True)
        info_label = QLabel(f"{metadata['size_formatted']} • {metadata['page_count']} pág.")
        info_label.setStyleSheet("color: #666; font-size: 11px;")
        info_layout.addWidget(name_label)
        info_layout.addWidget(info_label)
        info_layout.addStretch()
        layout.addLayout(info_layout)
        layout.addStretch()

        close_btn = QPushButton("✕")
        close_btn.setFixedSize(22, 22)
        close_btn.setToolTip("Fechar documento")
        close_btn.setStyleSheet(
            "QPushButton { background: none; border: none; color: #999; }"
            "QPushButton:hover { color: #d33; }"
        )
        close_btn.clicked.connect(lambda: self.close_requested.emit(self.file_path))
        layout.addWidget(close_btn, alignment=Qt.AlignTop)


class Sidebar(QListWidget):
    """Lista lateral com todos os documentos abertos na sessão atual."""

    document_selected = pyqtSignal(str)
    document_closed = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setSpacing(4)
        self.setStyleSheet("""
            QListWidget { background: #f7f7f9; border: none; }
            QListWidget::item:selected { background: #dbe9ff; border-radius: 6px; }
        """)
        self.currentItemChanged.connect(self._on_selection_changed)

    def add_document_item(self, file_path: str, pixmap: QPixmap, metadata: dict):
        item = QListWidgetItem()
        widget = DocumentItemWidget(file_path, pixmap, metadata)
        widget.close_requested.connect(self.document_closed.emit)
        item.setData(Qt.UserRole, file_path)
        item.setSizeHint(widget.sizeHint())
        self.addItem(item)
        self.setItemWidget(item, widget)
        self.setCurrentItem(item)

    def remove_document_item(self, file_path: str):
        for i in range(self.count()):
            if self.item(i).data(Qt.UserRole) == file_path:
                self.takeItem(i)
                break

    def index_of(self, file_path: str) -> int:
        for i in range(self.count()):
            if self.item(i).data(Qt.UserRole) == file_path:
                return i
        return -1

    def _on_selection_changed(self, current, _previous):
        if current:
            self.document_selected.emit(current.data(Qt.UserRole))