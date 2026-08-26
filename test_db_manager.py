from app.database.db_manager import DBManager


def test_add_and_get_recent(tmp_path):
    db = DBManager(str(tmp_path / "test.db"))
    fake_file = tmp_path / "doc.pdf"
    fake_file.write_text("conteudo fake")

    db.add_or_update_recent(str(fake_file), "doc.pdf", ".pdf", 5)
    recents = db.get_recent_files()

    assert len(recents) == 1
    assert recents[0][1] == "doc.pdf"


def test_remove_recent(tmp_path):
    db = DBManager(str(tmp_path / "test.db"))
    fake_file = tmp_path / "doc.pdf"
    fake_file.write_text("conteudo fake")

    db.add_or_update_recent(str(fake_file), "doc.pdf", ".pdf", 5)
    db.remove_recent(str(fake_file))
    recents = db.get_recent_files()

    assert len(recents) == 0


def test_update_existing_entry(tmp_path):
    db = DBManager(str(tmp_path / "test.db"))
    fake_file = tmp_path / "doc.pdf"
    fake_file.write_text("conteudo fake")

    db.add_or_update_recent(str(fake_file), "doc.pdf", ".pdf", 5)
    db.add_or_update_recent(str(fake_file), "doc.pdf", ".pdf", 10)
    recents = db.get_recent_files()

    assert len(recents) == 1
    assert recents[0][3] == 10  # page_count atualizado