import sqlite3
import os
import tempfile
import pytest
from app.db import get_db, init_db
from flask import Flask

# Setup a temporary Flask app with an isolated SQLite database for testing
@pytest.fixture
def test_app():
    # Create a temporary file to use as the database
    db_fd, db_path = tempfile.mkstemp()

    app = Flask(__name__)
    app.config['DATABASE'] = db_path
    app.config['TESTING'] = True
    app.secret_key = "test"

    # Initialize the database schema
    with app.app_context():
        init_db()

    # Provide the app to the test
    yield app

    # Close DB connection before removing the file (Windows workaround)
    with app.app_context():
        get_db().close()

    os.close(db_fd)

# Integration Test: Insert a post and retrieve it from the DB
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
