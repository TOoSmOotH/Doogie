import React from 'react';
import { Navigate, Outlet } from 'react-router-dom';
import { useAuth } from '../hooks/useAuth';
import LoadingScreen from './LoadingScreen';

const AdminRoute: React.FC = () => {
  const { user, loading } = useAuth();

  // Show loading screen while checking authentication
  if (loading) {
    return <LoadingScreen />;
  }

  // Redirect to home if not authenticated or not an admin
  if (!user || user.role !== 'admin') {
    return <Navigate to="/chat" replace />;
  }

  // Render child routes if authenticated and admin
  return <Outlet />;
};

export default AdminRoute;