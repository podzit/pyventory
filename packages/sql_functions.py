from packages.env import DB, TABLE, DUMP_FILE, EXPORT_FILE, INVOICE_TMP, PICTURE_TMP, text
from nicegui import ui
import sqlite3, os, datetime, logging

def get_table() -> list:
    """Get data from 'gear' table

    Returns:
        list: Data from 'gear' table
    """

    try:
        cnx = sqlite3.connect(DB)
        curseur = cnx.cursor()
        sql = f"select * from {TABLE}"
        curseur.execute(sql)
        content = curseur.fetchall()
        return content
    except Exception as e:
        logging.error(e)
    finally:
        curseur.close()
        cnx.close()

def get_by_id(p_id:int) -> list:
    """Get product by his ID from 'gear' table

    Args:
        p_id (int): Product ID

    Returns:
        list: Product details
    """
    try:
        cnx = sqlite3.connect(DB)
        curseur = cnx.cursor()
        sql = f"select * from {TABLE} where id={p_id}"
        curseur.execute(sql)
        gear = curseur.fetchone()
        return gear
    except Exception as e:
        logging.error(e)
    finally:
        curseur.close()
        cnx.close()        

def get_all(db_column:str) -> list:
    """Get all data of a column from 'gear' table
    
    Args:
        str: Column name in database

    Returns:
        list: All column's data from 'gear' table once
    """
    content_filtered = []
    try:
        cnx = sqlite3.connect(DB)
        curseur = cnx.cursor()
        sql = f"select {db_column} from {TABLE}"
        curseur.execute(sql)
        content = curseur.fetchall()
        for c in content:
            if c not in content_filtered:
                content_filtered.append(c)
        return content_filtered
    except Exception as e:
        logging.error(e)
    finally:
        curseur.close()
        cnx.close()

def tmp_read() -> tuple:
    """Read temp file with invoices and pictures name

    Returns:
        tuple: invoice (invoice name), picture (picture name)
    """
    invoice = ''
    picture = ''
    lst = [INVOICE_TMP,PICTURE_TMP]
    for l in lst:
        if os.path.exists(l):
            with open(l, mode='r') as f:
                f.seek(0)
                if l == INVOICE_TMP:
                    invoice = f.read()
                if l == PICTURE_TMP:
                    picture = f.read()
            os.remove(l)
    return invoice, picture

def insert(p_type, brand, ref:str, price:float, date:str, quantity:int, argus:str, last_argus:str, shop:bool, dialog:object, serial:str=None, comment:str=None) -> None:
    """Add product into 'gear' table

    Args:
        p_type (Any): Product type
        brand (Any): Product brand
        ref (str): Product reference
        price (float): Product price
        date (str): Product purchase date
        quantity (int): Product quantity
        argus (str): Product argus
        last_argus (str): Product argus last check date
        shop (bool): Still available on sell ?
        dialog (object): Dialog object
        serial (str, optional):Product serial number. Defaults to None.
        comment (str, optional): Comment about product. Defaults to None.
    """
    if type(brand) == tuple:
        brand = brand[0]
    if type(p_type) == tuple:
        p_type = p_type[0]
    else:
        pass
    if p_type == None or brand == None or ref == '' or price == '' or date == '':
        ui.notify(text['notify_dialog_miss_mandatory'])
    else:
        dialog.close()
        invoice, picture = tmp_read()
        ui.notify(f"{brand} {ref} {text['notify_dialog_inserted']}")
        if shop:
            shop = 1
        else:
            shop = 0
        try:
            cnx = sqlite3.connect(DB)
            curseur = cnx.cursor()
            sql = f"insert into {TABLE} values (null,:brand,:ref,:quantity,:price,:date,:argus,:last_argus,:invoice,:picture,:type,:serial,:comment,:shop) "
            params = {
                'type': p_type,
                'brand': brand,
                'ref': ref,
                'quantity': quantity,
                'price': price,
                'date': date,
                'argus': argus,
                'last_argus': last_argus,
                'invoice': invoice,
                'picture': picture,
                'serial': serial,
                'comment': comment,
                'shop': shop
            }
            curseur.execute(sql, params)
            cnx.commit()
            logging.warning(f"{text['logging_add_info']} {text['column11']}: {p_type}, {text['column2']}: {brand}, {text['column3']}: {ref}, {text['column4']}: {quantity}, {text['column5']}: {price}, {text['column6']}: {date}, {text['column7']}: {argus}, {text['column8']}: {last_argus}, {text['column9']}: {invoice}, {text['column10']}: {picture}, {text['column11']}: {serial}, {text['column12']}: {comment}, {text['column13']}: {shop}")
        except Exception as e:
            cnx.rollback()
            logging.error(e)
        finally:
            curseur.close()
            cnx.close()

def update(p_id:int, p_type:str, brand:str, ref:str, quantity:int, price:float, date:str, argus:float, last_argus:str, serial:str, comment:str, shop:bool, dialog:object) -> None:
    """Update a product

    Args:
        p_id (int): Product ID
        p_type (str): Product type
        brand (str): Product brand
        ref (str): Product reference
        quantity (int): Product quantity
        price (float): Product price
        date (str): Product purchase date
        argus (float): Product argus
        last_argus (str): Product argus check date
        serial (str): Product serial
        comment (str): Comment about product
        shop (bool): Still available on sell ?
        dialog (object): Dialog box
    """
    invoice, picture = tmp_read()   
    if p_type == '' or brand == '' or ref == '' or price == '' or date == '':
        ui.notify(text['notify_dialog_miss_mandatory'])
    else:
        ui.notify(f"{brand} {ref} {text['notify_dialog updated']}")
        dialog.close()
        if shop:
            shop = 1
        else:
            shop = 0
        try:
            cnx = sqlite3.connect(DB)
            curseur = cnx.cursor()
            sql = f"update {TABLE} set ref=:ref,quantity=:quantity,price=:price,date=:date,\
                argus=:argus,last_argus=:last_argus,invoice=:invoice,picture=:picture,serial=:serial,comment=:comment,shop=:shop where id=:id"
            params = {
                'id': p_id,
                'ref': ref,
                'quantity': quantity,
                'price': price,
                'date': date,
                'argus': argus,
                'last_argus': last_argus,
                'invoice': invoice,
                'picture': picture,
                'serial': serial,
                'comment': comment,
                'shop': shop
            }
            curseur.execute(sql, params)
            cnx.commit()
            logging.warning(f"{text['logging_update_info']} {text['column1']}: {p_id} {text['column11']}: {p_type}, {text['column2']}: {brand}, {text['column3']}: {ref}, {text['column4']}: {quantity}, {text['column5']}: {price}, {text['column6']}: {date}, {text['column7']}: {argus}, {text['column8']}: {last_argus}, {text['column9']}: {invoice}, {text['column10']}: {picture}, {text['column11']}: {serial}, {text['column12']}: {comment}, {text['column13']}: {shop}")
        except Exception as e:
            cnx.rollback()
            logging.error(e)
        finally:
            curseur.close()
            cnx.close()

def update_argus(p_id:int, argus:float) -> None:
    """Auto update for argus price and date (useless for the moment)

    Args:
        p_id (int): Product ID
        argus (float): Product argus
        last_argus (str): Argus last check date
    """
    today = (datetime.datetime.today()).strftime("%d-%m-%Y")
    try:
        cnx = sqlite3.connect(DB)
        curseur = cnx.cursor()
        sql = f"update {TABLE} set argus=:argus,last_argus=:last_argus where id=:id"
        params = {
            'id': p_id,
            'argus': argus,
            'last_argus': today
        }
        curseur.execute(sql, params)
        cnx.commit()
        logging.warning(f"{text['logging_update_argus']} {text['column1']}: {p_id}, {text['column7']}: {argus}")
    except Exception as e:
        cnx.rollback()
        logging.error(e)
    finally:
        curseur.close()
        cnx.close()

def delete(p_id:int):
    """Delete a product from 'gear' table

    Args:
        p_id (int): Product ID
    """
    try:
        cnx = sqlite3.connect(DB)
        curseur = cnx.cursor()
        sql = f"delete from {TABLE} where id={p_id}"
        curseur.execute(sql)
        cnx.commit()
        logging.warning(f"{text['logging_delete_info']} id : {p_id}")
    except Exception as e:
        cnx.rollback()
        logging.error(e)
    finally:
        curseur.close()
        cnx.close()

def export() -> None:
    """Export data from 'gear' table to csv file
    """
    csv = f"{text['column1']}, {text['column2']}, {text['column3']}, {text['column4']}, {text['column5']}, {text['column6']}, {text['column7']}, {text['column8']}, {text['column9']}, {text['column10']}, {text['column11']}, {text['column12']}, {text['column13']}, {text['column14']}\n"
    try:
        cnx = sqlite3.connect(DB)
        curseur = cnx.cursor()
        sql = f"select * from {TABLE}"
        curseur.execute(sql)
        content = curseur.fetchall()
        for c in content:
            if c[13] == 1:
                shop = text['csv_shop_yes']
            else:
                shop = text['csv_shop_no']
            csv += f'{c[0]},{c[1]},{c[2]},{c[3]},{c[4]},{c[5]},{c[6]},{c[7]},{c[8]},{c[9]},{c[10]},{c[11]},{c[12]},{shop}\n'
        with open(EXPORT_FILE, mode='w') as f:
            f.write(str(csv))
        if os.path.exists(EXPORT_FILE):
            ui.download(EXPORT_FILE)
    except Exception as e:
        logging.error(e)
    finally:
        curseur.close()
        cnx.close()

def dump(download:bool=True) -> None:
    """Create a dump file of the database

        Args:
            download (bool): If True download dump file
    """
    try:
        with open(DUMP_FILE, mode='w') as f:
                f.write('')
        cnx = sqlite3.connect(DB)
        for line in cnx.iterdump():
            if line.startswith('INSERT INTO "gear"'):
                with open(DUMP_FILE, mode='a') as f:
                    f.write('%s\n' % line)
        if download == True:
            if os.path.exists(DUMP_FILE):
                ui.download(DUMP_FILE)
    except Exception as e:
        logging.error(e)
    finally:
        cnx.close()    