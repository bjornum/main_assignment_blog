import sqlite3
from werkzeug.security import generate_password_hash

# Connect to DB
conn = sqlite3.connect("blog.db")
cursor = conn.cursor()

# Create super simple admin account
username = "admin"
password = "admin123"
hashed_password = generate_password_hash(password)

cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
               (username, hashed_password, "admin"))

conn.commit()
conn.close()

print("👤 Admin user created: admin / admin123")
