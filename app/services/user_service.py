import bcrypt
from pathlib import Path
from app.data.users import get_user_by_username, insert_user
from app.data.db import connect_database

def register_user(username, password, role='user'):
    """Register a new user with a secure hashed password"""
    if get_user_by_username(username):
        return False, "User already exists."

    password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    insert_user(username, password_hash, role)
    return True, f"User '{username}' registered successfully."

def login_user(username, password):
    """Check the login credentials"""
    user = get_user_by_username(username)
    if not user:
        return False, "User not found."

    stored_hash = user[2]  # column 2 is the password_hash
    if bcrypt.checkpw(password.encode('utf-8'), stored_hash.encode('utf-8')):
        return True, "Login successful."
    return False, "Incorrect password."

def migrate_users_from_file(filepath='DATA/users.txt'):
    """Move old users from text file into the database"""
    file = Path(filepath)
    if not file.exists():
        return "No users.txt file found."

    conn = connect_database()
    c = conn.cursor()
    count = 0
    for line in file.read_text().splitlines():
        if not line.strip():
            continue
        username, password, role = line.strip().split(',')
        password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        c.execute(
            "INSERT OR IGNORE INTO users (username, password_hash, role) VALUES (?, ?, ?)",
            (username, password_hash, role)
        )
        count += 1
    conn.commit()
    conn.close()
    return f"Migrated {count} users from file."
