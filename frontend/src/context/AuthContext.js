import { createContext, useState, useEffect } from "react";
import { loginUser } from "../api/authApi";

export const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);

  // Restore session on refresh
  useEffect(() => {
    const token = localStorage.getItem("token");
    const role = localStorage.getItem("role");
    const constituency_id = localStorage.getItem("constituency_id");

    if (token && role) {
      setUser({ role, constituency_id });
    }
  }, []);

  const login = async (email, password) => {
    const res = await loginUser(email, password);

    // Store everything needed for routing & authorization
    localStorage.setItem("token", res.data.access_token);
    localStorage.setItem("role", res.data.role);
    localStorage.setItem("constituency_id", res.data.constituency_id);

    setUser({
      role: res.data.role,
      constituency_id: res.data.constituency_id
    });

    return res.data.role; // return role for redirect
  };

  const logout = () => {
    localStorage.clear();
    setUser(null);
    window.location.href = "/login";
  };

  return (
    <AuthContext.Provider value={{ user, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
};
