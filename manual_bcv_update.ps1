# Script alternativo: Actualización manual de tasas BCV
# Ejecutar cuando sea necesario si la tarea programada falla

Write-Host "=== Actualización Manual de Tasas BCV ===" -ForegroundColor Cyan
Write-Host "Fecha: $(Get-Date)" -ForegroundColor Yellow
Write-Host ""

# Cambiar al directorio del backend
Set-Location "C:\Users\PC\innovaerp\backend"

# Ejecutar el comando de actualización
Write-Host "Ejecutando actualización de tasas..." -ForegroundColor Green
& "C:\Users\PC\innovaerp\.venv\Scripts\python.exe" manage.py update_bcv_exchange

# Verificar resultado
if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Actualización completada exitosamente" -ForegroundColor Green
} else {
    Write-Host "❌ Error en la actualización" -ForegroundColor Red
}

# Mostrar últimas líneas del log
Write-Host ""
Write-Host "Últimas líneas del log:" -ForegroundColor Cyan
Get-Content "logs\update_bcv_exchange.log" -Tail 10