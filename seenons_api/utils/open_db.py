import sqlite3
from flask import g

DATABASE = "seenons_api/database/seenons1.db"

def open_db():
    try:
        if 'db' not in g:
            g.database = sqlite3.connect(DATABASE)
            g.database.row_factory = sqlite3.Row
            return g.database
    except:
        return None