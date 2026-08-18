"""
Ponto de entrada da aplicação.
Responsável apenas por inicializar o Qt e exibir a janela principal.
"""
import sys
from PySide6.QtWidgets import QApplication

from ui.main_window import MainWindow


def main():
    app = QApplication(sys.argv)
    app.setApplicationName("Visualizador Universal de Documentos")

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()