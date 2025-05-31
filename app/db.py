import sqlite3
from flask import current_app, g
import click
from flask.cli import with_appcontext

# Get a connection to the SQLite database
def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            # Ensures proper type detection (like dates)
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        # Allows row access by column name
        g.db.row_factory = sqlite3.Row
    return g.db

# Close the database connection at the end of the request
def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

# Initialize the database by running the schema.sql file
def init_db():
    db = get_db()
    with open('schema.sql') as f:
        db.executescript(f.read())

# Defining a custom Flask CLI command: `flask init-db`
@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')

# Register the database functions with the Flask app
def init_app(app):
    # Ensure the database connection is closed after each request
    app.teardown_appcontext(close_db)

    # Register the custom CLI command `flask init-db` with the app
    app.cli.add_command(init_db_command)
