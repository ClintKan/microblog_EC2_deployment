import pytest
import requests

@pytest.fixture
def base_url():
    return "http://13.58.232.164"

def test_get_request(base_url):
    response = requests.get(f"{base_url}/")
    assert response.status_code == 200

def test_get_request(base_url):
    response = requests.get(f"{base_url}/auth/login")
    assert response.status_code == 200

def test_get_request(base_url):
    response = requests.get(f"{base_url}/explore")
    assert response.status_code == 200