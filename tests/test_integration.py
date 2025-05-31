import sqlite3
import os
import tempfile
import pytest
from app.db import get_db, init_db
from flask import Flask


# ----------------------------------------
# Setup: Create a temporary Flask app and isolated SQLite database for integration testing
# ----------------------------------------

@pytest.fixture
def test_app():
    # Create a temporary file to act as a separate database for tests
    db_fd, db_path = tempfile.mkstemp()

    # Create a Flask app instance with the test database
    app = Flask(__name__)
    # Use the temp database file
    app.config['DATABASE'] = db_path
    # Enable testing mode (disables error catching)
    app.config['TESTING'] = True
    # Set a dummy secret key for sessions
    app.secret_key = "test"

    # Initialize the schema in the test database
    with app.app_context():
        init_db()

    # Provide the app to the test
    yield app

    # Close DB connection before removing the file (Windows workaround)
    with app.app_context():
        get_db().close()

    # Close the file descriptor
    os.close(db_fd)


# ----------------------------------------
# Integration Test: Insert and retrieve a post in the database
# ----------------------------------------

def test_insert_and_fetch_post(test_app):
    with test_app.app_context():
        db = get_db()

        # Insert a test blog post
        db.execute("INSERT INTO posts (title, content, pub_date) VALUES (?, ?, DATE('now'))",
                   ("Test Post", "This is a test",))
        db.commit()

        # Fetch the inserted post and verify content
        result = db.execute("SELECT * FROM posts WHERE title = ?", ("Test Post",)).fetchone()
        assert result is not None
        assert result["content"] == "This is a test"
