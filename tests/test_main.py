import pytest
from app import create_app

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    
    with app.test_client() as client:
        yield client

def test_index_route(client):
    """Test the index route returns expected data"""
    response = client.get('/')
    assert response.status_code == 200
    data = response.get_json()
    assert data['app'] == 'Up to Date'
    assert data['version'] == '1.0.0'
    assert data['status'] == 'running'

def test_health_route(client):
    """Test the health check route"""
    response = client.get('/health')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'healthy'