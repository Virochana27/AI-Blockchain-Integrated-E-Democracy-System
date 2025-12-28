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
    <div>
      <h1>Election Commission Dashboard</h1>

      {constituencies.length === 0 && (
        <p>No constituencies found</p>
      )}

      <ul>
        {constituencies.map(c => (
          <li key={c.id}>
            <b>{c.name}</b> ({c.state})
            <button
              onClick={() => navigate(`/ec/constituency/${c.id}`)}
            >
              View
            </button>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default Dashboard;
