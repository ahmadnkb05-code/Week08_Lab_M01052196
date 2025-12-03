from app.data.db import connect_database

def get_user_by_username(username):
    """Find a single user by their username"""
    conn = connect_database()
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username = ?", (username,))
    row = c.fetchone()
    conn.close()
    return row

def insert_user(username, password_hash, role='user'):
    """Add a new user into the database"""
    conn = connect_database()
    c = conn.cursor()
    c.execute(
        "INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)",
        (username, password_hash, role)
    )
    conn.commit()
    conn.close()

def get_all_users():
    """See all the users"""
    conn = connect_database()
    c = conn.cursor()
    c.execute("SELECT id, username, role FROM users")
    rows = c.fetchall()
    conn.close()
    return rows

def delete_user(username):
    """Remove a user by name"""
    conn = connect_database()
    c = conn.cursor()
    c.execute("DELETE FROM users WHERE username = ?", (username,))
    conn.commit()
    conn.close()
