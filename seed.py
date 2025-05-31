import sqlite3
from datetime import datetime, timedelta
import random

# ----------------------------------------
# Sample data: Blog posts and tags
# ----------------------------------------

# Each post has a title, description and content.
sample_posts = [
    {
        "title": "Exploring the Unknown",
        "description": "Dive into the mysteries of the unknown.",
        "content": "The unknown is a vast and fascinating space. We often fear what we don't understand, but curiosity can lead us to incredible discoveries. This post shares personal thoughts on venturing beyond the familiar."
    },
    {
        "title": "A Journey Through Code",
        "description": "An adventure through lines of code.",
        "content": "Coding is a creative journey filled with problem-solving and exploration. In this post, I reflect on the challenges and victories that come with learning new programming languages."
    },
    {
        "title": "The Hidden Life of Data",
        "description": "Discover the secret life of your data.",
        "content": "Data is everywhere, but we rarely stop to consider its journey. This post explores how data moves through systems, how it's transformed, and how it impacts our lives."
    },
    {
        "title": "Why We Write",
        "description": "Why we write, and how it shapes us.",
        "content": "Writing is a way to connect, to express, and to make sense of the world. Here are my reflections on why writing is important and how it has shaped my personal growth."
    },
    {
        "title": "Understanding Flask Basics",
        "description": "Mastering the basics of Flask.",
        "content": "Flask is a lightweight Python framework that makes web development approachable. This post covers the core concepts that every beginner should know when getting started with Flask."
    },
    {
        "title": "10 Tips for Clean Code",
        "description": "Ten practical tips for writing cleaner code.",
        "content": "Writing clean code is an art and a discipline. In this post, I share 10 actionable tips that have helped me write more maintainable and readable code."
    },
    {
        "title": "The Art of Debugging",
        "description": "Debug like a pro and find hidden bugs.",
        "content": "Debugging is not just about fixing errors—it's about understanding problems deeply. I share strategies and techniques that have helped me become a better problem solver."
    },
    {
        "title": "Creating Powerful Templates",
        "description": "Learn the secrets of powerful templates.",
        "content": "Templates can bring your project to life. This post discusses best practices for creating reusable, dynamic templates in your web applications."
    },
    {
        "title": "What is a Backend?",
        "description": "An introduction to backend development.",
        "content": "Backend development is the engine of modern web apps. Here’s a beginner-friendly guide that explains what backend development is and why it’s important."
    },
    {
        "title": "Jinja2 Magic Tricks",
        "description": "Jinja2 can do more than you think!",
        "content": "Jinja2 is a powerful templating engine. This post reveals some lesser-known features and techniques you can use to supercharge your Flask projects."
    },
]

# A list of predefined tags for the blog posts.
sample_tags = ["flask", "python", "backend", "jinja2", "sqlite", "blog", "project", "debugging"]

# ----------------------------------------
# Database connection
# ----------------------------------------

# Connect to the SQLite database file (blog.db)
conn = sqlite3.connect("blog.db")
cursor = conn.cursor()


# ----------------------------------------
# Clear existing data (to avoid duplicates)
# ----------------------------------------

# Delete all existing records from tables
cursor.execute("DELETE FROM post_tags")
cursor.execute("DELETE FROM comments")
cursor.execute("DELETE FROM tags")
cursor.execute("DELETE FROM posts")


# ----------------------------------------
# Insert tags into the database
# ----------------------------------------

# Insert each tag into the tags table and store its ID
tag_ids = {}
for tag in sample_tags:
    cursor.execute("INSERT INTO tags (name) VALUES (?)", (tag,))
    tag_ids[tag] = cursor.lastrowid


# ----------------------------------------
# Insert posts into the database
# ----------------------------------------

# Insert posts
for i, post in enumerate(sample_posts):
    # Generate a unique publication date for each post, spaced out by days
    pub_date = (datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d')

    # Insert the post into the posts table
    cursor.execute(
        "INSERT INTO posts (title, description, content, pub_date) VALUES (?, ?, ?, ?)",
        (post["title"], post["description"], post["content"], pub_date)
    )
    post_id = cursor.lastrowid

    # Assign 2–3 random tags to each post
    for tag in random.sample(sample_tags, k=3):
        cursor.execute("INSERT INTO post_tags (post_id, tag_id) VALUES (?, ?)",
                       (post_id, tag_ids[tag]))


# ----------------------------------------
# Finalize changes and close connection
# ----------------------------------------

conn.commit()
conn.close()

print("🌱 Seed data with unique, natural content and descriptions inserted!")
