import api from "./axios";

export const createElection = (data) =>
  api.post("/elections/", data);

export const getElections = () =>
  api.get("/elections");

export const getConstituencies = () =>
  api.get("/elections/constituencies");

export const getECComplaints = (constituencyId) =>
  api.get(`/elections/complaints/${constituencyId}`);

// EC – Candidate applications by election
export const getCandidateApplications = (electionId) =>
  api.get(`/elections/applications/${electionId}`);

export const updateCandidateStatus = (applicationId, status) =>
  api.put(`/elections/applications/${applicationId}`, { status });

export const getElectionByConstituency = (constituencyId) =>
  api.get(`/elections/by-constituency/${constituencyId}`);

export const updateElection = (electionId, data) =>
  api.put(`/elections/${electionId}`, data);

export const getVoterElection = () =>
  api.get("/elections/voter");

export const raiseECComplaint = (data) =>
  api.post("/issues/complaint", data);

export const applyAsCandidate = (data) =>
  api.post("/elections/apply", data);


