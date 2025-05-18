# To help populate the database with some initial data
import sqlite3
from datetime import datetime, timedelta
import random

# Sample data
sample_titles = [
    "Exploring the Unknown", "A Journey Through Code", "The Hidden Life of Data",
    "Why We Write", "Understanding Flask Basics", "10 Tips for Clean Code",
    "The Art of Debugging", "Creating Powerful Templates", "What is a Backend?", "Jinja2 Magic Tricks"
]

sample_tags = ["flask", "python", "backend", "jinja2", "sqlite", "blog", "project", "debugging"]

# Connect to the database
conn = sqlite3.connect("blog.db")
cursor = conn.cursor()

# Clear old data (optional)
cursor.execute("DELETE FROM post_tags")
cursor.execute("DELETE FROM comments")
cursor.execute("DELETE FROM tags")
cursor.execute("DELETE FROM posts")

# Insert tags
tag_ids = {}
for tag in sample_tags:
    cursor.execute("INSERT INTO tags (name) VALUES (?)", (tag,))
    tag_ids[tag] = cursor.lastrowid

# Insert posts
for i, title in enumerate(sample_titles):
    content = f"This is the body of the blog post titled '{title}'. " * 5
    pub_date = (datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d')
    
    cursor.execute("INSERT INTO posts (title, content, pub_date) VALUES (?, ?, ?)",
                   (title, content, pub_date))
    post_id = cursor.lastrowid

    # Assign 2–3 random tags to each post
    for tag in random.sample(sample_tags, k=3):
        cursor.execute("INSERT INTO post_tags (post_id, tag_id) VALUES (?, ?)",
                       (post_id, tag_ids[tag]))

conn.commit()
conn.close()

print("🌱 Seed data inserted!")