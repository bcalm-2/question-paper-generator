import apiClient from "./api";
import { tokenService } from "../utils/tokenService";

// Auth service for handling authentication operations
export const authService = {
  // User registration
  async register(userData) {
    try {
      const response = await apiClient.post("/register", userData);
      return {
        success: true,
        message: response.data.message || "Registration successful",
        data: response.data,
      };
    } catch (error) {
      return {
        success: false,
        message:
          error.response?.data?.message ||
          "Registration failed. Please try again.",
        error: error.response?.data,
      };
    }
  },

  // User login
  async login(credentials) {
    try {
      const response = await apiClient.post("/login", credentials);

      // Store token and user data
      if (response.data.token) {
        tokenService.setToken(response.data.token);
      }

      if (response.data.user) {
        tokenService.setUser(response.data.user);
      }

      return {
        success: true,
        message: response.data.message || "Login successful",
        data: response.data,
      };
    } catch (error) {
      return {
        success: false,
        message: error.response?.data?.message || "Invalid email or password",
        error: error.response?.data,
      };
    }
  },

  // User logout
  async logout() {
    try {
      // Call backend logout endpoint if exists
      await apiClient.post("/logout");
    } catch (error) {
      console.error("Logout error:", error);
    } finally {
      // Clear local storage regardless of API call result
      tokenService.clearAuth();
    }
  },

  // Get current user
  getCurrentUser() {
    return tokenService.getUser();
  },

  // Check if user is authenticated
  isAuthenticated() {
    return tokenService.isAuthenticated();
  },
};
