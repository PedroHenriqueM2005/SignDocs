import os
import logging
from PyQt5.QtWidgets import QMainWindow, QSplitter, QFileDialog, QMessageBox, QMenu, QStatusBar
from PyQt5.QtCore import Qt
from app.config import APP_NAME, SUPPORTED_EXTENSIONS
from app.database.db_manager import DBManager
from app.ui.sidebar import Sidebar
from app.ui.viewer_panel import ViewerPanel
from app.ui.thumbnail_worker import DocumentLoaderWorker

logger = logging.getLogger(__name__)


class MainWindow(QMainWindow):
    """Janela principal: orquestra menu, barra lateral, painel de visualização e banco."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle(APP_NAME)
        self.resize(1200, 800)

        self.db = DBManager()
        self._documents = {}   # file_path -> instância de Document
        self._page_memory = {}  # file_path -> última página vista
        self._workers = []      # referências ativas de threads em execução

        self._build_ui()
        self._build_menu()

    # ---------- Construção da interface ----------

    def _build_ui(self):
        splitter = QSplitter(Qt.Horizontal)

        self.sidebar = Sidebar()
        self.sidebar.setMinimumWidth(260)
        self.sidebar.setMaximumWidth(340)
        self.sidebar.document_selected.connect(self._on_document_selected)
        self.sidebar.document_closed.connect(self._on_document_closed)

        self.viewer = ViewerPanel()

        splitter.addWidget(self.sidebar)
        splitter.addWidget(self.viewer)
        splitter.setStretchFactor(1, 1)
        self.setCentralWidget(splitter)

        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

    def _build_menu(self):
        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu("Arquivo")

        open_action = file_menu.addAction("Abrir documento(s)...")
        open_action.setShortcut("Ctrl+O")
        open_action.triggered.connect(self.open_files_dialog)

        self.recent_menu = QMenu("Arquivos recentes", self)
        file_menu.addMenu(self.recent_menu)
        self._refresh_recent_menu()

        close_all_action = file_menu.addAction("Fechar todos")
        close_all_action.triggered.connect(self.close_all_documents)

        exit_action = file_menu.addAction("Sair")
        exit_action.triggered.connect(self.close)

        help_menu = menu_bar.addMenu("Ajuda")
        about_action = help_menu.addAction("Sobre")
        about_action.triggered.connect(self._show_about)

    def _show_about(self):
        QMessageBox.information(self, "Sobre", f"{APP_NAME}\nVisualizador multi-formato de documentos.")

    def _refresh_recent_menu(self):
        self.recent_menu.clear()
        recents = self.db.get_recent_files()
        if not recents:
            action = self.recent_menu.addAction("(vazio)")
            action.setEnabled(False)
            return
        for path, name, _doc_type, _page_count, _last_opened in recents:
            action = self.recent_menu.addAction(name)
            action.triggered.connect(lambda checked=False, p=path: self._open_single_file(p))

    # ---------- Abertura de arquivos ----------

    def open_files_dialog(self):
        """Abre o seletor de arquivos permitindo seleção múltipla."""
        extensions = " ".join(f"*{ext}" for ext in SUPPORTED_EXTENSIONS.keys())
        filter_str = f"Documentos suportados ({extensions});;Todos os arquivos (*)"
        paths, _ = QFileDialog.getOpenFileNames(self, "Selecionar documento(s)", "", filter_str)
        for path in paths:
            self._open_single_file(path)

    def _open_single_file(self, path: str):
        # ---- validação de entrada ----
        if not path or not os.path.isfile(path):
            QMessageBox.warning(self, "Arquivo inválido", f"Arquivo não encontrado:\n{path}")
            return

        ext = os.path.splitext(path)[1].lower()
        if ext not in SUPPORTED_EXTENSIONS:
            QMessageBox.warning(self, "Formato não suportado", f"O formato '{ext}' não é suportado.")
            return

        if path in self._documents:
            self.sidebar.setCurrentRow(self.sidebar.index_of(path))
            return

        self.status_bar.showMessage(f"Carregando {os.path.basename(path)}...")
        worker = DocumentLoaderWorker(path)
        worker.loaded.connect(self._on_document_loaded)
        worker.failed.connect(self._on_document_failed)
        worker.finished.connect(lambda: self._cleanup_worker(worker))
        self._workers.append(worker)
        worker.start()

    def _cleanup_worker(self, worker):
        if worker in self._workers:
            self._workers.remove(worker)

    # ---------- Callbacks do worker ----------

    def _on_document_loaded(self, path, document, pixmap, metadata):
        self._documents[path] = document
        self.sidebar.add_document_item(path, pixmap, metadata)
        self.status_bar.showMessage(f"{metadata['name']} carregado com sucesso.", 5000)
        try:
            self.db.add_or_update_recent(path, metadata["name"], metadata["extension"], metadata["page_count"])
        except Exception as e:
            logger.warning(f"Falha ao salvar histórico: {e}")
        self._refresh_recent_menu()

    def _on_document_failed(self, path, error_message):
        self.status_bar.showMessage("Falha ao carregar documento.", 5000)
        QMessageBox.critical(self, "Erro ao abrir documento",
                              f"Não foi possível abrir:\n{path}\n\nDetalhes: {error_message}")

    # ---------- Interações da lista ----------

    def _on_document_selected(self, path):
        document = self._documents.get(path)
        if document:
            start_page = self._page_memory.get(path, 0)
            self.viewer.show_document(document, start_page)

    def _on_document_closed(self, path):
        # guarda a última página vista antes de fechar, caso reabra depois
        self._page_memory[path] = self.viewer.current_page()
        document = self._documents.pop(path, None)
        if document:
            document.close()
        self.sidebar.remove_document_item(path)
        if self.sidebar.count() == 0:
            self.viewer.clear()

    def close_all_documents(self):
        for path in list(self._documents.keys()):
            self._on_document_closed(path)

    def closeEvent(self, event):
        for document in self._documents.values():
            try:
                document.close()
            except Exception:
                pass
        event.accept()