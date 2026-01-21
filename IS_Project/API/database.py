import sqlite3
import time
from datetime import datetime
from logger import log_event

DB = "users.db"

def get_connection():
    conn = sqlite3.connect(DB, timeout=20, check_same_thread=False)
    conn.execute("PRAGMA foreign_keys = ON;")
    conn.execute("PRAGMA journal_mode = WAL;")
    conn.execute("PRAGMA synchronous = NORMAL;")
    return conn

def init_db():
    conn = get_connection()
    cur = conn.cursor()
    
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            email TEXT UNIQUE,
            password_hash TEXT,
            verified INTEGER DEFAULT 0,
            attempts INTEGER DEFAULT 0,
            blocked_until TEXT
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS otp (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            otp TEXT,
            expires_at TEXT,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)

    conn.commit()
    conn.close()
    log_event("Database initialized.")

# --- USER FUNCTIONS ---

def add_user(username, email, password_hash):
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)",
            (username, email, password_hash)
        )
        conn.commit()
        conn.close()
        return {"status": "success"}

    except sqlite3.IntegrityError as e:
        if "users.email" in str(e):
            return {"status": "error", "message": "Email already exists"}
        if "users.username" in str(e):
            return {"status": "error", "message": "Username already exists"}
        return {"status": "error", "message": "Duplicate entry"}

    except Exception as e:
        log_event(f"Error adding user: {e}")
        return {"status": "error", "message": "Database failure"}


def get_user_by_email(email):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, username, email, password_hash, attempts, blocked_until, verified FROM users WHERE email=?", (email,))
    row = cur.fetchone()
    conn.close()

    if row:
        return {
            "id": row[0],
            "username": row[1],
            "email": row[2],
            "password_hash": row[3],
            "attempts": row[4],
            "blocked_until": row[5],
            "verified": row[6]
        }
    return None

def update_password_by_email(email, new_hash):
    conn = get_connection()
    conn.execute("UPDATE users SET password_hash=? WHERE email=?", (new_hash, email))
    conn.commit()
    conn.close()
    log_event(f"Password updated for {email}")

def mark_user_verified(user_id):
    conn = get_connection()
    conn.execute("UPDATE users SET verified=1 WHERE id=?", (user_id,))
    conn.commit()
    conn.close()

def update_attempts(user_id, attempts, blocked_until=None):
    conn = get_connection()
    try:
        if blocked_until is not None:
            conn.execute(
                "UPDATE users SET attempts=?, blocked_until=? WHERE id=?",
                (attempts, blocked_until, user_id)
            )
        else:
            conn.execute(
                "UPDATE users SET attempts=?, blocked_until=NULL WHERE id=?",
                (attempts, user_id)
            )
        conn.commit()
    except Exception as e:
        log_event(f"Update Attempts Error: {e}")
    finally:
        conn.close()


def reset_attempts(user_id):
    update_attempts(user_id, 0, None)

def block_user(user_id, block_minutes):
    blocked_until = datetime.fromtimestamp(time.time() + block_minutes*60).strftime("%Y-%m-%d %H:%M:%S.%f")
    update_attempts(user_id, 0, blocked_until)

def unblock_user(user_id):
    update_attempts(user_id, 0, None)

# --- OTP FUNCTIONS ---

def store_otp(user_id, otp, expiry_minutes=1):
    expires_at = datetime.fromtimestamp(
        time.time() + expiry_minutes * 60
    ).strftime("%Y-%m-%d %H:%M:%S.%f")

    conn = get_connection()
    try:
        conn.execute(
            "INSERT INTO otp (user_id, otp, expires_at) VALUES (?, ?, ?)",
            (user_id, otp, expires_at)
        )
        conn.commit()
    except Exception as e:
        log_event(f"OTP Store Error: {e}")
    finally:
        conn.close()

def get_latest_otp(user_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT otp, expires_at FROM otp WHERE user_id=? ORDER BY id DESC LIMIT 1", (user_id,))
    row = cur.fetchone()
    conn.close()
    return row