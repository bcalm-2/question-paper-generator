import axios from "axios";

const API_URL = "http://localhost:5000/api/auth";

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

export const register = async (userData) => {
    try {
        const response = await api.post("/auth/register", userData);

        // Save session ID if present
        const sessionId = response.headers["x-session-id"];
        if (sessionId) {
            localStorage.setItem("sessionId", sessionId);
        }

        return response.data;
    } catch (error) {
        throw error.response ? error.response.data : error;
    }
};

export const login = async (credentials) => {
    try {
        const response = await api.post("/auth/login", credentials);

        // Save session ID if present
        const sessionId = response.headers["x-session-id"];
        if (sessionId) {
            localStorage.setItem("sessionId", sessionId);
        }

        return response.data;
    } catch (error) {
        throw error.response ? error.response.data : error;
    }
};

export const logout = () => {
    localStorage.removeItem("sessionId");
};

export default {
    register,
    login,
    logout
};
