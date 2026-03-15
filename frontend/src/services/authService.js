import axios from "axios";

const api = axios.create({
    baseURL: import.meta.env.VITE_API_BASE_URL || "",
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
        if (response.data.user && response.data.user.name) {
            localStorage.setItem("userName", response.data.user.name);
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
        if (response.data.user && response.data.user.name) {
            localStorage.setItem("userName", response.data.user.name);
        }

        return response.data;
    } catch (error) {
        throw error.response ? error.response.data : error;
    }
};

export const logout = () => {
    localStorage.removeItem("sessionId");
    localStorage.removeItem("userName");
};

export default {
    register,
    login,
    logout
};
