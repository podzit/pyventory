from packages.env import HOST, PORT, INVOICE_DIR, PICTURE_DIR, DB, text, import_dump, DUMP_FILE, IMPORT_TMP, TABLE, INVOICE_LINK, PICTURE_LINK
from packages.init import init_function
from packages.display_functions import main_page
from nicegui import ui

init_function(INVOICE_DIR, PICTURE_DIR, DB, text, import_dump, DUMP_FILE, IMPORT_TMP, TABLE, INVOICE_LINK, PICTURE_LINK)

ui.query('body').classes('bg-gray-100')

main_page()

ui.run(host=HOST, port=PORT, title='Pyventory', uvicorn_reload_includes='*.py,*.log', favicon='🗃️')
