from datetime import datetime
from utils.helpers import utc_now
from models.election import mark_election_active, parse_dt

# CHANGE TO:
from utils.helpers import utc_now, parse_dt   # use helpers.parse_dt not models.election.parse_dt

def activate_election_if_needed(election):
    if election["status"] in ["Draft", "ACTIVE", "COMPLETED"]:
        return

    start_dt = parse_dt(election.get("_raw_start_time") or election.get("start_time"))
    if not start_dt:
        return

    if utc_now() < start_dt:   # both timezone-aware after fixes
        return

    mark_election_active(election["id"])
    print(f"Election activated: {election['election_name']}")