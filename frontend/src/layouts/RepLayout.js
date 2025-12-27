import Navbar from "../components/Navbar";
import Sidebar from "../components/Sidebar";

const RepLayout = ({ children }) => {
  return (
    <>
      <Navbar />
      <div style={{ display: "flex" }}>
        <Sidebar role="REPRESENTATIVE" />
        <div style={{ padding: "20px" }}>{children}</div>
      </div>
    </>
  );
};

export default RepLayout;
