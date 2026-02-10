from utils.crypto import uuid_to_uint256
from services.blockchain_reader import get_votes_from_chain
from models.candidate import get_candidates_by_election_and_constituency, get_user_id_by_candidate_id 
import random
from models.election import get_election_by_id
from utils.helpers import utc_now

def get_final_constituency_results(election_id, constituency_id):
    """
    Returns:
    - winner
    - runner_up
    - all candidates with vote counts
    """

    election = get_election_by_id(election_id)
    if not election:
        raise ValueError("Invalid election")

    # ❗ Only completed elections
    if utc_now().isoformat() <= election["end_time"]:
        raise ValueError("Election not completed yet")

    # 1️⃣ Fetch candidates
    candidates = get_candidates_by_election_and_constituency(
        election_id=election_id,
        constituency_id=constituency_id
    )

    # 2️⃣ Prepare candidate map (uint256 id)
    candidate_map = {}
    for c in candidates:
        cid_uint = str(uuid_to_uint256(c["id"]))
        candidate_map[cid_uint] = {
            "candidate_id": c["id"],
            "candidate_name": c["candidate_name"],
            "party_name": c["party_name"],
            "votes": 0
        }

    # 3️⃣ Count votes from blockchain
    votes = get_votes_from_chain(election_id)

    for v in votes:
        cid = str(v["candidate_id"])
        if cid in candidate_map:
            candidate_map[cid]["votes"] += 1

    results = list(candidate_map.values())

    # 4️⃣ Sort by votes DESC
    results.sort(key=lambda x: x["votes"], reverse=True)

    # 5️⃣ Determine winner and runner-up with tie handling
    winner = None
    runner_up = None

    if len(results) >= 1:
        top_votes = results[0]["votes"]
        top_candidates = [c for c in results if c["votes"] == top_votes]

        winner = random.choice(top_candidates)

        remaining = [c for c in results if c != winner]

        if remaining:
            second_votes = remaining[0]["votes"]
            second_candidates = [
                c for c in remaining if c["votes"] == second_votes
            ]
            runner_up = random.choice(second_candidates)

    return {
        "winner": winner,
        "runner_up": runner_up,
        "all_candidates": results
    }


def get_constituency_results(election_id, constituency_id):

    candidates = get_candidates_by_election_and_constituency(
        election_id=election_id,
        constituency_id=constituency_id
    )

    candidate_map = {}

    # 🔑 IMPORTANT: map using uint256(candidate_id)
    for c in candidates:
        candidate_uint = str(uuid_to_uint256(c["id"]))
        user_id = get_user_id_by_candidate_id(c["id"])

        candidate_map[candidate_uint] = {
            "candidate_id": c["id"], 
            "user_id": user_id,      
            "candidate_name": c["candidate_name"],
            "party_name": c["party_name"],
            "votes": 0
        }

    # Read blockchain events
    votes = get_votes_from_chain(election_id)

    for v in votes:
        cid = str(v["candidate_id"])  # uint256 from chain

        if cid in candidate_map:
            candidate_map[cid]["votes"] += 1

    return list(candidate_map.values())

