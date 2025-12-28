import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { getECComplaints } from "../../api/electionsApi";

function Complaints() {
  const { id } = useParams();
  const [complaints, setComplaints] = useState([]);

  useEffect(() => {
    getECComplaints(id)
      .then(res => setComplaints(res.data))
      .catch(err => console.error(err));
  }, [id]);

  return (
    <div className="container py-5">

      {/* Header */}
      <div className="text-center mb-5">
        <h3 className="fw-bold">Complaints to Election Commission</h3>
        <p className="text-muted">
          Review and monitor voter complaints in this constituency
        </p>
      </div>

      {/* Empty State */}
      {complaints.length === 0 && (
        <div className="alert alert-info text-center">
          No complaints raised for this constituency
        </div>
      )}

      {/* Complaints List */}
      <div className="row justify-content-center">
        {complaints.map(c => (
          <div className="col-md-8 mb-4" key={c.id}>
            <div className="card shadow-sm border-0">

              <div className="card-body">

                {/* Complaint Text */}
                <h6 className="fw-semibold mb-3">
                  Complaint
                </h6>
                <p className="mb-3">
                  {c.message}
                </p>

                {/* Footer */}
                <div className="d-flex justify-content-between align-items-center">

                  {/* Status Badge */}
                  <span
                    className={`badge ${
                      c.status === "RESOLVED"
                        ? "bg-success"
                        : c.status === "IN_PROGRESS"
                        ? "bg-warning text-dark"
                        : "bg-secondary"
                    }`}
                  >
                    {c.status}
                  </span>

                  {/* Date */}
                  <small className="text-muted">
                    {new Date(c.created_at).toLocaleString()}
                  </small>

                </div>

              </div>
            </div>
          </div>
        ))}
      </div>

    </div>
  );
}

export default Complaints;
