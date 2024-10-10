import pytest
from app import create_app
from flask import json

@pytest.fixture
def app():
    app = create_app()
    app.config['TESTING'] = True
    return app

@pytest.fixture
def client(app):
    return app.test_client()

def test_example_route(client):
    response = client.post('/example', json={"key": "value"}, headers={"Authorization": "mysecrettoken"})
    data = json.loads(response.data)
    assert response.status_code == 200
    assert data['status'] == 'success'
    assert data['data']['received_data'] == {"key": "value"}

def test_example_route_unauthorized(client):
    response = client.post('/example', json={"key": "value"})
    data = json.loads(response.data)
    assert response.status_code == 401
    assert data['message'] == 'Token is missing!'

def test_get_user(client):
    response = client.get('/user/1', headers={"Authorization": "mysecrettoken"})
    data = json.loads(response.data)
    assert response.status_code == 200
    assert data['status'] == 'success'
    assert data['data']['user_id'] == 1
    assert data['data']['name'] == 'John Doe'