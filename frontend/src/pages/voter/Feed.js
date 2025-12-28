import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { getIssues } from "../../api/issuesApi";

function Feed() {
  const [issues, setIssues] = useState([]);
  const navigate = useNavigate();

  useEffect(() => {
    getIssues()
      .then(res => setIssues(res.data))
      .catch(err => console.error(err));
  }, []);

  return (
    <div className="container py-4">

      {/* Header */}
      <div className="d-flex justify-content-between align-items-center mb-4">
        <div>
          <h3 className="fw-bold text-center mb-1">Voter Feed</h3>
          <p className="text-muted mb-0">
            Issues raised in your constituency
          </p>
        </div>

        {/* Action Buttons */}
        <div>
          <button
            className="btn btn-outline-primary me-2"
            onClick={() => navigate("/voter/raise-issue")}
          >
            Raise Issue
          </button>

          <button
            className="btn btn-primary"
            onClick={() => navigate("/voter/elections")}
          >
            Elections
          </button>
        </div>
      </div>

      {/* Divider */}
      <hr />

      {/* Empty State */}
      {issues.length === 0 && (
        <div className="alert alert-info text-center mt-4">
          No issues raised yet
        </div>
      )}

      {/* Issue Feed */}
      <div className="row justify-content-center">
        {issues.map(issue => (
          <div className="col-md-8 mb-3" key={issue.id}>
            <div className="card shadow-sm border-0">

              <div className="card-body">

                {/* Issue Text */}
                <p className="mb-3">
                  {issue.description}
                </p>

                {/* Footer */}
                <div className="d-flex justify-content-between align-items-center">

                  {/* Status Badge */}
                  <span
                    className={`badge ${
                      issue.status === "RESOLVED"
                        ? "bg-success"
                        : issue.status === "IN_PROGRESS"
                        ? "bg-warning text-dark"
                        : "bg-secondary"
                    }`}
                  >
                    {issue.status}
                  </span>

                  {/* Timestamp */}
                  {issue.created_at && (
                    <small className="text-muted">
                      {new Date(issue.created_at).toLocaleString()}
                    </small>
                  )}

                </div>

              </div>
            </div>
          </div>
        ))}
      </div>

    </div>
  );
}

export default Feed;
