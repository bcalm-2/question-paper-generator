import axios from "axios";
import { tokenService } from "../utils/tokenService";

// Base API URL
const API_BASE_URL = "http://localhost:5000/api";

// Create axios instance with base configuration
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
  headers: {
    "Content-Type": "application/json",
  },
});

// Request interceptor to attach token to every request
apiClient.interceptors.request.use(
  (config) => {
    const token = tokenService.getToken();
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  },
);

// Response interceptor to handle common errors
apiClient.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    // Handle unauthorized errors
    if (error.response?.status === 401) {
      tokenService.clearAuth();
      window.location.href = "/";
    }

    // Handle token expiration
    if (error.response?.status === 403) {
      tokenService.clearAuth();
      window.location.href = "/";
    }

    return Promise.reject(error);
  },
);

export default apiClient;
