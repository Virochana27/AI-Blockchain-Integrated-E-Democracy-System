import { useState } from "react";
import { raiseIssue } from "../../api/issuesApi";
import { raiseECComplaint } from "../../api/electionsApi";

function RaiseIssue() {
  const [description, setDescription] = useState("");
  const [type, setType] = useState("PUBLIC"); // PUBLIC or EC

  const submit = async () => {
    if (!description.trim()) {
      alert("Please describe the issue");
      return;
    }

    try {
      if (type === "PUBLIC") {
        await raiseIssue({ description });
        alert("Issue raised successfully");
      } else {
        await raiseECComplaint({ message: description });
        alert("Complaint sent to Election Commission");
      }

      setDescription("");
    } catch (err) {
      alert("Something went wrong");
      console.error(err);
    }
  };

  return (
    <div className="container py-5">

      {/* Header */}
      <div className="text-center mb-5">
        <h3 className="fw-bold">Raise an Issue</h3>
        <p className="text-muted">
          Report public issues or submit confidential complaints to the Election Commission
        </p>
      </div>

      {/* Form Card */}
      <div className="row justify-content-center">
        <div className="col-md-8">
          <div className="card shadow-sm border-0">
            <div className="card-body">

              {/* Issue Type */}
              <div className="mb-4">
                <label className="form-label fw-semibold">
                  Issue Type
                </label>
                <select
                  className="form-select"
                  value={type}
                  onChange={e => setType(e.target.value)}
                >
                  <option value="PUBLIC">
                    Public Issue (Visible to Constituency)
                  </option>
                  <option value="EC">
                    Complaint to Election Commission (Private)
                  </option>
                </select>
              </div>

              {/* Description */}
              <div className="mb-4">
                <label className="form-label fw-semibold">
                  Description
                </label>
                <textarea
                  className="form-control"
                  placeholder="Describe the issue clearly and concisely"
                  value={description}
                  onChange={e => setDescription(e.target.value)}
                  rows={6}
                />
              </div>

              {/* Submit Button */}
              <div className="text-end">
                <button
                  className="btn btn-primary px-4"
                  onClick={submit}
                >
                  Submit
                </button>
              </div>

            </div>
          </div>
        </div>
      </div>

    </div>
  );
}

export default RaiseIssue;
