from app.utils.file_utils import format_size, get_file_metadata


def test_format_size():
    assert format_size(500) == "500 B"
    assert "KB" in format_size(2048)
    assert "MB" in format_size(5 * 1024 * 1024)


def test_get_file_metadata(tmp_path):
    file_path = tmp_path / "example.txt"
    file_path.write_text("teste")

    metadata = get_file_metadata(str(file_path))
    assert metadata["name"] == "example.txt"
    assert metadata["extension"] == ".txt"
    assert metadata["size"] > 0