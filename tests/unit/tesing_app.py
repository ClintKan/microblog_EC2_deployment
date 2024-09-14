import pytest
import requests

@pytest.fixture
def base_url():
    return "http://3.141.40.42"

def test_get_request(base_url):
    response = requests.get(f"{base_url}/explores")
    assert response.status_code == 200

# def test_post_request(base_url):
#     payload = {"title": "foo", "body": "bar", "userId": 1}
#     response = requests.post(f"{base_url}/posts", json=payload)
#     assert response.status_code == 201
#     assert response.json()['title'] == "foo"