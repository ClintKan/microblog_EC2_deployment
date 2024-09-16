import pytest
import requests
from microblog import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        with app.app_context():
            yield client

def test_get_home(client):
     response = client.get("/", follows_redirect=True)
     assert response.status_code == 302

def test_get_login(client):
     response = client.get("/auth/login", follows_redirect=True)
     assert response.status_code == 200

def test_get_explore(client):
    response = client.get("/explore", follows_redirect=True)
    assert response.status_code == 200

# nice 3 test functions
