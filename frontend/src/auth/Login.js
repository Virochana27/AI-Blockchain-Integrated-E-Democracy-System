import { useState, useContext } from "react";
import { useNavigate } from "react-router-dom";
import { AuthContext } from "../context/AuthContext";

function Login() {
  const { login } = useContext(AuthContext);
  const navigate = useNavigate();

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const submit = async (e) => {
    e.preventDefault();

    // login() returns role
    const role = await login(email, password);

    // Redirect based on role
    if (role === "EC") navigate("/ec");
    else if (role === "VOTER") navigate("/voter");
    else if (role === "REPRESENTATIVE") navigate("/rep");
    else if (role === "OPPOSITION") navigate("/opposition");
    else alert("Unknown role");
  };

  return (
    <form onSubmit={submit}>
      <h2>Login</h2>

      <input
        placeholder="Email"
        onChange={(e) => setEmail(e.target.value)}
        required
      />

      <input
        placeholder="Password"
        type="password"
        onChange={(e) => setPassword(e.target.value)}
        required
      />

      <button type="submit">Login</button>
    </form>
  );
}

export default Login;
