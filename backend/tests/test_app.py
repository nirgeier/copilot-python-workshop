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

def test_get_all_superheroes(client):
    """Test getting all superheroes"""
    response = client.get('/superheroes/all')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert isinstance(data, list)
    assert len(data) == 3  # We know we have 3 heroes in our data
    assert all('id' in hero for hero in data)
    assert all('name' in hero for hero in data)
    assert all('powerstats' in hero for hero in data)

def test_get_superhero_by_id(client):
    """Test getting a specific superhero by ID"""
    # Test valid superhero
    response = client.get('/superheroes/1')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['name'] == 'A-Bomb'
    
    # Test invalid superhero ID
    response = client.get('/superheroes/999')
    assert response.status_code == 404
    data = json.loads(response.data)
    assert 'error' in data

def test_get_superhero_powerstats(client):
    """Test getting powerstats for a specific superhero"""
    # Test valid superhero
    response = client.get('/superheroes/2/powerstats')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert all(stat in data for stat in ['intelligence', 'strength', 'speed', 'durability', 'power', 'combat'])
    assert data['intelligence'] == 100  # Ant-Man's intelligence
    
    # Test invalid superhero ID
    response = client.get('/superheroes/999/powerstats')
    assert response.status_code == 404
    data = json.loads(response.data)
    assert 'error' in data