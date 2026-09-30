"""Local storage of lecture packs in SQLite."""
import sqlite3
from datetime import datetime
from pathlib import Path

DB = Path(__file__).resolve().parent.parent / "data" / "lectures.db"


def _conn():
    DB.parent.mkdir(parents=True, exist_ok=True)
    c = sqlite3.connect(DB)
    c.execute("""CREATE TABLE IF NOT EXISTS lectures(
        id INTEGER PRIMARY KEY, title TEXT, created TEXT,
        transcript TEXT, board TEXT, notes TEXT, translation TEXT)""")
    return c


def save(title, transcript, board="", notes="", translation=""):
    with _conn() as c:
        c.execute("INSERT INTO lectures(title,created,transcript,board,notes,translation) VALUES(?,?,?,?,?,?)",
                  (title, datetime.now().isoformat(timespec="seconds"), transcript, board, notes, translation))


def list_lectures():
    with _conn() as c:
        return c.execute("SELECT id,title,created FROM lectures ORDER BY id DESC").fetchall()
