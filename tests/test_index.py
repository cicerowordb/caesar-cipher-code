import time
import pytest
from index import app

TEST_LOAD_PERFORMANCE_ITERATIONS = 100
TEST_LOAD_PERFORMANCE_MAX_DURATION = 0.2 #seconds

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_get_route(client):
    """Tests if the GET route displays the form correctly."""
    response = client.get('/')
    assert response.status_code == 200
    assert b"Text: <input type=" in response.data

def test_post_route_correct_data(client):
    """Tests the Caesar cipher with correct data."""
    response = client.post('/', data={'text': 'abc', 'shift': '3'})
    assert b'Encrypted Text: def' in response.data

def test_post_route_non_numeric_shift(client):
    """Tests input validation with a non-numeric shift."""
    response = client.post('/', data={'text': 'abc', 'shift': 'xyz'})
    assert b'Shift must be an integer.' in response.data

def test_post_route_missing_fields(client):
    """Tests validation when fields are missing."""
    # Testing without sending 'text'
    response = client.post('/', data={'shift': '3'})
    assert b'Please fill out all fields.' in response.data

    # Testing without sending 'shift'
    response = client.post('/', data={'text': 'abc'})
    assert b'Please fill out all fields.' in response.data

def test_post_route_extreme_shift(client):
    """Tests the Caesar cipher with an extremely high shift value."""
    high_shift_response = client.post('/', data={'text': 'abc', 'shift': '999'})
    assert b'Encrypted Text:' in high_shift_response.data
    low_shift_response = client.post('/', data={'text': 'abc', 'shift': '-999'})
    assert b'Encrypted Text:' in low_shift_response.data

def test_post_route_special_characters(client):
    """Tests if special characters and numbers remain unchanged or are handled differently."""
    response = client.post('/', data={'text': '123!@#', 'shift': '1'})
    assert b'Encrypted Text: 234"A$' in response.data  # Ajuste o resultado esperado conforme a regra definida

def test_post_route_zero_shift(client):
    """Tests the Caesar cipher with zero shift."""
    response = client.post('/', data={'text': 'abc', 'shift': '0'})
    assert b'Encrypted Text: abc' in response.data

def test_post_route_negative_shift(client):
    """Tests the Caesar cipher with a negative shift."""
    response = client.post('/', data={'text': 'def', 'shift': '-3'})
    assert b'Encrypted Text: abc' in response.data

def test_post_route_negative_shift(client):
    """Tests the Caesar cipher with a negative shift."""
    response = client.post('/', data={'text': 'def', 'shift': '-3'})
    assert b'Encrypted Text: abc' in response.data

def test_post_route_data_persistence(client):
    """Tests that data does not persist between requests."""
    first_response = client.post('/', data={'text': 'abc', 'shift': '1'})
    second_response = client.post('/', data={'text': 'def', 'shift': '2'})
    assert first_response.data != second_response.data

def test_post_route_large_input(client):
    """Tests how the app handles very large inputs."""
    large_text = 'a' * 10000
    response = client.post('/', data={'text': large_text, 'shift': '1'})
    assert response.status_code == 200
    assert len(response.data) > 0
    assert b'Encrypted Text: bbbbbbbbbbbbbbb' in response.data

def test_post_route_unicode_characters(client):
    """Tests the cipher's handling of Unicode characters."""
    response = client.post('/', data={'text': '你好，世界', 'shift': '2'})
    assert response.status_code == 200

def test_unsupported_http_methods(client):
    """Tests the app's response to unsupported HTTP methods."""
    methods = ['PUT', 'DELETE', 'PATCH']
    for method in methods:
        response = client.open(path='/', method=method)
        assert response.status_code == 405  # 405 Method Not Allowed

def test_unexpected_query_params(client):
    """Tests handling of unexpected query parameters."""
    response = client.post('/?extra=unexpected', data={'text': 'abc', 'shift': '1'})
    assert response.status_code == 200
    assert b'Encrypted Text:' in response.data

def test_malformed_post_requests(client):
    """Tests the app's robustness against malformed POST requests."""
    malformed_data = 'text=abc&shift=one'
    response = client.post('/', data=malformed_data, content_type='application/x-www-form-urlencoded')
    assert b'ERROR' in response.data

def test_load_performance(client):
    """Tests application performance under high load."""
    start_time = time.time()

    for _ in range(TEST_LOAD_PERFORMANCE_ITERATIONS):
        response = client.post('/', data={'text': 'test', 'shift': '1'}, follow_redirects=True)
        assert response.status_code == 200

    end_time = time.time()
    duration = end_time - start_time

    assert duration < TEST_LOAD_PERFORMANCE_MAX_DURATION, "The test took too long to complete"
    print(f"[{TEST_LOAD_PERFORMANCE_ITERATIONS} requests in {duration:.2f} seconds]")
