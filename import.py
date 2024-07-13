from constantes import DB, TABLE, logging, DUMP_FILE
from languages import *
import sqlite3, os

def import_data():
    """To import data from dump file to database
    """
    params = []
    with open(DUMP_FILE, mode='r') as f:
        sql = f.readlines()
    for line in sql:
        if line.startswith('INSERT'):
            lst = (line.split("VALUES(",1)[1]).replace(');','').split(',')
            brand = lst[1].replace('\'','')
            ref = lst[2].replace('\'','')
            quantity = int(lst[3])
            if lst[4] == 'NULL':
                price = 0
            else:
                price = float(lst[4])
            date = lst[5].replace('\'','')
            if lst[6] == 'NULL':
                argus = 0
            else:
                argus = float(lst[6])
            last_argus = lst[7].replace('\'','')
            invoice = lst[8].replace('\'','')
            picture = lst[9].replace('\'','')
            p_type = lst[10].replace('\'','')
            serial = lst[11].replace('\'','')
            comment = lst[12].replace('\'','')
            shop = lst[13].replace('\'','')
            try:
                cnx = sqlite3.connect(DB)
                curseur = cnx.cursor()
                sql = f"insert into {TABLE} values (null,:brand,:ref,:quantity,:price,:date,:argus,:last_argus,:invoice,:picture,:type,:serial,:comment,:shop) "
                params = {
                    'brand': brand,
                    'ref': ref,
                    'quantity': quantity,
                    'price': price,
                    'date': date,
                    'argus': argus,
                    'last_argus': last_argus,
                    'invoice': invoice,
                    'picture': picture,
                    'type': p_type,
                    'serial': serial,
                    'comment': comment,
                    'shop': shop
                }
                curseur.execute(sql, params)
                logging.warning(text['import_data_ok'])
                cnx.commit()
            except Exception as e:
                cnx.rollback()
                logging.error(f"{text['import_data_failed']} {e}")
            finally:
                curseur.close()
                cnx.close()

if __name__ == "__main__":
    if os.path.exists(DUMP_FILE):
        import_data()