from supabase_db.db import fetch_all, insert_record
from utils.helpers import generate_uuid, utc_now

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

    # index comments by id
    comment_map = {c["id"]: c for c in comments}

    # add replies list
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
