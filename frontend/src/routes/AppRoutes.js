import { Routes, Route } from "react-router-dom";
import Login from "../auth/Login";
import Register from "../auth/Register";
import ProtectedRoute from "../auth/ProtectedRoute";

import ECDashboard from "../pages/ec/Dashboard";
import VoterFeed from "../pages/voter/Feed";
import RepDashboard from "../pages/representative/Dashboard";

function AppRoutes() {
  return (
    <Routes>
      <Route path="/login" element={<Login />} />
      <Route path="/register" element={<Register />} />

      <Route path="/ec" element={
        <ProtectedRoute><ECDashboard /></ProtectedRoute>
      } />

      <Route path="/voter" element={
        <ProtectedRoute><VoterFeed /></ProtectedRoute>
      } />

      <Route path="/rep" element={
        <ProtectedRoute><RepDashboard /></ProtectedRoute>
      } />
    </Routes>
  );
}

export default AppRoutes;
