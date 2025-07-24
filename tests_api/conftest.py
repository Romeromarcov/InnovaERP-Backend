import pytest
from django.contrib.auth import get_user_model
from apps.core.models import Empresa, Moneda

@pytest.fixture
def test_user(db):
    # Crea una moneda y empresa requeridas por el modelo multi-tenant
    moneda = Moneda.objects.create(nombre="Dólar", codigo="USD", simbolo="$", es_base=True)
    empresa = Empresa.objects.create(nombre="Empresa Test", rif="J123456789", moneda_base=moneda)
    User = get_user_model()
    user = User.objects.create_user(
        username="testuser",
        password="testpass123",
        email="testuser@example.com",
        empresa=empresa,
        moneda=moneda,
        is_active=True
    )
    return user
