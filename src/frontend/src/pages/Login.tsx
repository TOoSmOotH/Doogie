import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../hooks/useAuth';
import { useTheme } from '../hooks/useTheme';
import ThemeToggle from '../components/ThemeToggle';

const Login: React.FC = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [errorMessage, setErrorMessage] = useState('');
  const { login } = useAuth();
  const { theme } = useTheme();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    setErrorMessage('');

    try {
      await login(email, password);
      // Redirect will happen automatically via protected route
    } catch (error: any) {
      setErrorMessage(error.response?.data?.detail || 'Login failed. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className={`min-h-screen flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8 ${
      theme === 'dark' ? 'bg-dark' : 'bg-light-off'
    }`}>
      <div className="max-w-md w-full space-y-8">
        <div>
          <h1 className={`text-center text-4xl font-extrabold ${
            theme === 'dark' ? 'text-white' : 'text-gray-900'
          }`}>Doogie</h1>
          <h2 className={`mt-6 text-center text-2xl font-bold ${
            theme === 'dark' ? 'text-gray-300' : 'text-gray-700'
          }`}>Sign in to your account</h2>
        </div>
        <form className="mt-8 space-y-6" onSubmit={handleSubmit}>
          <div className="rounded-md shadow-sm -space-y-px">
            <div>
              <label htmlFor="email-address" className="sr-only">
                Email address
              </label>
              <input
                id="email-address"
                name="email"
                type="email"
                autoComplete="email"
                required
                className={`appearance-none rounded-none relative block w-full px-3 py-3 border focus:outline-none focus:ring-primary focus:border-primary focus:z-10 sm:text-sm rounded-t-md ${
                  theme === 'dark'
                    ? 'border-dark-border placeholder-gray-500 text-white bg-dark-lighter'
                    : 'border-light-border placeholder-gray-400 text-gray-900 bg-white'
                }`}
                placeholder="Email address"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
              />
            </div>
            <div>
              <label htmlFor="password" className="sr-only">
                Password
              </label>
              <input
                id="password"
                name="password"
                type="password"
                autoComplete="current-password"
                required
                className={`appearance-none rounded-none relative block w-full px-3 py-3 border focus:outline-none focus:ring-primary focus:border-primary focus:z-10 sm:text-sm rounded-b-md ${
                  theme === 'dark'
                    ? 'border-dark-border placeholder-gray-500 text-white bg-dark-lighter'
                    : 'border-light-border placeholder-gray-400 text-gray-900 bg-white'
                }`}
                placeholder="Password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
              />
            </div>
          </div>

          {errorMessage && (
            <div className="text-red-500 text-sm text-center">{errorMessage}</div>
          )}

          <div>
            <button
              type="submit"
              disabled={isLoading}
              className="group relative w-full flex justify-center py-3 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-primary hover:bg-primary-dark focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary shadow-sm"
            >
              {isLoading ? 'Signing in...' : 'Sign in'}
            </button>
          </div>

          <div className="text-center space-y-4 mt-6">
            <Link to="/register" className="text-sm text-primary hover:text-primary-dark font-medium">
              Don't have an account? Register
            </Link>
            
            <div className="mt-4">
              <ThemeToggle />
            </div>
          </div>
        </form>
      </div>
    </div>
  );
};

export default Login;