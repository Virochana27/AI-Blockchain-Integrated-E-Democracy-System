import { useParams, useNavigate } from "react-router-dom";

function ConstituencyView() {
  const { id } = useParams();
  const navigate = useNavigate();

  return (
    <div className="container py-5">

      {/* Header */}
      <div className="text-center mb-5">
        <h3 className="fw-bold">Constituency Dashboard</h3>
        <p className="text-muted">
          Manage complaints and elections for this constituency
        </p>
      </div>

      {/* Action Cards */}
      <div className="row justify-content-center">

        {/* Complaints */}
        <div className="col-md-5 mb-4">
          <div className="card h-100 shadow-sm border-0">
            <div className="card-body text-center d-flex flex-column">

              <div className="mb-3">
                <i className="bi bi-exclamation-circle fs-1 text-danger"></i>
              </div>

              <h5 className="card-title fw-semibold">
                Complaints
              </h5>

              <p className="text-muted mb-4">
                View and resolve complaints raised by voters
              </p>

              <button
                className="btn btn-outline-danger mt-auto"
                onClick={() => navigate(`/ec/complaints/${id}`)}
              >
                View Complaints
              </button>

            </div>
          </div>
        </div>

        {/* Election */}
        <div className="col-md-5 mb-4">
          <div className="card h-100 shadow-sm border-0">
            <div className="card-body text-center d-flex flex-column">

              <div className="mb-3">
                <i className="bi bi-clipboard-check fs-1 text-primary"></i>
              </div>

              <h5 className="card-title fw-semibold">
                Election Management
              </h5>

              <p className="text-muted mb-4">
                Create and manage elections, schedules, and candidates
              </p>

              <button
                className="btn btn-primary mt-auto"
                onClick={() => navigate(`/ec/constituency/${id}/election`)}
              >
                Go to Election
              </button>

            </div>
          </div>
        </div>

      </div>

    </div>
  );
}

export default ConstituencyView;
