from flask import Blueprint, render_template, request, jsonify
from services.result_service import get_final_constituency_results
from models.election import get_completed_elections
from models.election import get_constituencies_for_election

bp = Blueprint("public_results", __name__, url_prefix="/public/results")


@bp.route("/")
def dashboard():
    elections = get_completed_elections()
    return render_template(
        "results/public_dashboard.html",
        elections=elections
    )


@bp.route("/constituencies")
def constituencies():
    election_id = request.args.get("election_id")
    return jsonify(get_constituencies_for_election(election_id))


@bp.route("/final")
def final_results():
    election_id = request.args.get("election_id")
    constituency_id = request.args.get("constituency_id")

    results = get_final_constituency_results(
        election_id=election_id,
        constituency_id=constituency_id
    )

    return jsonify(results)
