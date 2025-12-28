import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { getECComplaints } from "../../api/electionsApi";

function Complaints() {
  const { id } = useParams(); // constituency id
  const [complaints, setComplaints] = useState([]);

  useEffect(() => {
    getECComplaints(id)
      .then(res => setComplaints(res.data))
      .catch(err => console.error(err));
  }, [id]);

  return (
    <div>
      <h2>Complaints to Election Commission</h2>

      {complaints.length === 0 && (
        <p>No complaints raised for this constituency</p>
      )}

      {complaints.map(c => (
        <div
          key={c.id}
          style={{
            border: "1px solid #ccc",
            padding: "10px",
            marginBottom: "10px"
          }}
        >
          <p><b>Complaint:</b> {c.message}</p>
          <p><b>Status:</b> {c.status}</p>
          <small>{new Date(c.created_at).toLocaleString()}</small>
        </div>
      ))}
    </div>
  );
}

export default Complaints;
