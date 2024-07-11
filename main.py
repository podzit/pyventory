from nicegui import ui
from display_functions import display
from constantes import HOST, PORT

ui.query('body').classes('bg-gray-100')

display()

ui.run(host=HOST, port=PORT, title='INVENSTUD', uvicorn_reload_includes='*.py,*.log', favicon='🗃️')
