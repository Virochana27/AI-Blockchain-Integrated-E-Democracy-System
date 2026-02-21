from flask import Blueprint, jsonify, request, abort
from services.election_insight_service import get_election_dashboard

bp = Blueprint("election_insights", __name__, url_prefix="/insights")


@bp.route("/<election_id>", methods=["GET"])
def election_dashboard(election_id):
    """
    Main dashboard endpoint
    Example:
    /insights/abc-uuid
    """

    # Optional winners list from query
    winners = request.args.getlist("winner")

    # Optional vote map JSON
    vote_map = request.json.get("vote_map") if request.is_json else None

    insights = get_election_dashboard(
        election_id,
        winners=winners,
        vote_map=vote_map
    )

    if not insights:
        abort(404, "Election not found")

    return jsonify({
        "status": "success",
        "data": insights
    })