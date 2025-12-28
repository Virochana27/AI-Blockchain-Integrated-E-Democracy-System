from flask import Blueprint, request
from app.utils.db import get_db
from app.utils.decorators import role_required

elections_bp = Blueprint("elections", __name__)

@elections_bp.route("/", methods=["POST"])
@role_required("EC")
def create_election():
    data = request.json
    db = get_db()

    db.table("elections").insert({
        "constituency_id": data["constituency_id"],
        "status": "UPCOMING",
        "created_by": data["created_by"]
    }).execute()

    return {"msg": "Election created"}


@elections_bp.route("/constituencies", methods=["GET"])
@role_required("EC")
def get_constituencies():
    db = get_db()
    res = db.table("constituencies").select("*").execute()
    return res.data

@elections_bp.route("/complaints/<constituency_id>", methods=["GET"])
@role_required("EC")
def get_ec_complaints(constituency_id):
    db = get_db()

    res = (
        db.table("ec_complaints")
        .select("id, message, status, created_at")
        .eq("constituency_id", constituency_id)
        .order("created_at", desc=True)
        .execute()
    )

    return res.data

