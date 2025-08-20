import pytest
from app.app import app
import json

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_root_endpoint(client):
    """Test the root endpoint returns correct message"""
    response = client.get('/')
    assert response.status_code == 200
    assert b"Save the World!" in response.data