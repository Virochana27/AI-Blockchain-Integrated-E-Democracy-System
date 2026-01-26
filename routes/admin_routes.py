from flask import Blueprint, render_template, session
from utils.decorators import login_required, role_required
from models.audit import get_audit_logs
from models.user import get_users_by_role
from models.ledger import get_all_ledger_entries

bp = Blueprint("admin", __name__, url_prefix="/admin")


# -----------------------------
# Admin Dashboard (CEC Only)
# -----------------------------

@bp.route("/dashboard")
@login_required
@role_required("CEC")
def dashboard():
    return render_template("admin/dashboard.html")


# -----------------------------
# Audit Logs
# -----------------------------

@bp.route("/audit-logs")
@login_required
@role_required("CEC")
def audit_logs():
    logs = get_audit_logs()
    return render_template("admin/audit_logs.html", logs=logs)


# -----------------------------
# System Users Overview
# -----------------------------

@bp.route("/users")
@login_required
@role_required("CEC")
def users():
    election_commission_users = {
        "CEC": get_users_by_role("CEC"),
        "CEO": get_users_by_role("CEO"),
        "DEO": get_users_by_role("DEO"),
        "RO": get_users_by_role("RO"),
        "ERO": get_users_by_role("ERO"),
        "BLO": get_users_by_role("BLO")
    }
    return render_template(
        "admin/users.html",
        users=election_commission_users
    )


# -----------------------------
# Full Ledger (Admin View)
# -----------------------------

@bp.route("/ledger")
@login_required
@role_required("CEC")
def ledger():
    entries = get_all_ledger_entries()
    return render_template("admin/ledger.html", entries=entries)
