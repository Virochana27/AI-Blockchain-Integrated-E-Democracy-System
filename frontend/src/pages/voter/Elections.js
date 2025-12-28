import { useEffect, useState, useContext } from "react";
import { useNavigate } from "react-router-dom";
import {
  getVoterElection,
  applyAsCandidate
} from "../../api/electionsApi";
import { AuthContext } from "../../context/AuthContext";

function Elections() {
  const { user } = useContext(AuthContext);
  const [election, setElection] = useState(null);
  const [manifesto, setManifesto] = useState("");
  const navigate = useNavigate();

  useEffect(() => {
    getVoterElection()
      .then(res => setElection(res.data))
      .catch(err => console.error(err));
  }, []);

  const apply = async () => {
    if (!manifesto.trim()) {
      alert("Please enter your manifesto");
      return;
    }

    try {
      await applyAsCandidate({
        election_id: election.id,
        manifesto
      });

      alert("Nomination submitted successfully");
      setManifesto("");
    } catch (err) {
      alert(err.response?.data?.msg || "Failed to apply");
    }
  };

  if (!election || !election.id) {
    return (
      <div className="container py-5 text-center">
        <p className="text-muted">No election available</p>
      </div>
    );
  }

  return (
    <div className="container py-5">

      {/* Header */}
      <div className="text-center mb-5">
        <h3 className="fw-bold">Election Overview</h3>
        <p className="text-muted">
          Participate in the democratic process of your constituency
        </p>
      </div>

      {/* Election Status */}
      <div className="row justify-content-center mb-4">
        <div className="col-md-8">
          <div className="card shadow-sm border-0">
            <div className="card-body d-flex justify-content-between align-items-center">
              <span className="fw-semibold">Current Status</span>
              <span
                className={`badge fs-6 ${
                  election.status === "ONGOING"
                    ? "bg-success"
                    : election.status === "NOMINATION_OPEN"
                    ? "bg-primary"
                    : "bg-secondary"
                }`}
              >
                {election.status}
              </span>
            </div>
          </div>
        </div>
      </div>

      {/* ==========================
          Candidate Application
         ========================== */}
      {election.status === "NOMINATION_OPEN" && (
        <div className="row justify-content-center mb-5">
          <div className="col-md-8">
            <div className="card shadow-sm border-0">
              <div className="card-body">

                <h5 className="fw-semibold mb-3">
                  File Nomination
                </h5>

                <p className="text-muted mb-3">
                  Share your vision and policies with the voters
                </p>

                <textarea
                  className="form-control mb-3"
                  placeholder="Enter your manifesto"
                  rows={6}
                  value={manifesto}
                  onChange={e => setManifesto(e.target.value)}
                />

                <div className="text-end">
                  <button
                    className="btn btn-primary px-4"
                    onClick={apply}
                  >
                    Submit Nomination
                  </button>
                </div>

              </div>
            </div>
          </div>
        </div>
      )}

      {/* ==========================
          Voting Section
         ========================== */}
      {election.status === "ONGOING" ? (
        <div className="text-center">
          <button
            className="btn btn-success btn-lg px-5"
            onClick={() => navigate("/voter/vote")}
          >
            Vote Now
          </button>
        </div>
      ) : election.status !== "NOMINATION_OPEN" ? (
        <div className="text-center text-muted">
          Voting is not open yet
        </div>
      ) : null}

    </div>
  );
}

export default Elections;
