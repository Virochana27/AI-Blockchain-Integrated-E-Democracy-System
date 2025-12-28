from flask import Blueprint, request
from flask_jwt_extended import get_jwt_identity
from app.utils.db import get_db
from app.utils.decorators import role_required

issues_bp = Blueprint("issues", __name__)

@issues_bp.route("/", methods=["GET"])
@role_required("VOTER")
def get_issues():
    db = get_db()
    user_id = get_jwt_identity()

    user = (
        db.table("users")
        .select("constituency_id")
        .eq("id", user_id)
        .single()
        .execute()
        .data
    )

    res = (
        db.table("issues")
        .select("id, description, status, created_at")
        .eq("constituency_id", user["constituency_id"])
        .order("created_at", desc=True)
        .execute()
    )

    return res.data
    
@issues_bp.route("/", methods=["POST"])
@role_required("VOTER")
def raise_issue():
    db = get_db()
    user_id = get_jwt_identity()
    data = request.json

    user = (
        db.table("users")
        .select("constituency_id")
        .eq("id", user_id)
        .single()
        .execute()
        .data
    )

    db.table("issues").insert({
        "raised_by": user_id,
        "constituency_id": user["constituency_id"],
        "description": data["description"]
    }).execute()

    return {"msg": "Issue raised"}, 201

@issues_bp.route("/complaint", methods=["POST"])
@role_required("VOTER")
def raise_ec_complaint():
    db = get_db()
    user_id = get_jwt_identity()
    data = request.json

    user = (
        db.table("users")
        .select("constituency_id")
        .eq("id", user_id)
        .single()
        .execute()
        .data
    )

    db.table("ec_complaints").insert({
        "raised_by": user_id,
        "constituency_id": user["constituency_id"],
        "message": data["message"]
    }).execute()

    return {"msg": "Complaint sent"}, 201

