import api from "./api";

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
