from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.utils.db import get_db

issues_bp = Blueprint("issues", __name__)

@issues_bp.route("/", methods=["POST"])
@jwt_required()
def raise_issue():
    data = request.json
    db = get_db()

    db.table("issues").insert({
        "raised_by": get_jwt_identity(),
        "constituency_id": data["constituency_id"],
        "description": data["description"]
    }).execute()

    return {"msg": "Issue raised"}
