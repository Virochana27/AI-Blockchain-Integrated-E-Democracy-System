from models.voter import (
    get_voter_by_voter_id_number,
    map_voter_to_user,
    get_voter_user_mapping_by_user
)
from models.user import create_citizen_alias, get_citizen_alias
from utils.random_username import generate_random_username


# -----------------------------
# Voter Service
# -----------------------------

def link_voter_to_user(voter_id_number: str, user_id: str):
    """
    Maps an existing voter record to a logged-in user
    and generates anonymous citizen username if not exists.
    """

    voter = get_voter_by_voter_id_number(voter_id_number)
    if not voter or not voter.get("is_active"):
        raise ValueError("Invalid or inactive voter ID")

    # Check existing mapping
    existing_map = get_voter_user_mapping_by_user(user_id)
    if existing_map:
        return existing_map

    # Create voter ↔ user mapping
    mapping = map_voter_to_user(voter["id"], user_id)

    # Create citizen alias if not exists
    alias = get_citizen_alias(user_id)
    if not alias:
        random_username = generate_random_username()
        create_citizen_alias(user_id, random_username)

    return mapping


def get_linked_voter(user_id: str):
    """
    Returns voter details linked to logged-in user
    """
    mapping = get_voter_user_mapping_by_user(user_id)
    if not mapping:
        return None
    return mapping
