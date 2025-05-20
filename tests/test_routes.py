import pytest
from app import create_app
from flask import g

# Setup a Flask test app instance
@pytest.fixture
def app():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SECRET_KEY'] = 'test'
    return app

# Create a test client for sending HTTP requests
@pytest.fixture
def client(app):
    return app.test_client()

# Route Protection: Guest access to admin-only route should show restriction
def test_create_post_redirects_for_guest(client):
    response = client.get('/create', follow_redirects=True)
    assert response.status_code == 200
    assert b'You do not have permission' in response.data

# Admin Access: Simulate admin session and ensure access to /create
def test_create_post_allowed_for_admin(client, app):
    with client.session_transaction() as sess:
        sess['user_id'] = 1
        sess['username'] = 'admin'
        sess['role'] = 'admin'

    response = client.get('/create')
    assert response.status_code == 200
    assert b'Create New Blog Post' in response.data

# 404 Handling: Accessing a nonexistent post should return 404
def test_404_for_nonexistent_post(client):
    response = client.get('/post/99999')
    assert response.status_code == 404
    assert b'post not found' in response.data.lower()

# Homepage: Should load and contain blog post section
def test_homepage(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'All Blog Posts' in response.data

# Tag Page: Should display posts for a given tag
def test_tag_page(client):
    response = client.get('/tags/flask')
    assert response.status_code == 200
    assert b'Posts tagged with' in response.data