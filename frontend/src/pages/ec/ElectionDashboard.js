import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import {
  getElectionByConstituency,
  createElection,
  updateElection
} from "../../api/electionsApi";

function ElectionDashboard() {
  const { id } = useParams();
  const [election, setElection] = useState(null);
  const [form, setForm] = useState({});

  useEffect(() => {
    getElectionByConstituency(id).then(res => {
      if (res.data && res.data.id) {
        setElection(res.data);
      } else {
        setElection(null);
      }
    });
  }, [id]);

  const createNewElection = async () => {
    const res = await createElection({ constituency_id: id });
    setElection(res.data);
    alert("Election created successfully");
  };

  const save = async () => {
    if (!election || !election.id) {
      alert("Please create an election first");
      return;
    }

    await updateElection(election.id, form);
    alert("Election details updated");
  };

  return (
    <div className="container py-5">

      {/* Header */}
      <div className="text-center mb-5">
        <h3 className="fw-bold">Election Management</h3>
        <p className="text-muted">
          Configure nomination, registration, and election timelines
        </p>
      </div>

      {/* ===============================
          NO ELECTION STATE
         =============================== */}
      {!election && (
        <div className="row justify-content-center">
          <div className="col-md-8">
            <div className="card shadow-sm border-0 text-center">
              <div className="card-body">

                <h5 className="mb-3">
                  No Active Election
                </h5>

                <p className="text-muted mb-4">
                  There is currently no election for this constituency.
                </p>

                <button
                  className="btn btn-primary px-4"
                  onClick={createNewElection}
                >
                  Create New Election
                </button>

              </div>
            </div>
          </div>
        </div>
      )}

      {/* ===============================
          ELECTION EXISTS
         =============================== */}
      {election && (
        <div className="row justify-content-center">
          <div className="col-md-8">

            {/* Status Card */}
            <div className="card shadow-sm border-0 mb-4">
              <div className="card-body d-flex justify-content-between align-items-center">
                <span className="fw-semibold">Current Status</span>
                <span className="badge bg-secondary fs-6">
                  {election.status}
                </span>
              </div>
            </div>

            {/* Nomination Phase */}
            <div className="card shadow-sm border-0 mb-4">
              <div className="card-body">
                <h5 className="fw-semibold mb-3">
                  Nomination Filing Phase
                </h5>

                <label className="form-label">
                  Nomination Deadline
                </label>
                <input
                  type="datetime-local"
                  className="form-control"
                  onChange={e =>
                    setForm({
                      ...form,
                      application_deadline: e.target.value
                    })
                  }
                />
              </div>
            </div>

            {/* Voter Registration Phase */}
            <div className="card shadow-sm border-0 mb-4">
              <div className="card-body">
                <h5 className="fw-semibold mb-3">
                  Voter Registration Phase
                </h5>

                <label className="form-label">
                  Registration Deadline
                </label>
                <input
                  type="datetime-local"
                  className="form-control"
                  onChange={e =>
                    setForm({
                      ...form,
                      voter_registration_deadline: e.target.value
                    })
                  }
                />
              </div>
            </div>

            {/* Election Schedule */}
            <div className="card shadow-sm border-0 mb-4">
              <div className="card-body">
                <h5 className="fw-semibold mb-3">
                  Election Schedule
                </h5>

                <label className="form-label">
                  Start Time
                </label>
                <input
                  type="datetime-local"
                  className="form-control mb-3"
                  onChange={e =>
                    setForm({
                      ...form,
                      start_time: e.target.value
                    })
                  }
                />

                <label className="form-label">
                  End Time
                </label>
                <input
                  type="datetime-local"
                  className="form-control"
                  onChange={e =>
                    setForm({
                      ...form,
                      end_time: e.target.value
                    })
                  }
                />
              </div>
            </div>

            {/* Save Button */}
            <div className="text-end">
              <button
                className="btn btn-success px-4 d-flex justify-content-center"
                onClick={save}
              >
                Save Election Details
              </button>
            </div>

          </div>
        </div>
      )}

    </div>
  );
}

export default ElectionDashboard;
