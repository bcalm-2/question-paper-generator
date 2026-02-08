// Token management utility

const TOKEN_KEY = "auth_token";
const USER_KEY = "user_data";

export const tokenService = {
  // Get token from localStorage
  getToken() {
    return localStorage.getItem(TOKEN_KEY);
  },

  // Save token to localStorage
  setToken(token) {
    localStorage.setItem(TOKEN_KEY, token);
  },

  // Remove token from localStorage
  removeToken() {
    localStorage.removeItem(TOKEN_KEY);
  },

  // Check if user is authenticated
  isAuthenticated() {
    return !!this.getToken();
  },

  // Get user data from localStorage
  getUser() {
    const user = localStorage.getItem(USER_KEY);
    return user ? JSON.parse(user) : null;
  },

  // Save user data to localStorage
  setUser(user) {
    localStorage.setItem(USER_KEY, JSON.stringify(user));
  },

  // Remove user data from localStorage
  removeUser() {
    localStorage.removeItem(USER_KEY);
  },

  // Clear all auth data (logout)
  clearAuth() {
    this.removeToken();
    this.removeUser();
  },
};
