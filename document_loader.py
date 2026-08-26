import os
from app.config import SUPPORTED_EXTENSIONS
from app.core.exceptions import UnsupportedFormatError, DocumentNotFoundError
from app.core.converters import convert_to_pdf
from app.core.pdf_document import PDFDocument
from app.core.image_document import ImageDocument
from app.core.text_document import TextDocument


def load_document(file_path: str):
    """
    Fábrica (Factory) que decide COMO carregar cada tipo de documento
    e retorna uma instância que implementa a interface Document.
    """
    if not os.path.isfile(file_path):
        raise DocumentNotFoundError(f"Arquivo não encontrado: {file_path}")

    ext = os.path.splitext(file_path)[1].lower()
    kind = SUPPORTED_EXTENSIONS.get(ext)

    if kind is None:
        raise UnsupportedFormatError(f"Formato não suportado: {ext}")

    if kind == "pdf":
        return PDFDocument(file_path)
    if kind == "image":
        return ImageDocument(file_path)
    if kind == "text":
        return TextDocument(file_path)
    if kind == "office":
        pdf_path = convert_to_pdf(file_path)  # pode levantar ConversionError
        return PDFDocument(pdf_path)

    raise UnsupportedFormatError(f"Tipo não tratado: {kind}")