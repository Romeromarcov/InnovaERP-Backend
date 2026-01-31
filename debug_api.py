import os
import django
import json

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.test import Client
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

try:
    client = APIClient()
    User = get_user_model()
    user = User.objects.filter(is_superuser=True).first()
    if user:
        client.force_authenticate(user=user)
        response = client.get('/finanzas/plantillas-maestro-cajas/')
        print('Status:', response.status_code)
        if response.status_code == 200:
            data = response.json()
            print('Tipo de respuesta:', type(data))
            if isinstance(data, list) and len(data) > 0:
                print('Primer elemento:')
                print(json.dumps(data[0], indent=2, ensure_ascii=False))
            else:
                print('Respuesta:', data)
        else:
            print('Error:', response.content.decode())
    else:
        print('No hay usuario superusuario')
except Exception as e:
    print('Error:', str(e))
    import traceback
    traceback.print_exc()