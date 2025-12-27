import Navbar from "../components/Navbar";
import Sidebar from "../components/Sidebar";

const ECLayout = ({ children }) => {
  return (
    <>
      <Navbar />
      <div style={{ display: "flex" }}>
        <Sidebar role="EC" />
        <div style={{ padding: "20px" }}>{children}</div>
      </div>
    </>
  );
};

export default ECLayout;
