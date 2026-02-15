from supabase_db.db import fetch_one, fetch_all, insert_record
from utils.helpers import generate_uuid, utc_now, format_datetime, _time_ago
from datetime import datetime, timezone
from flask import session

TABLE = "rep_policy_comments"


def add_policy_comment(post_id, user_id, content, parent_comment_id=None):
    payload = {
        "id": generate_uuid(),
        "post_id": post_id,
        "user_id": user_id,
        "content": content,
        "parent_comment_id": parent_comment_id,
        "created_at": utc_now().isoformat(),
        "updated_at": utc_now().isoformat(),
    }

    return insert_record(TABLE, payload, use_admin=True)

def get_policy_comments(post_id):
    comments = fetch_all(
        "rep_policy_comments",
        {"post_id": post_id}
    ) or []

    user_id = session.get("user_id")

    # attach username + time + vote info
    for c in comments:

        # -------------------------
        # Username logic
        # -------------------------
        if c.get("ai_generated"):
            c["username"] = "AI Bot"
        else:
            alias = fetch_one("citizen_alias", {"user_id": c["user_id"]})
            if alias:
                c["username"] = alias.get("random_username")
            else:
                user = fetch_one("users", {"id": c["user_id"]})
                c["username"] = user.get("full_name") if user else "Citizen"

        # -------------------------
        # Time
        # -------------------------
        c["time_ago"] = _time_ago(c.get("created_at"))
        c["created_at"]=format_datetime(c["created_at"])
        # -------------------------
        # Vote score
        # -------------------------
        votes = fetch_all(
            "rep_policy_comment_votes",
            {"comment_id": c["id"]}
        ) or []

        c["score"] = sum(v["vote_value"] for v in votes)

        # -------------------------
        # User vote
        # -------------------------
        if user_id:
            user_vote = fetch_one(
                "rep_policy_comment_votes",
                {"comment_id": c["id"], "user_id": user_id}
            )
            c["user_vote"] = user_vote["vote_value"] if user_vote else None
        else:
            c["user_vote"] = None

    # -------------------------
    # Build threaded tree
    # -------------------------
    comment_map = {c["id"]: c for c in comments}

    for c in comment_map.values():
        c["replies"] = []

    root_comments = []

    for c in comments:
        parent_id = c.get("parent_comment_id")
        if parent_id and parent_id in comment_map:
            comment_map[parent_id]["replies"].append(c)
        else:
            root_comments.append(c)

    return root_comments
