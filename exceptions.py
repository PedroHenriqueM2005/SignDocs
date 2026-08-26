class DocumentError(Exception):
    """Classe base para erros relacionados a documentos."""


class UnsupportedFormatError(DocumentError):
    """Levantado quando o formato do arquivo não é suportado."""


class DocumentNotFoundError(DocumentError):
    """Levantado quando o arquivo não existe no caminho informado."""


class ConversionError(DocumentError):
    """Levantado quando a conversão via LibreOffice falha."""


class CorruptedFileError(DocumentError):
    """Levantado quando o arquivo está corrompido ou ilegível."""