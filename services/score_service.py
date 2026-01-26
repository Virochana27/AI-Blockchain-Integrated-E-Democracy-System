from models.representative import get_rep_score, update_rep_score
from models.issue import get_issue_resolution
from models.audit import create_audit_log


# -----------------------------
# Score Service
# -----------------------------

def reward_post_engagement(user_id: str, score_delta: int):
    """
    Adjust score based on post engagement (upvotes/downvotes – hidden from UI)
    """
    update_rep_score(
        user_id=user_id,
        post_score_delta=score_delta
    )

    create_audit_log(
        user_id=user_id,
        action="POST_ENGAGEMENT_SCORE_UPDATE",
        entity_type="REP_SCORE",
        entity_id=user_id
    )


def reward_successful_issue_resolution(rep_user_id: str, issue_id: str):
    """
    Rewards representative only if citizen confirms resolution
    """
    resolution = get_issue_resolution(issue_id)
    if not resolution or not resolution.get("citizen_confirmed"):
        raise ValueError("Issue resolution not confirmed by citizen")

    update_rep_score(
        user_id=rep_user_id,
        issue_score_delta=15
    )

    create_audit_log(
        user_id=rep_user_id,
        action="CONFIRMED_ISSUE_RESOLUTION_SCORE",
        entity_type="ISSUE",
        entity_id=issue_id
    )
