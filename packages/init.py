from packages.create_db import create_db
from packages.import_data import import_data
from nicegui import app
import os, logging


def init_function(INVOICE_DIR: str, PICTURE_DIR:str, DB:str, text:dict, import_dump:bool, DUMP_FILE:str, IMPORT_TMP:str, TABLE:str, INVOICE_LINK:str, PICTURE_LINK:str) -> None:
    """Directories, database creation with import dump file

    Args:
        INVOICE_DIR (str): Invoices directory
        PICTURE_DIR (str): Pictures directory
        DB (str): Database path
        text (dict): Text dictionnary
        import_dump (bool): True to import dump file
        DUMP_FILE (str): Dump file path
        IMPORT_TMP (str): Dump temp file
        TABLE (str): Table in database
        INVOICE_LINK (str): Invoices link
        PICTURE_LINK (str): Pictures link
    """
    # Creating invoices and pictures directories
    dir_list = [INVOICE_DIR, PICTURE_DIR]
    for dir in dir_list:
        if not os.path.exists(dir):
            os.mkdir(dir)

    # Creating database
    if not os.path.exists(DB):
        logging.warning(text['database_created'])
        create_db(DB, text)

    # Import data backup (remove import_tmp if previous data imported)
    if import_dump and os.path.exists(DUMP_FILE) and not os.path.exists(IMPORT_TMP):
        import_data(DB, TABLE, DUMP_FILE, text, IMPORT_TMP)
    else:
        pass

    app.add_static_files(f'/{INVOICE_LINK}', INVOICE_DIR)
    app.add_static_files(f'/{PICTURE_LINK}', PICTURE_DIR)