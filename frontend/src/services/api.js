import axios from "axios";

const api = axios.create({
    baseURL: import.meta.env.VITE_API_BASE_URL || "",
});

// Request interceptor: Attach Session ID
api.interceptors.request.use(
    (config) => {
        const sessionId = localStorage.getItem("sessionId");
        if (sessionId) {
            config.headers["X-Session-Id"] = sessionId;
        }
        return config;
    },
    (error) => Promise.reject(error)
);

// Response interceptor: Handle 401 Unauthorized
api.interceptors.response.use(
    (response) => response,
    (error) => {
        if (error.response && error.response.status === 401) {
            console.warn("Unauthorized! Clearing session and redirecting...");
            localStorage.removeItem("sessionId");
            localStorage.removeItem("userName");

            // Force redirect to auth page
            window.location.href = "/auth";
        }
        return Promise.reject(error);
    }
);

export default api;
