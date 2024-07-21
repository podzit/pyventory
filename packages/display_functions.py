from packages.env import INVOICE_DIR, PICTURE_DIR, INVOICE_TMP, PICTURE_TMP, INVOICE_LINK, PICTURE_LINK, text
from packages.sql_functions import get_table, update, insert, delete, get_all, dump, export
from packages.class_p import Product
from nicegui import ui, app
import os

def argus_color(price:float, argus:float) -> str:
    """Change argus color after comparison with product price

    Args:
        price (float): Purchase price
        argus (float): Argus

    Returns:
        str: Argus color
    """
    color = 'black'
    if argus:
        if argus >= price :
            color = 'green'
        if argus < price :
            color = 'red'
    else:
        color = 'black'
    return color

def gears_rows() -> tuple:
    """Get data to put in rows

    Returns:
        tuple(list,float,float): Data from database (list), total price (float), total argus (float)
    """
    total = 0
    argus_total = 0
    data=[]
    gears = get_table()
    for gear in gears:
        if gear[13] == 1:
            shop = '✅'
        else:
            shop = '❌'
        if gear[8]:
            invoice_row = os.path.join(INVOICE_LINK,gear[8])
            invoice = f'{invoice_row}'
        else:
            invoice = ''
        if gear[9]:
            picture_row = os.path.join(PICTURE_LINK,gear[9])
            picture = f'{picture_row}'
        else:
            picture = ''
        g = {
                'id': gear[0],
                'brand': gear[1],
                'ref': gear[2],
                'quantity': gear[3],
                'price': gear[4],
                'date': gear[5],
                'argus': gear[6],
                'last_argus': gear[7],
                'invoice': invoice,
                'picture': picture,
                'type': gear[10],
                'serial': gear[11],
                'comment': gear[12],
                'shop': gear[13],
                'shop_icon': shop
            }
        data.append(g)
        total += gear[4] * gear[3]
        if gear[6]:
            argus_total += gear[6] * gear[3]

    return data, total, argus_total


@ui.page('/main')
def main_page():
    """Multi instance function
    """
    display()

def display() -> None:
    """Main display function
    
    """

    data = gears_rows()[0]
    total = gears_rows()[1]
    total_str = round(total,2)
    argus_total = gears_rows()[2]
    argus_total_str = round(argus_total,2)
    color = argus_color(total, argus_total)
    
    columns = [
        {'name': 'id', 'label': text['column1'], 'field': 'id', 'align': 'left'},
        {'name': 'brand', 'label': text['column2'], 'field': 'brand', 'sortable': True, 'align': 'left'},
        {'name': 'ref', 'label': text['column3'], 'field': 'ref', 'sortable': True, 'align': 'left'},
        {'name': 'quantity', 'label': text['column4'], 'field': 'quantity', 'sortable': True, 'align': 'left'},
        {'name': 'price', 'label': text['column5'], 'field': 'price', 'sortable': True, 'align': 'left', ':format': 'value => value + " €"'},
        {'name': 'date', 'label': text['column6'], 'field': 'date', 'align': 'left'},
        {'name': 'argus', 'label': text['column7'], 'field': 'argus', 'align': 'left', ':format': 'value => value + " €"'},      
        {'name': 'last_argus', 'label': text['column8'], 'field': 'last_argus', 'align': 'left'},      
        {'name': 'invoice', 'label': text['column9'], 'field': 'invoice', 'align': 'left'},      
        {'name': 'picture', 'label': text['column10'], 'field': 'picture', 'align': 'left'},      
        {'name': 'type', 'label': text['column11'], 'field': 'type', 'sortable': True, 'align': 'left'},      
        {'name': 'serial', 'label': text['column12'], 'field': 'serial', 'align': 'left'},      
        {'name': 'comment', 'label': text['column13'], 'field': 'comment', 'align': 'left'},      
        {'name': 'shop', 'label': text['column14'], 'field': 'shop', 'align': 'left'},
        {'name': 'shop_icon', 'label': text['column14'], 'field': 'shop_icon', 'align': 'left'},      
        {'name': 'value', 'label': '', 'field': 'value'}
    ]

    with ui.header(elevated=True).classes('bg-gradient-to-r from-cyan-100 to-blue-300'):
        with ui.button(icon='menu').classes('mt-4'):
            with ui.menu(), ui.column().classes('gap-0 p-2'):
                for column in columns:
                    if column['name'] != 'value' and column['name'] != 'shop':
                        if column['name'] == 'id' or column['name'] == 'price' or column['name'] == 'date' or column['name'] == 'argus' \
                            or column['name'] == 'quantity' or column['name'] == 'last_argus' or column['name'] == 'invoice' or column['name'] == 'picture' \
                                or column['name'] == 'type' or column['name'] == 'serial' or column['name'] == 'comment' or column['name'] == 'shop_icon':
                            ui.switch(column['label'], value=False, on_change=lambda e, column=column: toggle(table, column, e.value))
                        else:
                            ui.switch(column['label'], value=True, on_change=lambda e, column=column: toggle(table, column, e.value))
        ui.button(icon='add_circle_outline', on_click=lambda: add_product()).classes('w-4 mt-4')
        ui.button(text['csv'], on_click=lambda: export()).classes('mt-4') 
        ui.button(text['dump'], on_click=lambda: dump()).classes('mt-4')
        f = ui.input('Filtre')
        with ui.grid().classes('gap-0'):
            ui.chip(f"{text['total']} {total_str}€", removable=True, color='blue-2')
            ui.chip(f"{text['argus_total']} {argus_total_str}€", removable=True, color='blue-2').classes(f'text-{color}-700')
    with ui.table(columns, rows=data).classes('w-full bg-gradient-to-r from-stone-100 to-zinc-200').bind_filter_from(f, 'value') as table:
        for column in columns:
            if column['name'] == 'id' or column['name'] == 'date' or column['name'] == 'price' or column['name'] == 'argus' or column['name'] == 'quantity'\
                or column['name'] == 'last_argus' or column['name'] == 'invoice' or column['name'] == 'picture' or column['name'] == 'type'\
                    or column['name'] == 'serial' or column['name'] == 'comment' or column['name'] == 'shop' or column['name'] == 'shop_icon':
                column['classes'] = 'hidden'
                column['headerClasses'] = 'hidden'
        table.add_slot('body-cell-invoice', '''
            <q-td :props="props">
                <a :href="props.value" target=_blank>{{ props.value }}</a>
            </q-td>
        ''')
        table.add_slot('body-cell-picture', '''
            <q-td :props="props">
                <a :href="props.value" target=_blank>{{ props.value }}</a>
            </q-td>
        ''')
        table.add_slot(f'body-cell-value', """
            <q-td :props="props">
                <q-btn @click="$parent.$emit('edit', props)" icon="edit" flat dense color='blue'/>
                <q-btn @click="$parent.$emit('del', props)" icon="delete" flat dense color='red'/>
            </q-td>
        """)
    table.on('edit', lambda msg: edit_product(msg.args))
    table.on('del', lambda msg: remove_dialog(msg.args))

def toggle(table:object, column: dict, visible: bool) -> None:
    """Column hidden switch choice

    Args:
        table (object): Table
        column (dict): Columns
        visible (bool): Visible (True ou False)
    """
    column['classes'] = '' if visible else 'hidden'
    column['headerClasses'] = '' if visible else 'hidden'
    table.update()


def rec(e:object, path:str) -> None:
    """Write invoices and pictures filename

    Args:
        e (object): Object uploaded
        path (str): Path to write file
    """
    tmp_file = e.content
    file_as_bytes = tmp_file.read()
    file_dst = os.path.join(path,e.name)
    with open(file_dst, mode="wb") as g:
        g.write(file_as_bytes)
    if path == INVOICE_DIR:
        with open(INVOICE_TMP, mode='w') as f:
            f.write(e.name)
    if path == PICTURE_DIR:
        with open(PICTURE_TMP, mode='w') as f:
            f.write(e.name)

def clean_last() -> None:
    """Clean last tmp files written
    """
    if os.path.exists(INVOICE_TMP):
        os.remove(INVOICE_TMP)
    if os.path.exists(PICTURE_TMP):
        os.remove(PICTURE_TMP)

def add_product() -> None:
    """Display to add a product
    """
    all_type = get_all('type')
    all_brand = get_all('brand')

    with ui.dialog() as dialog, ui.card():
        clean_last()
        ui.label(text['mandatory'])
        with ui.grid(columns=2):
            p_type = ui.select(label=text['dialog_type'], options=all_type, with_input=True, new_value_mode='add', multiple=False) 
            brand = ui.select(label=text['dialog_brand'], options=all_brand, with_input=True, new_value_mode='add', multiple=False)
            ref = ui.input(label=text['dialog_ref'])
            nb = ui.number(label=text['dialog_quantity'], value=1)
            price = ui.number(label=text['dialog_price'])
            with ui.input(text['dialog_purchase_date'], placeholder='DD-MM-YYYY') as date:
                with ui.menu().props('no-parent-event') as menu:
                    with ui.date(mask='DD-MM-YYYY').bind_value(date):
                        with ui.row().classes('justify-end'):
                            ui.button(text['dialog_calendar_close'], on_click=menu.close).props('flat')
                with date.add_slot('append'):
                    ui.icon('edit_calendar').on('click', menu.open).classes('cursor-pointer')
            argus = ui.number(label=text['dialog_argus'])
            with ui.input(text['dialog_argus_date'], placeholder='DD-MM-YYYY') as last_argus:
                with ui.menu().props('no-parent-event') as menu:
                    with ui.date(mask='DD-MM-YYYY').bind_value(last_argus):
                        with ui.row().classes('justify-end'):
                            ui.button(text['dialog_calendar_close'], on_click=menu.close).props('flat')
                with last_argus.add_slot('append'):
                    ui.icon('edit_calendar').on('click', menu.open).classes('cursor-pointer')
            ui.upload(label=text['dialog_invoice'], auto_upload=True, on_upload=lambda e: rec(e, INVOICE_DIR)).classes('ml-2 w-40')
            ui.upload(label=text['dialog_picture'], auto_upload=True, on_upload=lambda e: rec(e, PICTURE_DIR)).classes('ml-2 w-40')
            with ui.grid():
                serial = ui.input(label=text['dialog_serial'])
                shop = ui.checkbox(text['dialog_shop'])
            comment = ui.textarea(label=text['dialog_comment'])
            ui.button(text['dialog_add_button'], on_click=lambda : (insert(p_type.value, brand.value, ref.value, price.value, date.value, nb.value, argus.value, \
                    last_argus.value, shop.value, dialog, serial.value, comment.value)))
            ui.button(text['dialog_close_button'], color='red', icon='highlight_off', on_click=dialog.close)

    dialog.open()

def edit_product(msg:dict) -> None:
    """Display to modify a product

    Args:
        msg (dict): Dictionnary with product details from table rows
    """

    with ui.dialog() as dialog, ui.card():
        clean_last()
        fact_clean = str(msg['row']['invoice']).replace(f'{INVOICE_LINK}/', '').replace(f'{INVOICE_LINK}\\','')
        photo_clean = str(msg['row']['picture']).replace(f'{PICTURE_LINK}/', '').replace(f'{PICTURE_LINK}\\', '')
        with open(INVOICE_TMP, mode='w') as f:
            f.seek(0)
            f.write(fact_clean)
        with open(PICTURE_TMP, mode='w') as g:
            g.seek(0)
            g.write(photo_clean)

        prod = Product(msg['row']['id'], msg['row']['brand'], msg['row']['ref'], msg['row']['quantity'], msg['row']['price'], msg['row']['date'],\
        msg['row']['argus'], msg['row']['last_argus'], msg['row']['type'], msg['row']['serial'], msg['row']['comment'], msg['row']['shop'], fact_clean, photo_clean)
        color = argus_color(prod.price, prod.argus)
        if prod.shop == 1:
            shop_check = True
        if prod.shop == 0:
            shop_check = False
        ui.label(text['mandatory'])
        with ui.grid(columns=2):
            ui.label(text['dialog_type'])
            ui.label(text['dialog_brand'])
            ui.label(prod.p_type)
            ui.label(prod.brand)
            ref = ui.input(label=text['dialog_ref'], value=prod.ref)
            nb = ui.number(label=text['dialog_quantity'], value=prod.quantity)
            price = ui.number(label=text['dialog_price'], value=prod.price)
            with ui.input(text['dialog_purchase_date'], value=prod.date, placeholder='DD-MM-YYYY') as date:
                with ui.menu().props('no-parent-event') as menu:
                    with ui.date(mask='DD-MM-YYYY').bind_value(date):
                        with ui.row().classes('justify-end'):
                            ui.button(text['dialog_calendar_close'], on_click=menu.close).props('flat')
                with date.add_slot('append'):
                    ui.icon('edit_calendar').on('click', menu.open).classes('cursor-pointer')            
            argus = ui.number(label=text['dialog_argus'], value=prod.argus).props(f'input-style="color: {color}"')
            with ui.input(text['dialog_argus_date'], value=prod.last_argus, placeholder='DD-MM-YYYY') as last_argus:
                with ui.menu().props('no-parent-event') as menu:
                    with ui.date(mask='DD-MM-YYYY').bind_value(last_argus):
                        with ui.row().classes('justify-end'):
                            ui.button(text['dialog_calendar_close'], on_click=menu.close).props('flat')
                with last_argus.add_slot('append'):
                    ui.icon('edit_calendar').on('click', menu.open).classes('cursor-pointer')          
            ui.upload(label=f'{prod.invoice}', auto_upload=True, on_upload=lambda e: rec(e, INVOICE_DIR)).classes('w-40')
            ui.upload(label=f'{prod.picture}', auto_upload=True, on_upload=lambda e: rec(e, PICTURE_DIR)).classes('w-40')
            with ui.grid():
                serial = ui.input(label=text['dialog_serial'], value=prod.serial)
                shop = ui.checkbox(text['dialog_shop'], value=shop_check)              
            comment = ui.textarea(label=text['dialog_comment'], value=prod.comment)
            ui.button(text['dialog_update_button'], on_click=lambda : (update(prod.p_id, prod.p_type, prod.brand, ref.value, nb.value, price.value, date.value, \
                argus.value, last_argus.value, serial.value, comment.value, shop.value, dialog)))
            ui.button(text['dialog_close_button'], color='red', icon='highlight_off', on_click=dialog.close)
    
    dialog.open()

def remove_dialog(msg:dict) -> None:
    """Remove confirmation

    Args:
        msg (dict): Dictionnary with product details from table rows
    """
    with ui.dialog() as dialog, ui.card():
        ui.label(text['dialog_suppress_title'])
        with ui.grid(columns=3):
            ui.button(text['dialog_suppress_yes_button'], on_click=lambda: remove_product(msg, dialog))
            ui.label('')
            ui.button(text['dialog_suppress_no_button'], color='red', on_click=dialog.close)
    
    dialog.open()

def remove_product(msg:dict, dialog:object) -> None:
    """Product remove

    Args:
        msg (dict): Dictionnary with product details from table rows
        dialog (object): Dialog box
    """
    id_msg = msg['row']['id']
    brand_msg = msg['row']['brand']
    ref_msg = msg['row']['ref']
    delete(id_msg)
    ui.notify(f"{brand_msg} {ref_msg} {text['notify_suppressed']}")
    dialog.close()