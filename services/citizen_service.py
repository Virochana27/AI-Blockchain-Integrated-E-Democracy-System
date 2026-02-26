from models.issue import (
    get_issues_by_constituency,
    get_issues_by_user
)
from models.user import get_citizen_alias
from models.voter import get_voter_user_mapping_by_user
from models.representative import get_rep_posts_by_constituency
from models.candidate import get_representatives_by_constituency
from models.user import get_citizen_alias, create_citizen_alias
from utils.alias_generator import generate_random_username
from supabase_db.db import fetch_one


# -----------------------------
# Citizen Aggregation Service
# -----------------------------

def get_constituency_issues(constituency_id: str):
    return get_issues_by_constituency(constituency_id)


def get_my_issues(user_id: str):
    return get_issues_by_user(user_id)


def get_citizen_profile(user_id: str):
    alias = get_citizen_alias(user_id)
    voter_map = get_voter_user_mapping_by_user(user_id)

    return {
        "alias": alias,
        "voter_mapping": voter_map
    }


def get_representatives(constituency_id: str):
    return get_representatives_by_constituency(constituency_id)


def get_representative_posts(constituency_id: str):
    return get_rep_posts_by_constituency(constituency_id)

def ensure_citizen_alias(user_id: str):
    alias = get_citizen_alias(user_id)
    if alias:
        return alias

    # Keep generating until unique
    while True:
        username = generate_random_username()
        existing = fetch_one(
            "citizen_alias",
            {"random_username": username}
        )
        if not existing:
            break

    return create_citizen_alias(user_id, username)[0]

from utils.helpers import parse_dt

def get_resolution_time_from_timeline(timeline, parse_dt):
    """Return latest resolved timestamp from timeline entries."""
    resolved_times = [
        parse_dt(t["created_at"])
        for t in timeline
        if t.get("status") in ("Resolved", "Closed")
    ]
    resolved_times = [t for t in resolved_times if t]
    return max(resolved_times) if resolved_times else None