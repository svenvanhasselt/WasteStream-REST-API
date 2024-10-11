import sqlite3
from flask import g, abort

DATABASE = "seenons_api/database/seenons1.db"

def open_db():
    if 'db' not in g:
        g.database = sqlite3.connect(f'file:{DATABASE}?mode=ro', uri=True)
        g.database.row_factory = sqlite3.Row
        return g.database
