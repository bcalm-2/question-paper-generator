import { Navigate } from "react-router-dom";
import { authService } from "../services/authService";

// Protected Route Component - Redirects to login if not authenticated
const ProtectedRoute = ({ children }) => {
  const isAuthenticated = authService.isAuthenticated();

  if (!isAuthenticated) {
    return <Navigate to="/auth" replace />;
  }

  return children;
};

export default ProtectedRoute;
