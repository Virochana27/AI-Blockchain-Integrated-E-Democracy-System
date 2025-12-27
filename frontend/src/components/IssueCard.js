const IssueCard = ({ issue }) => {
  return (
    <div style={{ border: "1px solid #ddd", margin: "10px", padding: "10px" }}>
      <p>{issue.description}</p>
      <small>Status: {issue.status}</small>
    </div>
  );
};

export default IssueCard;
