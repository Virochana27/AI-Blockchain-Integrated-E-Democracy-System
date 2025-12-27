from flask import Blueprint, request
from app.utils.db import get_db
from app.auth.services import hash_password

users_bp = Blueprint("users", __name__)

@users_bp.route("/register", methods=["POST"])
def register():
    data = request.json
    db = get_db()

    user = {
        "name": data["name"],
        "email": data["email"],
        "password_hash": hash_password(data["password"]),
        "role": data["role"],
        "constituency_id": data.get("constituency_id")
    }

    db.table("users").insert(user).execute()
    return {"msg": "User registered successfully"}
