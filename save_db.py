from packages.env import this_folder, text, DB
from packages.sql_functions import dump
import os, datetime, logging

today = (datetime.datetime.today()).strftime('%d-%m-%Y')
old = ((datetime.datetime.today())-datetime.timedelta(days=15)).strftime('%d-%m-%Y')
db_file = os.path.join(this_folder,'db.dump')
old_db_file = os.path.join(this_folder,f'db.dump_{old}')

if os.path.exists(DB) and os.path.exists(db_file):
    os.rename(db_file, f'{db_file}_{today}')
    try: 
        dump(False)
        logging.warning(f"{text['auto_save_ok']}")
    except Exception as e:
        logging.error(f"{text['auto_save_failed']} {e}")
if os.path.exists(old_db_file):
    os.remove(old_db_file)
    logging.warning(f"{text['old_backup_removed']}")