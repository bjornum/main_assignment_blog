import pytest
from app import create_app
from flask import g

# ----------------------------------------
# Setup: Flask App and Test Client Fixtures
# ----------------------------------------

@pytest.fixture
def app():
    # Create a Flask test application instance
    app = create_app()
    app.config['TESTING'] = True
    # Dummy secret key for sessions
    app.config['SECRET_KEY'] = 'test'
    return app

# Create a test client for sending HTTP requests
@pytest.fixture
def client(app):
    return app.test_client()


# ----------------------------------------
# Route Tests
# ----------------------------------------


# Test: Guest access to an admin-only route should show restriction message
def test_create_post_redirects_for_guest(client):
    response = client.get('/create', follow_redirects=True)
    assert response.status_code == 200
    assert b'You do not have permission' in response.data

# Test: Admin user should have access to /create page
def test_create_post_allowed_for_admin(client, app):
    # Simulate an admin session
    with client.session_transaction() as sess:
        sess['user_id'] = 1
        sess['username'] = 'admin'
        sess['role'] = 'admin'

    response = client.get('/create')
    assert response.status_code == 200
    assert b'Create New Blog Post' in response.data

# Test: going to an non-existent post should return a 404 page
def test_404_for_nonexistent_post(client):
    # Assumes this post ID does not exist
    response = client.get('/post/99999')
    assert response.status_code == 404
    assert b'post not found' in response.data.lower()

# Test: Homepage should load and display the blog post section
def test_homepage(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'All Blog Posts' in response.data

# Test: Tag page should display posts for a given tag
def test_tag_page(client):
    response = client.get('/tags/flask')
    assert response.status_code == 200
    assert b'Posts tagged with' in response.data