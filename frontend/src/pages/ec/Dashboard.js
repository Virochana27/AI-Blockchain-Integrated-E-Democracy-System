import { useEffect, useState } from "react";
import { getConstituencies } from "../../api/electionsApi";
import { useNavigate } from "react-router-dom";

function Dashboard() {
  const [constituencies, setConstituencies] = useState([]);
  const navigate = useNavigate();

  useEffect(() => {
    getConstituencies()
      .then(res => setConstituencies(res.data))
      .catch(err => console.error(err));
  }, []);

  return (
    <div className="container">

      {/* Header */}
      <div className="mb-4 text-center">
        <h3>Election Commission Dashboard</h3>
        <p className="text-muted">
          Manage constituencies, elections, and complaints
        </p>
      </div>

      {/* Empty State */}
      {constituencies.length === 0 && (
        <div className="alert alert-info">
          No constituencies found
        </div>
      )}

      {/* Constituency Cards */}
      <div className="row">
        {constituencies.map(c => (
          <div className="col-md-4 mb-3" key={c.id}>
            <div className="card h-100 shadow-sm">
              <div className="card-body d-flex flex-column">

                <h5 className="card-title">
                  {c.name}
                </h5>

                <p className="card-text text-muted mb-4">
                  State: {c.state}
                </p>

                <button
                  className="btn btn-primary mt-auto"
                  onClick={() => navigate(`/ec/constituency/${c.id}`)}
                >
                  Manage Constituency
                </button>

              </div>
            </div>
          </div>
        ))}
      </div>

    </div>
  );
}

export default Dashboard;
