import pytest
from flask import Flask
from seenons_api.main import api

@pytest.fixture
def client():
    with api.test_client() as client:
        yield client

def test_no_database_connection(mocker, client):
    # Mock the database connection to raise an exception
    mock_open_db = mocker.patch('seenons_api.main.open_db')
    mock_open_db.side_effect = Exception("Database connection failed")
    
    response = client.get('/streams/?postalcode=1234AB')
    assert response.status_code == 500
    assert 'Database connection failed' in str(response.data)

def test_get_waste_streams_success(mocker, client):
    # Mock the database connection
    mock_open_db = mocker.patch('seenons_api.main.open_db')
    mock_open_db.return_value = mocker.MagicMock()
    
    # Mock the get_postcode function
    mock_get_postcode = mocker.patch('seenons_api.main.get_postcode')
    mock_get_postcode.return_value = '1234AB'
    
    # Mock the search_database function
    mock_search_database = mocker.patch('seenons_api.main.search_database')
    mock_search_database.return_value = [
        {
            'Id': 1,
            'Name': 'Provider 1',
            'Provider': 'Provider 1',
            'Asset': 'Asset 1',
            'Postal range': '1234AB',
            'Available days': 'Monday',
            'Time slots': '08:00-12:00'
        }
    ]
    
    response = client.get('/streams/?postalcode=1234AB')
    assert response.status_code == 200
    assert 'Provider 1' in str(response.data)

def test_get_waste_streams_invalid_postcode(mocker, client):
    # Mock the database connection
    mock_open_db = mocker.patch('seenons_api.main.open_db')
    mock_open_db.return_value = mocker.MagicMock()
    
    # Mock the get_postcode function to raise ValueError
    mock_get_postcode = mocker.patch('seenons_api.main.get_postcode')
    mock_get_postcode.side_effect = ValueError("Invalid postal code")
    
    response = client.get('/streams/?postalcode=invalid')
    assert response.status_code == 400
    assert 'Invalid postal code' in str(response.data)

def test_get_waste_streams_no_data_found(mocker, client):
    # Mock the database connection
    mock_open_db = mocker.patch('seenons_api.main.open_db')
    mock_open_db.return_value = mocker.MagicMock()
    
    # Mock the get_postcode function
    mock_get_postcode = mocker.patch('seenons_api.main.get_postcode')
    mock_get_postcode.return_value = '1234AB'
    
    # Mock the search_database function to return no results
    mock_search_database = mocker.patch('seenons_api.main.search_database')
    mock_search_database.return_value = []
    
    response = client.get('/streams/?postalcode=1234AB')
    assert response.status_code == 404
    assert 'No data found for the given postal code' in str(response.data)