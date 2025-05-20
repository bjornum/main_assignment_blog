import pytest
from app import create_app

# Setup test client using Flask's test interface
@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True

    with app.test_client() as client:
        yield client

# E2E Test: Homepage should load successfully and contain the blog section
def test_homepage_loads(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"All Blog Posts" in response.data

# E2E Test: Add a comment to an existing post (assumes post ID 1 exists)
def test_post_comment(client):
    response = client.post("/post/1", data={
        "title": "Test Comment",
        "content": "This is a test comment"
    }, follow_redirects=True)

    assert b"Comment added!" in response.data
