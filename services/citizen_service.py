from models.issue import (
    get_issues_by_constituency,
    get_issues_by_user
)
from models.user import get_citizen_alias
from models.voter import get_voter_user_mapping_by_user
from models.representative import get_rep_posts_by_constituency
from models.candidate import get_representatives_by_constituency


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
