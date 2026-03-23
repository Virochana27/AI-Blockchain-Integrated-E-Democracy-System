from datetime import datetime,timezone
from services.election_closure_service import close_election_and_assign_reps
from utils.helpers import utc_now

def finalize_election_if_needed(election):
    from models.election import get_election_by_id, mark_election_completed, parse_dt
    """
    Finalizes election ONLY ONCE:
    - Marks election COMPLETED
    - Assigns representatives
    """
    if election["status"] == "COMPLETED":
        return  # already done
    end_dt = parse_dt(election.get("_raw_end_time"))
    if not end_dt:
        return

    if end_dt.tzinfo is None:
        end_dt = end_dt.replace(tzinfo=timezone.utc)
    if utc_now() <= end_dt:   # proper datetime comparison
        return

    # 1️⃣ Mark election completed
    mark_election_completed(election["id"])

    close_election_and_assign_reps(election)

