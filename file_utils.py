import os


def format_size(num_bytes: int) -> str:
    """Formata bytes em unidade legível (B, KB, MB, GB)."""
    size = float(num_bytes)
    for unit in ["B", "KB", "MB", "GB"]:
        if size < 1024.0:
            return f"{size:.0f} {unit}" if unit == "B" else f"{size:.1f} {unit}"
        size /= 1024.0
    return f"{size:.1f} TB"


def get_file_metadata(file_path: str) -> dict:
    """Retorna metadados básicos do arquivo para exibição na prévia."""
    stat = os.stat(file_path)
    return {
        "name": os.path.basename(file_path),
        "size": stat.st_size,
        "size_formatted": format_size(stat.st_size),
        "extension": os.path.splitext(file_path)[1].lower(),
    }