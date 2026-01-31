# Script para verificar estado de tasas BCV
# Ejecutar para verificar si las tasas están actualizadas

Write-Host "=== Verificación de Tasas BCV ===" -ForegroundColor Cyan
Write-Host "Fecha actual: $(Get-Date)" -ForegroundColor Yellow
Write-Host ""

# Ejecutar consulta de tasas
Write-Host "Consultando tasas en base de datos..." -ForegroundColor Green
& "C:\Users\PC\innovaerp\.venv\Scripts\python.exe" manage.py shell -c "
from apps.finanzas.models import TasaCambio
from datetime import date, timedelta

# Buscar tasas del día actual
tasas_hoy = TasaCambio.objects.filter(
    tipo_tasa='OFICIAL_BCV',
    fecha_tasa=date.today()
)

# Buscar tasas del día anterior si no hay de hoy
if not tasas_hoy.exists():
    tasas_hoy = TasaCambio.objects.filter(
        tipo_tasa='OFICIAL_BCV',
        fecha_tasa=date.today() - timedelta(days=1)
    )

print(f'Tasas encontradas: {tasas_hoy.count()}')
for tasa in tasas_hoy:
    dias_antiguedad = (date.today() - tasa.fecha_tasa).days
    estado = '✅ ACTUAL' if dias_antiguedad == 0 else f'⚠️ {dias_antiguedad} días de antigüedad'
    print(f'{tasa.id_moneda_origen.codigo_iso}->{tasa.id_moneda_destino.codigo_iso}: {tasa.valor_tasa} ({estado})')
"