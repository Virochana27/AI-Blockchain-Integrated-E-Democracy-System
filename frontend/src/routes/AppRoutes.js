import { Routes, Route } from "react-router-dom";
import Login from "../auth/Login";
import Register from "../auth/Register";
import ProtectedRoute from "../auth/ProtectedRoute";

import ECDashboard from "../pages/ec/Dashboard";
import ConstituencyView from "../pages/ec/ConstituencyView";
import CandidateReview from "../pages/ec/CandidateReview";
import Complaints from "../pages/ec/Complaints";
import ElectionDashboard from "../pages/ec/ElectionDashboard";

import RaiseIssue from "../pages/voter/RaiseIssue";
import Elections from "../pages/voter/Elections";
import Vote from "../pages/voter/Vote";


import VoterFeed from "../pages/voter/Feed";
import RepDashboard from "../pages/representative/Dashboard";

function AppRoutes() {
  return (
    <Routes>
      {/* Auth */}
      <Route path="/login" element={<Login />} />
      <Route path="/register" element={<Register />} />

      {/* EC routes */}
      <Route
        path="/ec"
        element={
          <ProtectedRoute>
            <ECDashboard />
          </ProtectedRoute>
        }
      />

      <Route
        path="/ec/constituency/:id"
        element={
          <ProtectedRoute>
            <ConstituencyView />
          </ProtectedRoute>
        }
      />

      <Route
        path="/ec/candidates"
        element={
          <ProtectedRoute>
            <CandidateReview />
          </ProtectedRoute>
        }
      />

      <Route
        path="/ec/complaints"
        element={
          <ProtectedRoute>
            <Complaints />
          </ProtectedRoute>
        }
      />

      <Route
  path="/ec/constituency/:id/election"
  element={<ProtectedRoute><ElectionDashboard /></ProtectedRoute>}
/>


      {/* Voter */}
      <Route
        path="/voter"
        element={
          <ProtectedRoute>
            <VoterFeed />
          </ProtectedRoute>
        }
      />

      {/* Representative */}
      <Route
        path="/rep"
        element={
          <ProtectedRoute>
            <RepDashboard />
          </ProtectedRoute>
        }
      />
      <Route
  path="/ec/complaints/:id"
  element={
    <ProtectedRoute>
      <Complaints />
    </ProtectedRoute>
  }
/>

<Route
  path="/voter/raise-issue"
  element={
    <ProtectedRoute>
      <RaiseIssue />
    </ProtectedRoute>
  }
/>

<Route
  path="/voter/elections"
  element={
    <ProtectedRoute>
      <Elections />
    </ProtectedRoute>
  }
/>

<Route
  path="/voter/vote"
  element={
    <ProtectedRoute>
      <Vote />
    </ProtectedRoute>
  }
/>

    </Routes>

    
  );
}

export default AppRoutes;
