import pytest
import httpx
from django.urls import reverse

pytestmark = pytest.mark.django_db

BASE_URL = "http://localhost:8000/api/"
TOKEN_URL = "http://localhost:8000/api/token/"


def test_login_invalid_credentials():
    response = httpx.post(TOKEN_URL, data={"username": "wrong", "password": "wrong"})
    assert response.status_code == 401
    assert "access" not in response.json()

def test_login_valid(test_user):
    response = httpx.post(TOKEN_URL, data={"username": "testuser", "password": "testpass123"})
    assert response.status_code == 200
    assert "access" in response.json()
    assert "refresh" in response.json()
    token = response.json()["access"]
    # Probar acceso a endpoint protegido (usuarios)
    users_url = BASE_URL + "core/usuarios/"
    r = httpx.get(users_url, headers={"Authorization": f"Bearer {token}"})
    assert r.status_code in (200, 403)  # 200 si tiene permisos, 403 si no
