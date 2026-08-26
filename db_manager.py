import sqlite3
import os
import time
from app.config import DB_PATH, MAX_RECENT_FILES


class DBManager:
    """Gerencia a persistência do histórico de arquivos abertos (SQLite)."""

    def __init__(self, db_path: str = DB_PATH):
        self.db_path = db_path
        self._init_db()

    def _get_connection(self):
        return sqlite3.connect(self.db_path)

    def _init_db(self):
        with self._get_connection() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS recent_files (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    path TEXT UNIQUE NOT NULL,
                    name TEXT NOT NULL,
                    doc_type TEXT,
                    page_count INTEGER,
                    last_opened REAL NOT NULL
                )
            """)
            conn.commit()

    def add_or_update_recent(self, path: str, name: str, doc_type: str, page_count: int):
        try:
            with self._get_connection() as conn:
                conn.execute("""
                    INSERT INTO recent_files (path, name, doc_type, page_count, last_opened)
                    VALUES (?, ?, ?, ?, ?)
                    ON CONFLICT(path) DO UPDATE SET
                        last_opened = excluded.last_opened,
                        page_count = excluded.page_count
                """, (path, name, doc_type, page_count, time.time()))
                conn.commit()
        except sqlite3.Error as e:
            raise RuntimeError(f"Erro ao salvar histórico: {e}")

    def get_recent_files(self, limit: int = MAX_RECENT_FILES):
        with self._get_connection() as conn:
            cur = conn.execute("""
                SELECT path, name, doc_type, page_count, last_opened
                FROM recent_files
                ORDER BY last_opened DESC
                LIMIT ?
            """, (limit,))
            rows = cur.fetchall()
        # filtra arquivos que ainda existem no disco (podem ter sido movidos/apagados)
        return [r for r in rows if os.path.exists(r[0])]

    def remove_recent(self, path: str):
        with self._get_connection() as conn:
            conn.execute("DELETE FROM recent_files WHERE path = ?", (path,))
            conn.commit()

    def clear_all(self):
        with self._get_connection() as conn:
            conn.execute("DELETE FROM recent_files")
            conn.commit()