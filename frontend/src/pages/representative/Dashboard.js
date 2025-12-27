import { createPost } from "../../api/postsApi";

function Dashboard() {
  const post = async () => {
    await createPost({
      constituency_id: "UUID",
      post_type: "POLICY",
      content: "New policy announcement"
    });
    alert("Post created");
  };

  return (
    <div>
      <h1>Representative Dashboard</h1>
      <button onClick={post}>Create Post</button>
    </div>
  );
}

export default Dashboard;
