from constantes import logging, DB
from languages import *
import sqlite3, os

def create_db():
    """ Create database
    """
    try:
        cnx = sqlite3.connect(DB)
        curseur = cnx.cursor()
        curseur.execute(
            """
                CREATE TABLE IF NOT EXISTS gear(
                id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE,
                brand TEXT NOT NULL,
                ref TEXT NOT NULL,
                quantity INTEGER NOT NULL DEFAULT 1,
                price REAL NOT NULL,
                date TEXT NOT NULL DEFAULT '01/01/1970',
                argus REAL,
                last_argus TEXT,
                invoice TEXT,
                picture TEXT,
                type TEXT NOT NULL,
                serial TEXT,
                comment TEXT,
                shop INTEGER NOT NULL
                )
            """
        )
    except Exception as e:
        logging.error(f"{text['database_creation_failed']} {e}")
    finally:
        curseur.close()
        cnx.close()

if __name__ == "__main__":
    if not os.path.exists(DB):
        logging.warning(text['database_created'])
        create_db()
    else:
        logging.warning(text['database_exists'])