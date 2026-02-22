from supabase_db.db import fetch_all, fetch_one
from datetime import datetime

ELECTIONS = "elections"
CANDIDATES = "candidates"
VOTERS = "voters"
RECEIPTS = "vote_receipts"
CONSTITUENCIES = "constituencies"
DISTRICTS = "districts"
STATES = "states"

def get_constituency_name(constituency_id):
    c = fetch_one(CONSTITUENCIES, {"id": constituency_id})
    return c["constituency_name"] if c else "Unknown Constituency"

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
    Turnout per constituency using registered voters vs actual voters
    """

    from supabase_db.db import fetch_all

    VOTE_STATUS = "vote_status"

    candidates = fetch_all(CANDIDATES, {"election_id": election_id})
    constituency_ids = list({c["constituency_id"] for c in candidates})

    results = []

    for cid in constituency_ids:

        # registered voters
        registered = fetch_all(VOTERS, {
            "constituency_id": cid,
            "is_active": True
        })
        registered_count = len(registered)

        # voters who voted
        voted = fetch_all(VOTE_STATUS, {
            "election_id": election_id,
            "has_voted": True
        })

        voted_count = 0
        for r in voted:
            v = fetch_one(VOTERS, {"id": r["voter_id"]})
            if v and v.get("constituency_id") == cid:
                voted_count += 1

        turnout = (voted_count / registered_count * 100) if registered_count else 0

        results.append({
            "constituency_id": cid,
            "constituency_name": get_constituency_name(cid),
            "registered_voters": registered_count,
            "votes_cast": voted_count,
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

def voter_gender_split(election_id):
    """
    Gender split of people who ACTUALLY voted in this election
    """

    from supabase_db.db import fetch_all, fetch_one

    VOTE_STATUS = "vote_status"

    # get all voters who voted
    rows = fetch_all(VOTE_STATUS, {
        "election_id": election_id,
        "has_voted": True
    })

    if not rows:
        return {
            "Male":0,"Female":0,"Other":0,
            "Male_pct":0,"Female_pct":0,"Other_pct":0
        }

    stats = {"Male":0,"Female":0,"Other":0}

    for r in rows:
        voter = fetch_one(VOTERS, {"id": r["voter_id"]})
        if not voter:
            continue

        g = voter.get("gender") or "Other"
        stats[g] = stats.get(g, 0) + 1

    total = sum(stats.values()) or 1

    return {
        "Male": stats["Male"],
        "Female": stats["Female"],
        "Other": stats["Other"],
        "Male_pct": round(stats["Male"]/total*100,2),
        "Female_pct": round(stats["Female"]/total*100,2),
        "Other_pct": round(stats["Other"]/total*100,2),
    }


# ---------------------------------------------------
# 🟢 AGE DEMOGRAPHICS
# ---------------------------------------------------

def age_distribution(election_id, election_start):
    """
    Age distribution for registered vs voted voters
    """

    from supabase_db.db import fetch_all, fetch_one

    VOTE_STATUS = "vote_status"

    # Convert election_start if string
    if isinstance(election_start, str):
        election_start = datetime.fromisoformat(election_start)

    buckets = {
        "18-25": {"registered":0, "voted":0},
        "26-40": {"registered":0, "voted":0},
        "41-60": {"registered":0, "voted":0},
        "60+": {"registered":0, "voted":0}
    }

    voters = fetch_all(VOTERS, {"is_active": True})

    # get who voted
    voted_rows = fetch_all(VOTE_STATUS, {
        "election_id": election_id,
        "has_voted": True
    })
    voted_ids = {r["voter_id"] for r in voted_rows}

    for v in voters:
        dob = v.get("date_of_birth")
        if not dob:
            continue

        if isinstance(dob, str):
            dob = datetime.fromisoformat(dob).date()

        age = (election_start.date() - dob).days // 365

        # determine bucket
        if age < 18:
            continue
        elif age <= 25:
            bucket = "18-25"
        elif age <= 40:
            bucket = "26-40"
        elif age <= 60:
            bucket = "41-60"
        else:
            bucket = "60+"

        buckets[bucket]["registered"] += 1

        if v["id"] in voted_ids:
            buckets[bucket]["voted"] += 1

    return buckets

def turnout_by_age_group(election_id, election_start):
    from supabase_db.db import fetch_all
    from datetime import datetime

    VOTE_STATUS = "vote_status"

    if isinstance(election_start, str):
        election_start = datetime.fromisoformat(election_start)

    voters = fetch_all(VOTERS, {"is_active": True})

    voted_rows = fetch_all(VOTE_STATUS, {
        "election_id": election_id,
        "has_voted": True
    })
    voted_ids = {r["voter_id"] for r in voted_rows}

    buckets = {
        "18-25": {"registered":0,"voted":0},
        "26-40": {"registered":0,"voted":0},
        "41-60": {"registered":0,"voted":0},
        "60+": {"registered":0,"voted":0}
    }

    for v in voters:
        dob = v.get("date_of_birth")
        if not dob:
            continue
        if isinstance(dob, str):
            dob = datetime.fromisoformat(dob).date()

        age = (election_start.date() - dob).days // 365

        if age < 18: continue
        elif age <= 25: bucket="18-25"
        elif age <= 40: bucket="26-40"
        elif age <= 60: bucket="41-60"
        else: bucket="60+"

        buckets[bucket]["registered"] += 1
        if v["id"] in voted_ids:
            buckets[bucket]["voted"] += 1

    # compute turnout %
    for b in buckets:
        reg = buckets[b]["registered"] or 1
        buckets[b]["turnout_pct"] = round(buckets[b]["voted"]/reg*100,2)

    return buckets

def gender_turnout_by_age(election_id, election_start):
    from supabase_db.db import fetch_all
    from datetime import datetime

    VOTE_STATUS = "vote_status"

    if isinstance(election_start, str):
        election_start = datetime.fromisoformat(election_start)

    voters = fetch_all(VOTERS, {"is_active": True})

    voted_rows = fetch_all(VOTE_STATUS, {
        "election_id": election_id,
        "has_voted": True
    })
    voted_ids = {r["voter_id"] for r in voted_rows}

    data = {
        "18-25": {"Male":0,"Female":0,"Other":0},
        "26-40": {"Male":0,"Female":0,"Other":0},
        "41-60": {"Male":0,"Female":0,"Other":0},
        "60+": {"Male":0,"Female":0,"Other":0}
    }

    for v in voters:
        dob = v.get("date_of_birth")
        if not dob:
            continue
        if isinstance(dob,str):
            dob=datetime.fromisoformat(dob).date()

        age=(election_start.date()-dob).days//365

        if age < 18: continue
        elif age<=25: bucket="18-25"
        elif age<=40: bucket="26-40"
        elif age<=60: bucket="41-60"
        else: bucket="60+"

        if v["id"] in voted_ids:
            gender=v.get("gender") or "Other"
            data[bucket][gender]+=1

    return data

def constituency_demographic_heatmap(election_id, election_start):
    from supabase_db.db import fetch_all, fetch_one
    from datetime import datetime

    VOTE_STATUS="vote_status"

    if isinstance(election_start,str):
        election_start=datetime.fromisoformat(election_start)

    voted_rows=fetch_all(VOTE_STATUS,{
        "election_id":election_id,
        "has_voted":True
    })

    heatmap={}

    for r in voted_rows:
        voter=fetch_one(VOTERS,{"id":r["voter_id"]})
        if not voter: continue

        cid=voter["constituency_id"]
        cname=get_constituency_name(cid)

        if cname not in heatmap:
            heatmap[cname]={
                "total":0,
                "Male":0,
                "Female":0,
                "Other":0
            }

        heatmap[cname]["total"]+=1
        g=voter.get("gender") or "Other"
        heatmap[cname][g]+=1

    return heatmap
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