import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import {
  getCandidateApplications,
  updateCandidateStatus
} from "../../api/electionsApi";

function CandidateReview() {
  const { electionId } = useParams();
  const [candidates, setCandidates] = useState([]);

  useEffect(() => {
    getCandidateApplications(electionId)
      .then(res => setCandidates(res.data))
      .catch(err => console.error(err));
  }, [electionId]);

  const updateStatus = (id, status) => {
    updateCandidateStatus(id, status).then(() => {
      setCandidates(prev =>
        prev.map(c =>
          c.id === id ? { ...c, status } : c
        )
      );
    });
  };

  return (
    <div className="container py-5">

      {/* Header */}
      <div className="text-center mb-5">
        <h3 className="fw-bold">Filed Nominations</h3>
        <p className="text-muted">
          Review and approve candidate applications for this election
        </p>
      </div>

      {/* Empty State */}
      {candidates.length === 0 && (
        <div className="alert alert-info text-center">
          No candidate applications received
        </div>
      )}

      {/* Candidate Cards */}
      <div className="row justify-content-center">
        {candidates.map(c => (
          <div className="col-md-8 mb-4" key={c.id}>
            <div className="card shadow-sm border-0">

              <div className="card-body">

                {/* Candidate Info */}
                <div className="mb-3">
                  <h5 className="mb-1">
                    {c.users?.name}
                  </h5>
                  <small className="text-muted">
                    {c.users?.email}
                  </small>
                </div>

                {/* Manifesto */}
                <div className="mb-3">
                  <h6 className="fw-semibold">Manifesto</h6>
                  <p className="mb-0">
                    {c.manifesto || "No manifesto submitted"}
                  </p>
                </div>

                {/* Footer */}
                <div className="d-flex justify-content-between align-items-center">

                  {/* Status Badge */}
                  <span
                    className={`badge ${
                      c.status === "ACCEPTED"
                        ? "bg-success"
                        : c.status === "REJECTED"
                        ? "bg-danger"
                        : "bg-secondary"
                    }`}
                  >
                    {c.status}
                  </span>

                  {/* Action Buttons */}
                  {c.status === "PENDING" && (
                    <div>
                      <button
                        className="btn btn-outline-success btn-sm me-2"
                        onClick={() => updateStatus(c.id, "ACCEPTED")}
                      >
                        Accept
                      </button>

                      <button
                        className="btn btn-outline-danger btn-sm"
                        onClick={() => updateStatus(c.id, "REJECTED")}
                      >
                        Reject
                      </button>
                    </div>
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

export default CandidateReview;
