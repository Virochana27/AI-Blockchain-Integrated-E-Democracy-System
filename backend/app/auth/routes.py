from flask import Blueprint, request
from flask_jwt_extended import create_access_token
from app.utils.db import get_db
from app.auth.services import verify_password


auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/login", methods=["POST"])
def login():
    if not request.is_json:
        return {"msg": "Request must be JSON"}, 415

    data = request.json
    db = get_db()

    res = db.table("users").select("*").eq("email", data["email"]).execute()
    if not res.data:
        return {"msg": "Invalid credentials"}, 401

    user = res.data[0]

    if not verify_password(user["password_hash"], data["password"]):
        return {"msg": "Invalid credentials"}, 401

    token = create_access_token(identity=user["id"])
    return {
        "access_token": token,
        "role": user["role"]
    }
