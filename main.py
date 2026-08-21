import sys
from PyQt5.QtWidgets import QApplication
from app.ui.main_window import MainWindow
from app.ui.styles import APP_STYLESHEET
from app.utils.logger import setup_logger


def main():
    setup_logger()
    app = QApplication(sys.argv)
    app.setApplicationName("Visualizador de Documentos")
    app.setStyleSheet(APP_STYLESHEET)

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())  # PyQt5 usa exec_() (versão com underscore)


if __name__ == "__main__":
    main()
