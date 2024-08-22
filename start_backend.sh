#!/bin/bash
cd /home/ozkanerozcan/ftp/upload/drf-quasar
source env/bin/activate
cd backend
python manage.py runserver_plus 185.95.164.18:8000  --cert-file ssl/server.crt --key-file ssl/server.key