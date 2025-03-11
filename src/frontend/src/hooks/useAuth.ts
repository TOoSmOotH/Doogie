import { useState, useEffect, createContext, useContext } from 'react';
import axios from 'axios';

// Define user type
export interface User {
  id: string;
  email: string;
  full_name?: string;
  role: string;
  status: string;
}

// Define auth context type
interface AuthContextType {
  user: User | null;
  loading: boolean;
  error: string | null;
  login: (email: string, password: string) => Promise<void>;
  register: (email: string, password: string, fullName: string) => Promise<void>;
  logout: () => void;
  checkAuth: () => Promise<void>;
}

// Create auth context
const AuthContext = createContext<AuthContextType | undefined>(undefined);

// Auth provider props
interface AuthProviderProps {
  children: React.ReactNode;
}

// Auth provider component
export const AuthProvider: React.FC<AuthProviderProps> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  // Check if user is authenticated on mount
  useEffect(() => {
    checkAuth();
  }, []);

  // Check authentication status
  const checkAuth = async (): Promise<void> => {
    try {
      setLoading(true);
      const token = localStorage.getItem('token');
      
      if (!token) {
        setUser(null);
        setLoading(false);
        return;
      }
      
      // Set auth header
      axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
      
      // Get user info
      const response = await axios.get('/api/auth/me');
      setUser(response.data);
      setError(null);
    } catch (err) {
      console.error('Authentication check failed:', err);
      setUser(null);
      localStorage.removeItem('token');
      delete axios.defaults.headers.common['Authorization'];
    } finally {
      setLoading(false);
    }
  };

  // Login function
  const login = async (email: string, password: string): Promise<void> => {
    try {
      setLoading(true);
      setError(null);
      
      // Get token
      const response = await axios.post('/api/auth/token', {
        username: email, // API expects username field
        password,
      });
      
      const { access_token } = response.data;
      
      // Save token
      localStorage.setItem('token', access_token);
      
      // Set auth header
      axios.defaults.headers.common['Authorization'] = `Bearer ${access_token}`;
      
      // Get user info
      await checkAuth();
    } catch (err: any) {
      console.error('Login failed:', err);
      setError(err.response?.data?.detail || 'Login failed. Please try again.');
      throw err;
    } finally {
      setLoading(false);
    }
  };

  // Register function
  const register = async (email: string, password: string, fullName: string): Promise<void> => {
    try {
      setLoading(true);
      setError(null);
      
      // Register user
      await axios.post('/api/auth/register', {
        email,
        password,
        full_name: fullName,
      });
      
      // Show success message but don't log in automatically
      // since admin approval is required
    } catch (err: any) {
      console.error('Registration failed:', err);
      setError(err.response?.data?.detail || 'Registration failed. Please try again.');
      throw err;
    } finally {
      setLoading(false);
    }
  };

  // Logout function
  const logout = (): void => {
    localStorage.removeItem('token');
    delete axios.defaults.headers.common['Authorization'];
    setUser(null);
  };

  // Auth context value
  const value = {
    user,
    loading,
    error,
    login,
    register,
    logout,
    checkAuth,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

// Hook to use auth context
export const useAuth = (): AuthContextType => {
  const context = useContext(AuthContext);
  
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  
  return context;
};

export default useAuth;