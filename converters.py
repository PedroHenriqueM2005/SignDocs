import os
import shutil
import subprocess
import tempfile
import hashlib
import logging
from app.config import CACHE_DIR
from app.core.exceptions import ConversionError

logger = logging.getLogger(__name__)


def _find_soffice() -> str | None:
    """Localiza o executável do LibreOffice no sistema (Windows/Linux/Mac)."""
    candidates = [
        "soffice", "libreoffice",
        r"C:\Program Files\LibreOffice\program\soffice.exe",
        r"C:\Program Files (x86)\LibreOffice\program\soffice.exe",
    ]
    for c in candidates:
        if os.path.isabs(c):
            if os.path.exists(c):
                return c
        else:
            found = shutil.which(c)
            if found:
                return found
    return None


def convert_to_pdf(file_path: str) -> str:
    """
    Converte um documento Office (docx, xlsx, pptx, doc, xls, ppt) para PDF
    usando o LibreOffice em modo headless. Usa cache em disco para evitar
    reconverter o mesmo arquivo em aberturas futuras (chave = caminho +
    data de modificação + tamanho).
    """
    soffice_path = _find_soffice()
    if not soffice_path:
        raise ConversionError(
            "LibreOffice não encontrado no sistema. Instale o LibreOffice "
            "para abrir arquivos Word, Excel ou PowerPoint."
        )

    stat = os.stat(file_path)
    key_source = f"{file_path}-{stat.st_mtime}-{stat.st_size}"
    cache_key = hashlib.md5(key_source.encode("utf-8")).hexdigest()
    output_pdf = os.path.join(CACHE_DIR, f"{cache_key}.pdf")

    if os.path.exists(output_pdf):
        return output_pdf  # já convertido anteriormente

    # Usa um diretório temporário isolado para evitar colisão entre
    # conversões concorrentes (múltiplos documentos abertos ao mesmo tempo)
    tmp_outdir = tempfile.mkdtemp(prefix="conv_", dir=CACHE_DIR)
    try:
        cmd = [
            soffice_path, "--headless", "--norestore",
            "--convert-to", "pdf", "--outdir", tmp_outdir, file_path
        ]
        result = subprocess.run(cmd, capture_output=True, timeout=120)
        if result.returncode != 0:
            raise ConversionError(
                f"Falha ao converter arquivo: {result.stderr.decode(errors='ignore')}"
            )

        generated_name = os.path.splitext(os.path.basename(file_path))[0] + ".pdf"
        generated_path = os.path.join(tmp_outdir, generated_name)

        if not os.path.exists(generated_path):
            raise ConversionError("Conversão não gerou o arquivo PDF esperado.")

        shutil.move(generated_path, output_pdf)
        return output_pdf
    except subprocess.TimeoutExpired:
        raise ConversionError("Tempo excedido ao converter o documento.")
    except ConversionError:
        raise
    except Exception as e:
        logger.exception("Erro na conversão do documento")
        raise ConversionError(str(e))
    finally:
        shutil.rmtree(tmp_outdir, ignore_errors=True)