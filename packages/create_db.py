import sqlite3, logging

def create_db(db:str, text:dict) -> None:
    """ Create database

    Args:
        db (str): Database path
        text (dict): Text from languages.py
    """
    try:
        cnx = sqlite3.connect(db)
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