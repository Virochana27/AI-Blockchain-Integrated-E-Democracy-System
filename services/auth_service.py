import hashlib
from flask import session
from supabase.auth import login_with_email_password, logout_user, extract_user_identity
from models.user import get_user_by_email
from utils.helpers import is_valid_email
from utils.helpers import normalize_role


# -----------------------------
# Authentication Service
# -----------------------------

def login_user(email: str, password: str):
    """
    Handles full login flow:
    - Supabase auth
    - User lookup in internal users table
    - Flask session setup
    """

    if not is_valid_email(email):
        raise ValueError("Invalid email format")

    # Authenticate with Supabase
    supabase_session = login_with_email_password(email, password)

    # Extract identity from Supabase JWT
    identity = extract_user_identity(supabase_session)

    # Fetch internal user record
    user = get_user_by_email(identity["email"])
    if not user or not user.get("is_active"):
        raise ValueError("User not found or inactive")

    # Store session data (used by decorators)
    session.clear()
    session["user_id"] = user["id"]
    session["email"] = user["email"]
    session["role"] = normalize_role(user["role"])
    session["state_id"] = user.get("state_id")
    session["district_id"] = user.get("district_id")
    session["constituency_id"] = user.get("constituency_id")
    session["booth_id"] = user.get("booth_id")

    return user


def logout_current_user():
    """
    Clears Flask session and Supabase auth
    """
    logout_user()
    session.clear()


# -----------------------------
# Password Utilities
# -----------------------------

def hash_password(password: str) -> str:
    """
    Hash password before storing in DB
    """
    return hashlib.sha256(password.encode("utf-8")).hexdigest()
