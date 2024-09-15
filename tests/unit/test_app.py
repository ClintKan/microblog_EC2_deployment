import pytest
import requests

@pytest.fixture
def base_url():
    return "http://3.144.229.235"

def test_get_home(base_url):
     response = requests.get(f"{base_url}/", timeout=3)
     assert response.status_code == 200

def test_get_login(base_url):
     response = requests.get(f"{base_url}/auth/login", timeout=3)
     assert response.status_code == 200

def test_get_explore(base_url):
    response = requests.get(f"{base_url}/explore", timeout=3)
    assert response.status_code == 200

# nice 3 test functions