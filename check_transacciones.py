#!/usr/bin/env python
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
django.setup()

from apps.finanzas.models import TransaccionFinanciera
from django.db.models import Count

print('Total transacciones:', TransaccionFinanciera.objects.count())
print('Transacciones por empresa (top 5):')
for item in TransaccionFinanciera.objects.values('id_empresa').annotate(count=Count('id_transaccion')).order_by('-count')[:5]:
    print(f'Empresa {item["id_empresa"]}: {item["count"]} transacciones')

# Verificar transacciones recientes
print('\nTransacciones recientes (últimas 5):')
for tf in TransaccionFinanciera.objects.order_by('-fecha_hora_transaccion')[:5]:
    print(f'ID: {tf.id_transaccion}, Empresa: {tf.id_empresa}, Tipo: {tf.tipo_transaccion}, Monto: {tf.monto_transaccion} {tf.id_moneda_transaccion.codigo_iso}')