
from line_detector import create_app


def test_config():
    """Test if test config can be passed to app or not."""
    assert not create_app().testing
    assert create_app({'TESTING': True}).testing


def test_hello(client):
    response = client.get('/hello')
    assert response.data == b'Hello, World!'
