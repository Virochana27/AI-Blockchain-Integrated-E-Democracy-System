from supabase_db.db import fetch_all, fetch_one
from datetime import datetime

ELECTIONS = "elections"
CANDIDATES = "candidates"
VOTERS = "voters"
RECEIPTS = "vote_receipts"
CONSTITUENCIES = "constituencies"
DISTRICTS = "districts"
STATES = "states"


# ---------------------------------------------------
# 🟢 BASIC COUNTS
# ---------------------------------------------------

def get_total_votes(election_id):
    receipts = fetch_all(RECEIPTS, {"election_id": election_id})
    return len(receipts)


def get_total_voters_in_constituency(constituency_id):
    voters = fetch_all(VOTERS, {"constituency_id": constituency_id, "is_active": True})
    return len(voters)


def get_total_candidates(election_id):
    return len(fetch_all(CANDIDATES, {"election_id": election_id}))


# ---------------------------------------------------
# 🟢 TURNOUT INSIGHTS
# ---------------------------------------------------

def constituency_turnout_percentage(election_id):
    """
    Turnout = votes / registered voters per constituency
    """
    candidates = fetch_all(CANDIDATES, {"election_id": election_id})
    constituencies = {}

    for c in candidates:
        cid = c["constituency_id"]
        constituencies[cid] = True

    results = []

    total_votes = get_total_votes(election_id)

    for cid in constituencies:
        voters = get_total_voters_in_constituency(cid)
        turnout = (total_votes / voters * 100) if voters else 0

        results.append({
            "constituency_id": cid,
            "registered_voters": voters,
            "turnout_percent": round(turnout, 2)
        })

    return results


# ---------------------------------------------------
# 🟢 FIRST TIME VOTERS
# ---------------------------------------------------

def first_time_voters(election_start):
    """
    First time voters = age 18–19 at election time
    """

    voters = fetch_all(VOTERS, {"is_active": True})

    # Convert election_start if Supabase returned string
    if isinstance(election_start, str):
        election_start = datetime.fromisoformat(election_start)

    first_timers = []

    for v in voters:
        dob = v.get("date_of_birth")

        # Skip invalid records safely
        if not dob:
            continue

        # Convert dob if string
        if isinstance(dob, str):
            dob = datetime.fromisoformat(dob).date()

        age = (election_start.date() - dob).days // 365

        if 18 <= age <= 19:
            first_timers.append(v)

    return {
        "count": len(first_timers),
        "percentage": round(len(first_timers) / len(voters) * 100, 2) if voters else 0
    }


# ---------------------------------------------------
# 🟢 GENDER DISTRIBUTION
# ---------------------------------------------------

def voter_gender_split():
    voters = fetch_all(VOTERS, {"is_active": True})

    stats = {"Male": 0, "Female": 0, "Other": 0}

    for v in voters:
        g = v["gender"]
        stats[g] = stats.get(g, 0) + 1

    return stats


# ---------------------------------------------------
# 🟢 AGE DEMOGRAPHICS
# ---------------------------------------------------

def age_distribution(election_start):
    voters = fetch_all(VOTERS, {"is_active": True})

    # Convert election_start if string
    if isinstance(election_start, str):
        election_start = datetime.fromisoformat(election_start)

    buckets = {
        "18-25": 0,
        "26-40": 0,
        "41-60": 0,
        "60+": 0
    }

    for v in voters:
        dob = v.get("date_of_birth")

        # Skip invalid records
        if not dob:
            continue

        # Convert dob if string
        if isinstance(dob, str):
            dob = datetime.fromisoformat(dob).date()

        age = (election_start.date() - dob).days // 365

        if age < 18:
            continue
        elif age <= 25:
            buckets["18-25"] += 1
        elif age <= 40:
            buckets["26-40"] += 1
        elif age <= 60:
            buckets["41-60"] += 1
        else:
            buckets["60+"] += 1

    return buckets

# ---------------------------------------------------
# 🟢 PARTY SEAT SHARE
# ---------------------------------------------------

def party_seat_share(election_id, winners):
    """
    winners = list of candidate_ids who won seats
    """
    parties = {}

    for cid in winners:
        candidate = fetch_one(CANDIDATES, {"id": cid})
        if not candidate:
            continue

        party = candidate["party_name"]
        parties[party] = parties.get(party, 0) + 1

    return parties


# ---------------------------------------------------
# 🟢 PARTY VOTE SHARE
# ---------------------------------------------------

def party_vote_share(election_id, vote_map):
    """
    vote_map = {candidate_id: vote_count}
    """
    parties = {}

    for candidate_id, votes in vote_map.items():
        candidate = fetch_one(CANDIDATES, {"id": candidate_id})
        if not candidate:
            continue

        party = candidate["party_name"]
        parties[party] = parties.get(party, 0) + votes

    return parties


# ---------------------------------------------------
# 🟢 TOP PERFORMING CONSTITUENCIES
# ---------------------------------------------------

def top_turnout_constituencies(turnout_data, top_n=5):
    return sorted(turnout_data, key=lambda x: x["turnout_percent"], reverse=True)[:top_n]


# ---------------------------------------------------
# 🟢 LOWEST TURNOUT WARNING
# ---------------------------------------------------

def lowest_turnout_constituencies(turnout_data, bottom_n=5):
    return sorted(turnout_data, key=lambda x: x["turnout_percent"])[:bottom_n]