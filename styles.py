"""Folha de estilos (QSS) global — dá uma aparência moderna à interface."""

APP_STYLESHEET = """
QMainWindow { background-color: #ffffff; }

QMenuBar { background-color: #fafafa; border-bottom: 1px solid #e0e0e0; }
QMenuBar::item:selected { background: #dbe9ff; }

QPushButton {
    background-color: #2d6cdf;
    color: white;
    border: none;
    padding: 6px 14px;
    border-radius: 6px;
    font-weight: 500;
}
QPushButton:hover { background-color: #1f57c0; }
QPushButton:disabled { background-color: #b7c6e0; }

QLineEdit { border: 1px solid #ccc; border-radius: 4px; padding: 3px; }

QStatusBar { background: #fafafa; border-top: 1px solid #e0e0e0; }
"""