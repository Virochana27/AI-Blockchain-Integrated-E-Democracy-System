import Navbar from "../components/Navbar";

const VoterLayout = ({ children }) => {
  return (
    <>
      <Navbar />
      <div style={{ padding: "20px" }}>{children}</div>
    </>
  );
};

export default VoterLayout;
