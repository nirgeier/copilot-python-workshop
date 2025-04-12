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
    """Test getting all superheroes returns list and 200 status"""
    response = client.get('/superheroes/all')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert isinstance(data, list)

def test_get_all_superheroes_data_validation(client):
    """Test that all superheroes have required fields"""
    response = client.get('/superheroes/all')
    data = json.loads(response.data)
    required_fields = ['id', 'name', 'powerstats']
    
    for hero in data:
        for field in required_fields:
            assert field in hero, f"Hero missing required field: {field}"
        # Validate powerstats structure
        assert isinstance(hero['powerstats'], dict)
        assert all(stat in hero['powerstats'] for stat in 
                  ['intelligence', 'strength', 'speed', 'durability', 'power', 'combat'])

def test_get_superhero_by_valid_id(client):
    """Test getting superhero by valid ID returns hero data and 200 status"""
    response = client.get('/superheroes/1')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert isinstance(data, dict)
    assert 'id' in data
    assert data['id'] == 1

def test_get_superhero_by_invalid_id(client):
    """Test getting superhero by invalid ID returns 404 error"""
    response = client.get('/superheroes/999')
    assert response.status_code == 404
    data = json.loads(response.data)
    assert 'error' in data
    assert data['error'] == 'Superhero not found'

def test_get_superhero_by_non_numeric_id(client):
    """Test getting superhero with non-numeric ID returns 404"""
    response = client.get('/superheroes/abc')
    assert response.status_code == 404

def test_get_powerstats_by_valid_id(client):
    """Test getting powerstats for valid hero ID returns stats and 200 status"""
    response = client.get('/superheroes/1/powerstats')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert isinstance(data, dict)
    expected_stats = ['intelligence', 'strength', 'speed', 'durability', 'power', 'combat']
    for stat in expected_stats:
        assert stat in data

def test_get_powerstats_by_invalid_id(client):
    """Test getting powerstats for invalid hero ID returns 404 error"""
    response = client.get('/superheroes/999/powerstats')
    assert response.status_code == 404
    data = json.loads(response.data)
    assert 'error' in data
    assert data['error'] == 'Superhero not found'

def test_get_powerstats_values_valid_range(client):
    """Test that powerstats values are within valid range (0-100)"""
    response = client.get('/superheroes/1/powerstats')
    data = json.loads(response.data)
    
    for stat, value in data.items():
        assert isinstance(value, (int, float)), f"{stat} should be numeric"
        assert 0 <= value <= 100, f"{stat} should be between 0 and 100"

def test_empty_superheroes_list_handling(client, mocker):
    """Test handling of empty superheroes list"""
    # Mock the superheroes list to be empty
    mocker.patch('app.app.superheroes', [])
    
    response = client.get('/superheroes/all')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert isinstance(data, list)
    assert len(data) == 0

def test_malformed_superhero_id(client):
    """Test handling of malformed superhero ID"""
    response = client.get('/superheroes/0')
    assert response.status_code == 404
    data = json.loads(response.data)
    assert data['error'] == 'Superhero not found'