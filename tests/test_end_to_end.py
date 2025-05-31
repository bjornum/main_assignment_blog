import pytest
from app import create_app

# ----------------------------------------
# Setup: Create a test client using Flask's testing interface
# Enabled testing mode (disables error catching, enables test signals)
# ----------------------------------------

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True

    # Use Flask's test client as a context manager
    with app.test_client() as client:
        yield client


# ----------------------------------------
# End-to-End (E2E) Tests
# ----------------------------------------

# Test: Homepage should load successfully and contain the blog section
def test_homepage_loads(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"All Blog Posts" in response.data

# Test: Add a comment to an existing post (assumes post ID 1 exists)
def test_post_comment(client):
    response = client.post("/post/1", data={
        "title": "Test Comment",
        "content": "This is a test comment"
    }, follow_redirects=True)

    # Confirm the flash message indicating success is shown
    assert b"Comment added!" in response.data
