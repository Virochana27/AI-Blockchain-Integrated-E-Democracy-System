from supabase_db.db import fetch_one, insert_record, update_record, delete_record
from utils.helpers import generate_uuid, utc_now

TABLE = "rep_policy_comment_votes"


def get_user_comment_vote(comment_id, user_id):
    return fetch_one(TABLE, {
        "comment_id": comment_id,
        "user_id": user_id
    })


def upsert_comment_vote(comment_id, user_id, vote_value):
    existing = get_user_comment_vote(comment_id, user_id)

    if existing:
        return update_record(
            TABLE,
            {"id": existing["id"]},
            {
                "vote_value": vote_value,
                "updated_at": utc_now().isoformat()
            },
            use_admin=True
        )

    return insert_record(
        TABLE,
        {
            "id": generate_uuid(),
            "comment_id": comment_id,
            "user_id": user_id,
            "vote_value": vote_value,
            "created_at": utc_now().isoformat(),
            "updated_at": utc_now().isoformat()
        },
        use_admin=True
    )


def remove_comment_vote(comment_id, user_id):
    return delete_record(
        TABLE,
        {"comment_id": comment_id, "user_id": user_id},
        use_admin=True
    )
