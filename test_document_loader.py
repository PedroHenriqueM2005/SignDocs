import fitz
import pytest
from app.core.document_loader import load_document
from app.core.exceptions import UnsupportedFormatError, DocumentNotFoundError
from app.core.pdf_document import PDFDocument
from app.core.text_document import TextDocument


def create_sample_pdf(path, pages=3):
    doc = fitz.open()
    for _ in range(pages):
        doc.new_page()
    doc.save(path)
    doc.close()


def test_load_pdf_document(tmp_path):
    pdf_path = tmp_path / "sample.pdf"
    create_sample_pdf(str(pdf_path), pages=3)

    document = load_document(str(pdf_path))
    assert isinstance(document, PDFDocument)
    assert document.page_count() == 3
    document.close()


def test_load_text_document(tmp_path):
    txt_path = tmp_path / "sample.txt"
    txt_path.write_text("Linha de teste\n" * 200, encoding="utf-8")

    document = load_document(str(txt_path))
    assert isinstance(document, TextDocument)
    assert document.page_count() >= 1
    document.close()


def test_unsupported_format(tmp_path):
    fake_path = tmp_path / "file.xyz"
    fake_path.write_text("dummy")
    with pytest.raises(UnsupportedFormatError):
        load_document(str(fake_path))


def test_file_not_found():
    with pytest.raises(DocumentNotFoundError):
        load_document("/caminho/que/nao/existe.pdf")


def test_pdf_render_page(tmp_path):
    pdf_path = tmp_path / "sample.pdf"
    create_sample_pdf(str(pdf_path), pages=1)
    document = load_document(str(pdf_path))
    image = document.render_page(0, zoom=1.0)
    assert image.width() > 0
    assert image.height() > 0
    document.close()


def test_pdf_render_invalid_page_raises(tmp_path):
    pdf_path = tmp_path / "sample.pdf"
    create_sample_pdf(str(pdf_path), pages=1)
    document = load_document(str(pdf_path))
    with pytest.raises(IndexError):
        document.render_page(5)
    document.close()