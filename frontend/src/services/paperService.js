import axios from "axios";

// Create axios instance
const api = axios.create({
    baseURL: "http://localhost:5000/api",
});

// Add a request interceptor to include the session ID
api.interceptors.request.use(
    (config) => {
        const sessionId = localStorage.getItem("sessionId");
        if (sessionId) {
            config.headers["X-Session-Id"] = sessionId;
        }
        return config;
    },
    (error) => {
        return Promise.reject(error);
    }
);

export const getConfig = async () => {
    try {
        const response = await api.get("/config");
        return response.data;
    } catch (error) {
        throw error.response ? error.response.data : error;
    }
};

export const getAllPapers = async () => {
    try {
        const response = await api.get("/papers");
        return response.data;
    } catch (error) {
        throw error.response ? error.response.data : error;
    }
};

export const getPaperById = async (id) => {
    try {
        const response = await api.get(`/papers/${id}`);
        return response.data;
    } catch (error) {
        throw error.response ? error.response.data : error;
    }
};

export const generatePaper = async (data) => {
    try {
        const response = await api.post("/papers/generate", data);
        return response.data;
    } catch (error) {
        throw error.response ? error.response.data : error;
    }
};

export default {
    getConfig,
    getAllPapers,
    getPaperById,
    generatePaper
};
