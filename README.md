# Pyventory

Pyventory is a Python app to inventory your equipment.

## Installation

Need python 3.10 or higher and [nicegui](https://nicegui.io/) installed.

```bash
pip install nicegui
```

## Customize your variables
Edit constantes.py to custom your environnement:
```python
HOST = 'your_ip_server'
PORT = 8091 # Or another custom port
INVOICE_LINK = 'invoices' # Name of directory for invoices
PICTURE_LINK = 'pictures' # Name of directory for pictures
LANGUAGE = 'fr' # 'fr' or 'eng'
```

## Database creation
make a copy or rename pyventory-template.sqlite3 to pyventory.sqlite3 or use create_db.py

```python
python3 ./create_db.py
```

## Start app


```python
python3 ./main.py
```

## Import data
You need a db.dump file in the same directory

```python
python3 ./import.py
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.