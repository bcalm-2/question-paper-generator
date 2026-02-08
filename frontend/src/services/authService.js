import axios from "axios";

const API_URL = "http://localhost:5000/api/auth";

const api = axios.create({
    baseURL: "http://localhost:5000/api",
});

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
