import api from "./axios";

export const raiseIssue = (data) =>
  api.post("/issues", data);

export const getIssues = () =>
  api.get("/issues");
