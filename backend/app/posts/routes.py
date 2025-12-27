from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.utils.db import get_db

posts_bp = Blueprint("posts", __name__)

@posts_bp.route("/", methods=["POST"])
@jwt_required()
def create_post():
    data = request.json
    db = get_db()

    db.table("posts").insert({
        "user_id": get_jwt_identity(),
        "constituency_id": data["constituency_id"],
        "post_type": data["post_type"],
        "content": data["content"]
    }).execute()

    return {"msg": "Post created"}
