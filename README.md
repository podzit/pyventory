# Pyventory

Pyventory is a Python app to inventory your equipment.

## Install

Need python 3.10 or higher and [nicegui](https://nicegui.io/) installed.

```bash
pip install nicegui
```

Init and clone:
```shell
git init
git clone https://github.com/podzit/pyventory.git
```

## Customize your environment
Edit packages/env.py to custom your environment:
```python
HOST = 'your_server_ip'
PORT = 8091 # Or another custom port
INVOICE_LINK = 'invoices' # Name of directory for invoices
PICTURE_LINK = 'pictures' # Name of directory for pictures
LANGUAGE = 'fr' # 'fr' or 'eng'
import_dump = True # Do you want to import dump file ?
BACKUP_DAYS = 15 # How much daily backup do you want to keep?
```

## First run
First launch of main.py create database, invoices and pictures directories and import data from existing packages/dump file if you set import_dump to True in packages/env.py

## Start app


```python
python3 ./main.py
```

And go to http://your_server_ip:8091/main

## Auto backup

Use save_db.py in your daily cron to auto backup. 

```python
python3 ./save_db.py
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

If you want to start service at boot :

```shell
sudo systemctl enable pyventory.service
```

## Import data once again ?

Stop app, remove packages/import_tmp file, set import_dump to True in packages/env.py and start app.

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.
