import logging, os

this_folder = os.path.dirname(__file__)
DB = os.path.join(this_folder, 'inv_stud-test.sqlite3')
TABLE = 'gear'
# Server IP
HOST = '192.168.1.2'
PORT = 8091
FACT_LINK = 'factures'
PHOTO_LINK = 'photos'
LOCAL_DIR = this_folder
DUMP_FILE = os.path.join(this_folder,'db.dump')
EXPORT_FILE = os.path.join(this_folder,'export.csv')
FACT_TMP = os.path.join(this_folder,'fact_tmp')
PHOTO_TMP = os.path.join(this_folder,'photo_tmp')
FACT_DIR = os.path.join(LOCAL_DIR,FACT_LINK)
PHOTO_DIR = os.path.join(LOCAL_DIR,PHOTO_LINK)
# 'fr' or 'eng'
LANGUAGE = 'fr'

logging.basicConfig(
    filename=os.path.join(this_folder,'inv_stud.log'),
    level= logging.WARNING
)