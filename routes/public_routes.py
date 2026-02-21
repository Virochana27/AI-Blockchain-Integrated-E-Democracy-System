from flask import Blueprint, render_template
from models.election import get_all_elections

bp = Blueprint("public", __name__)

@bp.route("/elections")
def election_schedule():
    elections = get_all_elections()
    return render_template(
        "public/election_schedule.html",
        elections=elections
    )
@bp.route("/")
def landing():
    elections = get_all_elections()
    return render_template("public/landing.html",elections=elections)

@bp.route("/election-insights")
def election_dashboard(election_id=None):
    elections = get_all_elections()
    return render_template(
        "public/election_dashboard.html",
        elections=elections,
        preselected_id=election_id
    )

from services.election_insight_service import get_election_dashboard

@bp.route("/insights/<election_id>")
def insights_api(election_id):
    data = get_election_dashboard(election_id)

    if not data:
        return {"status": "error", "message": "Election not found"}, 404

    return {"status": "success", "data": data}