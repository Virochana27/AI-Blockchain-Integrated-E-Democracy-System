import { useState, useContext } from "react";
import { useNavigate } from "react-router-dom";
import { AuthContext } from "../context/AuthContext";

function Login() {
  const { login } = useContext(AuthContext);
  const navigate = useNavigate();

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const submit = async (e) => {
    e.preventDefault();
    setError("");
    setLoading(true);

    try {
      const role = await login(email, password);

      // Role-based redirect
      if (role === "EC") navigate("/ec");
      else if (role === "VOTER") navigate("/voter");
      else if (role === "REPRESENTATIVE") navigate("/rep");
      else navigate("/");
    } catch (err) {
      setError("Invalid email or password");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container-fluid d-flex justify-content-center align-items-center vh-100">
      <div className="card shadow-lg" style={{ width: "420px" }}>
        <div className="card-body p-4">

          <h3 className="text-center mb-1">E-Democracy Portal</h3>
          <p className="text-center text-muted mb-4">
            Secure login for citizens and officials
          </p>

          {error && (
            <div className="alert alert-danger py-2">
              {error}
            </div>
          )}

          <form onSubmit={submit}>
            <div className="mb-3">
              <label className="form-label">Email</label>
              <input
                type="email"
                className="form-control"
                placeholder="name@example.com"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
              />
            </div>

            <div className="mb-3">
              <label className="form-label">Password</label>
              <input
                type="password"
                className="form-control"
                placeholder="••••••••"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
              />
            </div>

            <button
              type="submit"
              className="btn btn-primary w-100"
              disabled={loading}
            >
              {loading ? "Signing in..." : "Login"}
            </button>
          </form>

          <hr className="my-4" />

          <p className="text-center text-muted small mb-0">
            © Election Commission — Secure Digital Democracy
          </p>
        </div>
      </div>
    </div>
  );
}

export default Login;
