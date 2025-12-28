import api from "./axios";

export const createElection = (data) =>
  api.post("/elections", data);

export const getElections = () =>
  api.get("/elections");

export const getConstituencies = () =>
  api.get("/elections/constituencies");

export const getECComplaints = (constituencyId) =>
  api.get(`/elections/complaints/${constituencyId}`);


