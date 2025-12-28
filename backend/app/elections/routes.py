from flask import Blueprint, request
from app.utils.db import get_db
from app.utils.decorators import role_required
from flask_jwt_extended import get_jwt_identity
from datetime import datetime, timezone


elections_bp = Blueprint("elections", __name__)

# ------------------------------------------------------
# Helper: convert ISO string → UTC aware datetime
# ------------------------------------------------------
def to_utc(dt_str):
    if not dt_str:
        return None
    dt = datetime.fromisoformat(dt_str)
    return dt.replace(tzinfo=timezone.utc)


# ======================================================
# Create Election (Initial creation)
# ======================================================
@elections_bp.route("/", methods=["POST"])
@role_required("EC")
def create_election():
    data = request.json
    db = get_db()

    ec_id = get_jwt_identity()

    res = db.table("elections").insert({
        "constituency_id": data["constituency_id"],
        "status": "UPCOMING",
        "created_by": ec_id
    }).execute()

    return res.data[0], 201


# ======================================================
# Get all constituencies
# ======================================================
@elections_bp.route("/constituencies", methods=["GET"])
@role_required("EC")
def get_constituencies():
    db = get_db()
    return db.table("constituencies").select("*").execute().data


# ======================================================
# View EC complaints (constituency-wise)
# ======================================================
@elections_bp.route("/complaints/<constituency_id>", methods=["GET"])
@role_required("EC")
def get_ec_complaints(constituency_id):
    db = get_db()
    return (
        db.table("ec_complaints")
        .select("id, message, status, created_at")
        .eq("constituency_id", constituency_id)
        .order("created_at", desc=True)
        .execute()
        .data
    )


# ======================================================
# Get latest election by constituency
# ======================================================
@elections_bp.route("/by-constituency/<constituency_id>", methods=["GET"])
@role_required("EC")
def get_election_by_constituency(constituency_id):
    db = get_db()
    res = (
        db.table("elections")
        .select("*")
        .eq("constituency_id", constituency_id)
        .order("created_at", desc=True)
        .limit(1)
        .execute()
    )

    if not res.data:
        return {}, 200

    return res.data[0], 200


# ======================================================
# Update / Announce Election (Time-driven status)
# ======================================================
@elections_bp.route("/<election_id>", methods=["PUT"])
@role_required("EC")
def update_election(election_id):
    data = request.json
    db = get_db()

    # -----------------------------
    # 1. Save provided fields
    # -----------------------------
    update_data = {}

    for field in [
        "application_deadline",
        "voter_registration_deadline",
        "start_time",
        "end_time"
    ]:
        if field in data:
            update_data[field] = data[field]

    if update_data:
        db.table("elections").update(update_data).eq("id", election_id).execute()

    # -----------------------------
    # 2. Fetch updated election
    # -----------------------------
    election = (
        db.table("elections")
        .select(
            "application_deadline, voter_registration_deadline, start_time, end_time"
        )
        .eq("id", election_id)
        .single()
        .execute()
        .data
    )

    now = datetime.now(timezone.utc)

    application_deadline = to_utc(election["application_deadline"])
    voter_registration_deadline = to_utc(election["voter_registration_deadline"])
    start_time = to_utc(election["start_time"])
    end_time = to_utc(election["end_time"])

    # -----------------------------
    # 3. Compute correct status
    # -----------------------------
    status = "UPCOMING"

    if application_deadline and now < application_deadline:
        status = "NOMINATION_OPEN"

    elif (
        application_deadline
        and voter_registration_deadline
        and application_deadline <= now < voter_registration_deadline
    ):
        status = "VOTER_REGISTRATION"

    elif start_time and end_time and start_time <= now < end_time:
        status = "ONGOING"

    elif end_time and now >= end_time:
        status = "COMPLETED"

    # -----------------------------
    # 4. Update status
    # -----------------------------
    db.table("elections").update({
        "status": status
    }).eq("id", election_id).execute()

    return {"msg": "Election updated", "status": status}


# ======================================================
# Review Candidate Applications
# ======================================================
@elections_bp.route("/applications/<election_id>", methods=["GET"])
@role_required("EC")
def get_candidate_applications(election_id):
    db = get_db()
    return (
        db.table("candidate_applications")
        .select(
            """
            id,
            manifesto,
            status,
            applied_at,
            users (
                name,
                email
            )
            """
        )
        .eq("election_id", election_id)
        .order("applied_at", desc=True)
        .execute()
        .data
    )


# ======================================================
# Accept / Reject Candidate
# ======================================================
@elections_bp.route("/applications/<application_id>", methods=["PUT"])
@role_required("EC")
def update_candidate_status(application_id):
    db = get_db()
    db.table("candidate_applications").update({
        "status": request.json["status"]
    }).eq("id", application_id).execute()

    return {"msg": "Candidate status updated"}

@elections_bp.route("/voter", methods=["GET"])
@role_required("VOTER")
def get_voter_election():
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
        db.table("elections")
        .select("*")
        .eq("constituency_id", user["constituency_id"])
        .order("created_at", desc=True)
        .limit(1)
        .execute()
    )

    if not res.data:
        return {}, 200

    return res.data[0], 200

# ======================================================
# Voter applies as candidate
# ======================================================
@elections_bp.route("/apply", methods=["POST"])
@role_required("VOTER")
def apply_as_candidate():
    db = get_db()
    user_id = get_jwt_identity()
    data = request.json

    election_id = data["election_id"]
    manifesto = data["manifesto"]

    # 🔒 Prevent duplicate application
    existing = (
        db.table("candidate_applications")
        .select("id")
        .eq("election_id", election_id)
        .eq("user_id", user_id)
        .execute()
        .data
    )

    if existing:
        return {"msg": "You have already Filed Nomination"}, 400

    db.table("candidate_applications").insert({
        "election_id": election_id,
        "user_id": user_id,
        "manifesto": manifesto
    }).execute()

    return {"msg": "Nomination Filed Successfully"}, 201

