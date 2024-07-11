from sql_functions import dump
from constantes import this_folder
import os, datetime

today = (datetime.datetime.today()).strftime('%d-%m-%Y')
old = ((datetime.datetime.today())-datetime.timedelta(days=15)).strftime('%d-%m-%Y')
db_file = os.path.join(this_folder,'db.dump')
old_db_file = os.path.join(this_folder,f'db.dump_{old}')

if os.path.exists(db_file):
    os.rename(db_file, f'{db_file}_{today}')
try: 
    dump(False)
    with open('/var/log/save_db_inv_stud.log', mode='a') as f:
        f.write(f"{today} : Sauvegarde réussie\n")
except Exception as e:
    with open('/var/log/save_db_inv_stud.log', mode='a') as f:
        f.write(f"{today} : Problème de sauvegarde avec l'erreur quivante : {e}\n")
if os.path.exists(old_db_file):
    os.remove(old_db_file)
    with open('/var/log/save_db_inv_stud.log', mode='a') as f:
        f.write(f"{today} : Suppression de la sauvegrde datant de 15 jours\n")