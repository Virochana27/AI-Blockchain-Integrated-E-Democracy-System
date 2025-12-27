import { createPost } from "../../api/postsApi";

function CreatePost() {
  const submit = async () => {
    await createPost({
      constituency_id: "UUID",
      post_type: "PROJECT",
      content: "Project update"
    });
    alert("Post created");
  };

  return <button onClick={submit}>Create Post</button>;
}

export default CreatePost;
