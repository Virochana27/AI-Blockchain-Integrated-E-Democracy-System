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
