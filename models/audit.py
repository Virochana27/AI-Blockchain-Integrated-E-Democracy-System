from supabase_db.db import insert_record, fetch_all
from utils.helpers import generate_uuid, utc_now,format_datetime


# -----------------------------
# Table Name
# -----------------------------

AUDIT_LOGS_TABLE = "audit_logs"


# -----------------------------
# Audit Logs
# -----------------------------

def create_audit_log(
    user_id: str,
    action: str,
    entity_type: str = None,
    entity_id: str = None
):
    payload = {
        "id": generate_uuid(),
        "user_id": user_id,
        "action": action,
        "entity_type": entity_type,
        "entity_id": entity_id,
        "timestamp": utc_now().isoformat()
    }
    return insert_record(AUDIT_LOGS_TABLE, payload, use_admin=True)


def get_audit_logs():
    audits=fetch_all(AUDIT_LOGS_TABLE)
    for audit in audits:
        audit["timestamp"]=format_datetime(audit["timestamp"])
    return audits


def get_audit_logs_by_user(user_id: str):
    return fetch_all(AUDIT_LOGS_TABLE, {"user_id": user_id})
