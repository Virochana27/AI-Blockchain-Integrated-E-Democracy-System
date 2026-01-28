from flask import Blueprint, render_template, request
from models.ledger import (
    get_ledger_entry_by_hash,
    get_all_ledger_entries
)
from models.vote import get_vote_by_transaction_id

bp = Blueprint("ledger", __name__, url_prefix="/ledger")


# -----------------------------
# Ledger Explorer
# -----------------------------

@bp.route("/explorer", methods=["GET"])
def explorer():
    search_hash = request.args.get("hash")

    if search_hash:
        entry = get_ledger_entry_by_hash(search_hash)
        vote = None

        if entry:
            vote = get_vote_by_transaction_id(search_hash)

        return render_template(
            "ledger/explorer.html",
            entry=entry,
            vote=vote,
            entries=None
        )

    entries = get_all_ledger_entries()

    return render_template(
        "ledger/explorer.html",
        entry=None,
        vote=None,
        entries=entries
    )
