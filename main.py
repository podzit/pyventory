from nicegui import ui
from display_functions import display
from const import HOST, PORT

ui.query('body').classes('bg-gray-100')

display()

ui.run(host=HOST, port=PORT, title='Pyventory', uvicorn_reload_includes='*.py,*.log', favicon='🗃️')
