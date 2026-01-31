#!/usr/bin/env python
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()
user = User.objects.filter(username='admin').first()
if user:
    print(f'Usuario: {user.username}')
    empresas = user.empresas.all()
    print(f'Empresas asociadas ({empresas.count()}):')
    for empresa in empresas:
        print(f'  - ID: {empresa.id_empresa}, Nombre: {empresa.nombre_legal}')
else:
    print('Usuario admin no encontrado')