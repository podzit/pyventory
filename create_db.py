from constantes import logging, DB
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
                nb INTEGER NOT NULL DEFAULT 1,
                price REAL NOT NULL,
                date TEXT NOT NULL DEFAULT '01/01/1970',
                argus REAL,
                last_argus TEXT,
                fact TEXT,
                photo TEXT,
                type TEXT NOT NULL,
                serial TEXT,
                comment TEXT,
                shop INTEGER NOT NULL
                )
            """
        )
    except Exception as e:
        logging.error(e)
    finally:
        curseur.close()
        cnx.close()

if __name__ == "__main__":
    if not os.path.exists(DB):
        print('Création de la base')
        create_db()
    else:
        print('La base existe déjà !')