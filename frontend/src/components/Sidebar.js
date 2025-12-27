import { Link } from "react-router-dom";

const Sidebar = ({ role }) => {
  return (
    <div style={{ width: "200px", borderRight: "1px solid #ccc" }}>
      <ul>
        {role === "EC" && (
          <>
            <li><Link to="/ec">Dashboard</Link></li>
            <li><Link to="/ec/complaints">Complaints</Link></li>
          </>
        )}

        {role === "REPRESENTATIVE" && (
          <>
            <li><Link to="/rep">Dashboard</Link></li>
            <li><Link to="/rep/issues">Issues</Link></li>
          </>
        )}
      </ul>
    </div>
  );
};

export default Sidebar;
