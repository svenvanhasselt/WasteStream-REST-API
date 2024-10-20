import sqlite3
from flask import g, abort

DATABASE = "seenons_api/database/seenons.db"

def open_db():
    if 'db' not in g:
        g.db = sqlite3.connect(f'file:{DATABASE}?mode=ro', uri=True)
        g.db.row_factory = sqlite3.Row
        return g.db
