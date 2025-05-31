import sqlite3
from werkzeug.security import generate_password_hash

# ----------------------------------------
# Connect to the SQLite database
# ----------------------------------------

# Connect to the existing blog database
conn = sqlite3.connect("blog.db")
cursor = conn.cursor()


# ----------------------------------------
# Create a simple admin user
# ----------------------------------------

# Defining admin username and password
username = "admin"
password = "admin123"

# Hashing the password for security (using Werkzeug)
hashed_password = generate_password_hash(password)

# Insert the admin user into the users table
cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
               (username, hashed_password, "admin"))


# ----------------------------------------
# Finalize changes and close the connection
# ----------------------------------------

conn.commit()
conn.close()

print("👤 Admin user created: admin / admin123")
