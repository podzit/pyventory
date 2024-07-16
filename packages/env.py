from packages.languages import lang
import logging, os

this_folder = os.path.dirname(__file__)
DB = os.path.join(this_folder, 'pyventory.sqlite3')
TABLE = 'gear'
# Server IP
HOST = 'your_server_ip'
PORT = 8091
INVOICE_LINK = 'invoices'
PICTURE_LINK = 'pictures'
LOCAL_DIR = this_folder
DUMP_FILE = os.path.join(this_folder,'db.dump')
EXPORT_FILE = os.path.join(this_folder,'export.csv')
INVOICE_TMP = os.path.join(this_folder,'invoice_tmp')
PICTURE_TMP = os.path.join(this_folder,'picture_tmp')
IMPORT_TMP = os.path.join(this_folder, 'import_tmp')
INVOICE_DIR = os.path.join(LOCAL_DIR,INVOICE_LINK)
PICTURE_DIR = os.path.join(LOCAL_DIR,PICTURE_LINK)
# True or false
import_dump = True
# 'fr' or 'eng'
LANGUAGE = 'fr'

text = lang(LANGUAGE)

logging.basicConfig(
    filename=os.path.join(this_folder,'pyventory.log'),
    level= logging.WARNING,
    format="%(asctime)s - %(levelname)s - %(filename)s: %(message)s\n",
    datefmt="%d/%m/%Y - %H:%M"
)

