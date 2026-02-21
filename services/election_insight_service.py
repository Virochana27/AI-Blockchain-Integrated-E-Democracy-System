from supabase_db.db import fetch_one, fetch_all
from models.election_insights import (
    get_total_votes,
    constituency_turnout_percentage,
    first_time_voters,
    voter_gender_split,
    age_distribution,
)
from services.result_service import (
    get_final_constituency_results,
    get_constituency_results
)
import math

ELECTIONS = "elections"
ELECTION_CONSTITUENCIES = "election_constituencies"


# ---------------------------------------------------
# 🟣 Party Seat Share (Blockchain winners)
# ---------------------------------------------------

def compute_party_seat_share(election_id):
    rows = fetch_all(ELECTION_CONSTITUENCIES, {"election_id": election_id})
    parties = {}

    for r in rows:
        cid = r["constituency_id"]

        try:
            result = get_final_constituency_results(election_id, cid)
        except Exception:
            continue

        winner = result.get("winner")
        if not winner:
            continue

        party = winner.get("party_name")
        if party:
            parties[party] = parties.get(party, 0) + 1

    return parties


# ---------------------------------------------------
# 📊 Party Vote Share %
# ---------------------------------------------------

def compute_party_vote_share(election_id):
    rows = fetch_all(ELECTION_CONSTITUENCIES, {"election_id": election_id})

    party_votes = {}
    total_votes = 0

    for r in rows:
        cid = r["constituency_id"]
        results = get_constituency_results(election_id, cid)

        for c in results:
            party = c["party_name"]
            votes = c["votes"]

            party_votes[party] = party_votes.get(party, 0) + votes
            total_votes += votes

    if total_votes > 0:
        for p in party_votes:
            party_votes[p] = round(party_votes[p] / total_votes * 100, 2)

    return party_votes


# ---------------------------------------------------
# 🏆 Victory Margins
# ---------------------------------------------------

def compute_victory_margins(election_id):
    rows = fetch_all(ELECTION_CONSTITUENCIES, {"election_id": election_id})
    margins = []

    for r in rows:
        cid = r["constituency_id"]

        try:
            res = get_final_constituency_results(election_id, cid)
        except Exception:
            continue

        winner = res.get("winner")
        runner = res.get("runner_up")

        if not winner or not runner:
            continue

        margin = winner["votes"] - runner["votes"]

        margins.append({
            "constituency_id": cid,
            "margin": margin,
            "winner": winner["candidate_name"],
            "party": winner["party_name"]
        })

    margins.sort(key=lambda x: x["margin"])  # smallest first = closest races
    return margins


# ---------------------------------------------------
# 📈 Turnout Leaderboard
# ---------------------------------------------------

def turnout_leaderboard(election_id):
    turnout = constituency_turnout_percentage(election_id)
    turnout.sort(key=lambda x: x["turnout_percent"], reverse=True)
    return turnout


# ---------------------------------------------------
# 🗺 Engagement Score (Heatmap Index)
# ---------------------------------------------------

def constituency_heatmap_score(election_id):
    turnout = constituency_turnout_percentage(election_id)
    scores = []

    for t in turnout:
        cid = t["constituency_id"]
        turnout_pct = t["turnout_percent"]

        results = get_constituency_results(election_id, cid)
        total_votes = sum(c["votes"] for c in results)

        score = turnout_pct + math.log(total_votes + 1)

        scores.append({
            "constituency_id": cid,
            "score": round(score, 2),
            "turnout": turnout_pct,
            "votes": total_votes
        })

    scores.sort(key=lambda x: x["score"], reverse=True)
    return scores


# ---------------------------------------------------
# 🟢 MAIN DASHBOARD SERVICE
# ---------------------------------------------------

def get_election_dashboard(election_id):
    election = fetch_one(ELECTIONS, {"id": election_id})
    if not election:
        return None

    election_start = election["start_time"]

    turnout_data = constituency_turnout_percentage(election_id)

    insights = {
        # Core metrics
        "total_votes": get_total_votes(election_id),
        "turnout_by_constituency": turnout_data,
        "first_time_voters": first_time_voters(election_start),
        "gender_split": voter_gender_split(),
        "age_distribution": age_distribution(election_start),

        # Blockchain derived metrics
        "party_seat_share": compute_party_seat_share(election_id),
        "party_vote_share": compute_party_vote_share(election_id),
        "victory_margins": compute_victory_margins(election_id),

        # Rankings
        "turnout_leaderboard": turnout_leaderboard(election_id),
        "constituency_heatmap": constituency_heatmap_score(election_id),
    }

    return insights