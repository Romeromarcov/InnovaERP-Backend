#!/usr/bin/env python
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
django.setup()

from apps.core.models import Empresa

print('Empresas existentes:')
for e in Empresa.objects.all()[:10]:
    print(f'ID: {e.id_empresa}, Nombre: {e.nombre_legal}')

# Verificar si hay una empresa con nombre "InnovaERP"
innova_erp = Empresa.objects.filter(nombre_legal='InnovaERP').first()
if innova_erp:
    print(f'\nEmpresa InnovaERP encontrada: ID={innova_erp.id_empresa}')
else:
    print('\nNo se encontró empresa con nombre InnovaERP')