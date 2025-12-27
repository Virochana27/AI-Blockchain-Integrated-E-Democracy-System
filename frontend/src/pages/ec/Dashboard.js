import { createElection } from "../../api/electionsApi";

function Dashboard() {
  const create = async () => {
    await createElection({
      constituency_id: "UUID",
      created_by: "EC_ID"
    });
    alert("Election created");
  };

  return (
    <div>
      <h1>EC Dashboard</h1>
      <button onClick={create}>Create Election</button>
    </div>
  );
}

export default Dashboard;
