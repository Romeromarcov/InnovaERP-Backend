# Script para crear tarea programada de actualización de tasas BCV
# Ejecutar como administrador

$taskName = "InnovaERP_Update_BCV_Exchange"
$scriptPath = "C:\Users\PC\innovaerp\backend\update_bcv_exchange.bat"

# Verificar que el archivo .bat existe
if (!(Test-Path $scriptPath)) {
    Write-Host "Error: No se encuentra el archivo $scriptPath" -ForegroundColor Red
    exit 1
}

# Eliminar tarea existente si existe
if (Get-ScheduledTask -TaskName $taskName -ErrorAction SilentlyContinue) {
    Unregister-ScheduledTask -TaskName $taskName -Confirm:$false
    Write-Host "Tarea anterior eliminada." -ForegroundColor Yellow
}

# Crear la tarea programada con configuración mejorada
$action = New-ScheduledTaskAction -Execute $scriptPath
$trigger = New-ScheduledTaskTrigger -Daily -At 6am
$settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable -MultipleInstances IgnoreNew -ExecutionTimeLimit (New-TimeSpan -Hours 1)

# Registrar la tarea sin especificar principal (usará el usuario actual por defecto)
Register-ScheduledTask -TaskName $taskName -Action $action -Trigger $trigger -Settings $settings -Description "Actualización automática de tasas de cambio BCV para InnovaERP - Se ejecuta cuando esté disponible"

Write-Host "Tarea programada '$taskName' creada exitosamente con configuración mejorada." -ForegroundColor Green
Write-Host "La tarea se ejecutará diariamente a las 6:00 AM o cuando la PC esté disponible." -ForegroundColor Green