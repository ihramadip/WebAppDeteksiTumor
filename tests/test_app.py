import pytest
from app import app as flask_app

@pytest.fixture
def app():
    yield flask_app

@pytest.fixture
def client(app):
    return app.test_client()

def test_index_page_redirects_to_login(client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/' route is requested by an unauthenticated client
    THEN check that the client is redirected to the '/login' page
    """
    response = client.get('/', follow_redirects=False)
    # Check that the server sent a redirect status code
    assert response.status_code == 302
    # Check that the redirect location is the login page
    assert response.location.startswith('/login')

def test_login_page_loads(client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/login' route is requested (GET)
    THEN check that the response is valid and contains the correct title
    """
    response = client.get('/login')
    assert response.status_code == 200
    # Check for a more specific and stable element from the login page
    assert b"Login Aplikasi" in response.data
