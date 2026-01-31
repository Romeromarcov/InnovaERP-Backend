# Script de PowerShell para actualizar tasas de cambio BCV
Set-Location 'C:\Users\PC\innovaerp'
& '.\.venv\Scripts\Activate.ps1'
Set-Location 'backend'
python manage.py update_bcv_exchange >> logs\update_bcv_exchange.log 2>&1
