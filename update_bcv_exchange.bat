@echo off
cd /d C:\Users\PC\innovaerp\backend
"C:\Users\PC\innovaerp\.venv\Scripts\python.exe" manage.py update_bcv_exchange >> logs\update_bcv_exchange.log 2>&1
