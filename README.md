# Pyventory

Pyventory is a Python app to inventory your equipment.

## Installation

Need python 3.10 or higher and [nicegui](https://nicegui.io/) installed.

```bash
pip install nicegui
```

## Customize your variables
Edit const.py to custom your environnement:
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

## Auto backup

Use save_db.py in your cron to auto backup 

```python
python3 ./save_db.py
```

## Import data
You need a db.dump file in the same directory. Create this file on web GUI or with save_db.py

```python
python3 ./import.py
```

## Start as a service

For Ubuntu create pyventory.service in /etc/systemd/system/ with this lines:

```shell
[Unit]
Description=Pyventory
After=syslog.target network.target

[Service]
WorkingDirectory=[your_working_directory]
ExecStart=python3.10 [path_to_main.py]

Restart=always
RestartSec=120

[Install]
WantedBy=multi-user.target
```

Then reload daemon:

```shell
sudo systemctl daemon-reload
```

After that you can start stop and status with:
```shell
sudo service pyventory start
sudo service pyventory status
sudo service pyventory stop
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.