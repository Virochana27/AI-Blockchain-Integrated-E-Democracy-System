import { useEffect, useState } from "react";
import { getPosts } from "../../api/postsApi";

function Feed() {
  const [posts, setPosts] = useState([]);

  useEffect(() => {
    getPosts().then(res => setPosts(res.data));
  }, []);

  return (
    <div>
      <h1>Voter Feed</h1>
      {posts.map(p => <div key={p.id}>{p.content}</div>)}
    </div>
  );
}

export default Feed;
