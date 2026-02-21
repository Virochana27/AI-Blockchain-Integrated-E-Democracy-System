from models.representative import (
    create_rep_post,
    add_rep_comment,
    update_rep_score,
    get_rep_posts_by_user,
    get_rep_score
)
from models.issue import get_issue_by_id
from models.audit import create_audit_log
from models.issue import get_issues_by_constituency
from supabase_db.db import fetch_one, fetch_all, insert_record, update_record


# -----------------------------
# Representative Service
# -----------------------------
'''
def post_update(user_id: str, constituency_id: str, content: str):
    """
    Elected / Opposition representative creates a post.
    """
    post = create_rep_post(user_id, constituency_id, content)

    create_audit_log(
        user_id=user_id,
        action="CREATE_REP_POST",
        entity_type="REP_POST",
        entity_id=post[0]["id"]
    )

    return post
'''

def comment_on_rep_post(post_id: str, user_id: str, comment: str):
    """
    Representatives debate on posts.
    """
    add_rep_comment(post_id, user_id, comment)

    create_audit_log(
        user_id=user_id,
        action="COMMENT_REP_POST",
        entity_type="REP_POST",
        entity_id=post_id
    )


def reward_issue_resolution(rep_user_id: str, issue_id: str):
    """
    Increase score when issue is successfully resolved.
    """
    issue = get_issue_by_id(issue_id)
    if not issue:
        raise ValueError("Issue not found")

    update_rep_score(
        user_id=rep_user_id,
        issue_score_delta=10
    )

    create_audit_log(
        user_id=rep_user_id,
        action="ISSUE_RESOLUTION_REWARD",
        entity_type="ISSUE",
        entity_id=issue_id
    )



def get_my_posts(user_id: str):
    return get_rep_posts_by_user(user_id)

from utils.helpers import _time_ago
def get_constituency_issues_for_rep(constituency_id: str):
    """
    Returns constituency issues with:
    - human readable created_at
    - vote score (upvotes - downvotes)
    """

    issues = get_issues_by_constituency(constituency_id)

    if not issues:
        return []

    for issue in issues:

        # 🔹 Convert time to "time ago"
        if issue.get("created_at"):
            issue["time_ago"] = _time_ago(issue["created_at"])

        # 🔹 Fetch votes for this issue
        votes = fetch_all(
            "issue_votes",
            {"issue_id": issue["id"]}
        )

        upvotes = 0
        downvotes = 0

        for vote in votes:
            if vote["vote_type"] == "up":
                upvotes += 1
            elif vote["vote_type"] == "down":
                downvotes += 1

        # 🔹 Score calculation
        issue["score"] = upvotes - downvotes
        issue["upvotes"] = upvotes
        issue["downvotes"] = downvotes

    return issues

def get_my_performance_score(user_id: str):
    return get_rep_score(user_id)
