import { raiseIssue } from "../../api/issuesApi";

function RaiseIssue() {
  const submit = async () => {
    await raiseIssue({
      constituency_id: "UUID",
      description: "Issue description"
    });
    alert("Issue submitted");
  };

  return <button onClick={submit}>Raise Issue</button>;
}

export default RaiseIssue;
