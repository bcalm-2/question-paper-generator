import axios from "axios";

export const generatePaper = (data) => {
  return axios.post(
    "http://localhost:5000/api/generate-paper",
    data
  );
};
