import { useParams, useNavigate } from "react-router-dom";

function ConstituencyView() {
  const { id } = useParams();
  const navigate = useNavigate();

  return (
    <div>
      <h2>Constituency Dashboard</h2>
      <p>Constituency ID: {id}</p>

      <button onClick={() => navigate("/ec/candidates")}>
        Review Candidates
      </button>

      <button onClick={() => navigate(`/ec/complaints/${id}`)}>
        View Complaints
      </button>

      <button onClick={() => navigate("/ec/create-election")}>
        Announce Election
      </button>
    </div>
  );
}

export default ConstituencyView;
