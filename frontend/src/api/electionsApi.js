import api from "./axios";

export const createElection = (data) =>
  api.post("/elections", data);

export const getElections = () =>
  api.get("/elections");
