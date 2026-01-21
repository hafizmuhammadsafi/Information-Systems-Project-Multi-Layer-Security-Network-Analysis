from database import *
from otp import generate_otp, send_email, hash_password, check_password
from datetime import datetime
import re

OTP_EXPIRY_MINUTES = 1
BLOCK_MINUTES = 3
MAX_ATTEMPTS = 3

def is_strong_password(password):
    """Checks for 8+ chars, Uppercase, Lowercase, Number, and symbols (_ - @ !)"""
    if len(password) < 8: return False
    if not re.search(r"[a-z]", password): return False
    if not re.search(r"[A-Z]", password): return False
    if not re.search(r"[0-9]", password): return False
    if not re.search(r"[_@!-]", password): return False
    return True


# --- EXISTING FUNCTIONS (Login, Signup, Forgot, Verify) ---
def login_backend(email, password):
    user = get_user_by_email(email)
    if not user: return {"status": "error", "message": "Email not found"}

    if user['blocked_until']:
        blocked_until = datetime.strptime(user['blocked_until'], "%Y-%m-%d %H:%M:%S.%f")
        now = datetime.now()
        if now < blocked_until:
            remaining = int((blocked_until - now).total_seconds())
            return {"status": "blocked", "remaining_time": remaining}
        else:
            unblock_user(user['id'])

    if not check_password(password, user['password_hash']):
        new_attempts = user['attempts'] + 1
        update_attempts(user['id'], new_attempts)
        if new_attempts >= MAX_ATTEMPTS:
            block_user(user['id'], BLOCK_MINUTES)
            return {"status": "blocked", "remaining_time": BLOCK_MINUTES * 60}
        return {"status": "wrong"}

    reset_attempts(user['id'])
    otp = generate_otp()
    store_otp(user['id'], otp, OTP_EXPIRY_MINUTES)
    send_email(email, "Login OTP", f"Your OTP is {otp}")
    return {"status": "otp_sent", "email": email}

def verify_otp_backend(email, user_otp):
    user = get_user_by_email(email)
    if not user: return {"status": "error", "message": "User not found"}

    db_otp_data = get_latest_otp(user['id'])
    if not db_otp_data: return {"status": "error", "message": "No OTP generated"}

    stored_otp, expires_str = db_otp_data
    expires_at = datetime.strptime(expires_str, "%Y-%m-%d %H:%M:%S.%f")

    if datetime.now() > expires_at:
        return {"status": "error", "message": "OTP Expired"}

    if stored_otp == user_otp:
        mark_user_verified(user['id'])
        return {"status": "ok", "username": user['username']}
    else:
        return {"status": "error", "message": "Invalid OTP"}

def signup_backend(name, email, password):
    if get_user_by_email(email):
        return {"status": "error", "message": "Email already exists"}

    hashed = hash_password(password)
    result = add_user(name, email, hashed)

    if result["status"] == "error":
        return result

    user = get_user_by_email(email)
    if not user:
        return {"status": "error", "message": "User fetch failed"}

    otp = generate_otp()
    store_otp(user["id"], otp, OTP_EXPIRY_MINUTES)
    send_email(email, "Signup OTP", f"Your OTP is {otp}")

    return {"status": "success"}


def forgot_backend(email):
    user = get_user_by_email(email)
    if not user: return {"status": "error", "message": "Email not found"}
    otp = generate_otp()
    store_otp(user['id'], otp, OTP_EXPIRY_MINUTES)
    send_email(email, "Password Reset OTP", f"Your OTP is {otp}")
    return {"status": "ok"}

def reset_password_backend(email, new_password):
    user = get_user_by_email(email)
    if not user: return {"status": "error", "message": "User not found"}
    hashed = hash_password(new_password)
    update_password_by_email(email, hashed)
    return {"status": "success"}

# --- NEW FUNCTION ---
def resend_otp_backend(email):
    user = get_user_by_email(email)
    if not user:
        return {"status": "error", "message": "User not found"}
    
    # Generate NEW OTP
    otp = generate_otp()
    # This overwrites/adds to the DB, making previous OTPs effectively obsolete for this new validity period
    store_otp(user['id'], otp, OTP_EXPIRY_MINUTES)
    
    send_email(email, "Resend OTP Code", f"Your new OTP is {otp}. Valid for 1 minute.")
    return {"status": "ok"}