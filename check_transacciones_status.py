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

print('=== ESTADO ACTUAL DE TRANSACCIONES ===')
print(f'Total de transacciones: {TransaccionFinanciera.objects.count()}')

# Ver transacciones por empresa
print('\nTransacciones por empresa:')
for item in TransaccionFinanciera.objects.values('id_empresa').annotate(count=Count('id_transaccion')).order_by('-count'):
    print(f'Empresa {item["id_empresa"]}: {item["count"]} transacciones')

# Ver las últimas 5 transacciones
print('\nÚltimas 5 transacciones:')
for tf in TransaccionFinanciera.objects.order_by('-fecha_hora_transaccion')[:5]:
    print(f'ID: {tf.id_transaccion}, Empresa: {tf.id_empresa}, Tipo: {tf.tipo_transaccion}, Monto: {tf.monto_transaccion} {tf.id_moneda_transaccion.codigo_iso}, Fecha: {tf.fecha_hora_transaccion}')