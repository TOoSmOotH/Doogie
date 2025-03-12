import React, { useState } from 'react';
import { Outlet, Link, useNavigate, useLocation } from 'react-router-dom';
import { useAuth } from '../hooks/useAuth';
import { useTheme } from '../hooks/useTheme';

const Layout: React.FC = () => {
  const { user, logout } = useAuth();
  const { theme, toggleTheme } = useTheme();
  const navigate = useNavigate();
  const location = useLocation();
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  const isActive = (path: string) => {
    if (location.pathname.startsWith(path)) {
      return theme === 'dark' ? 'bg-gray-800' : 'bg-blue-50 text-blue-700';
    }
    return '';
  };

  return (
    <div className={`flex h-screen ${theme === 'dark' ? 'bg-dark text-white' : 'bg-light-off text-gray-900'}`}>
      {/* Sidebar */}
      <div className="hidden md:flex md:flex-shrink-0">
        <div className="flex flex-col w-64">
          <div className="sidebar flex flex-col h-0 flex-1">
            <div className="flex-1 flex flex-col pt-5 pb-4 overflow-y-auto">
              <div className="flex items-center flex-shrink-0 px-4">
                <h1 className="text-2xl font-bold">Doogie</h1>
              </div>
              <nav className="mt-5 flex-1 px-2 space-y-1">
                <Link
                  to="/chat"
                  className={`group flex items-center px-3 py-2 text-base font-medium rounded-md mb-1 ${
                    isActive('/chat')
                      ? theme === 'dark'
                        ? 'bg-dark-lighter text-white'
                        : 'bg-light text-primary'
                      : theme === 'dark'
                        ? 'text-gray-300 hover:bg-dark-lighter hover:text-white'
                        : 'text-gray-700 hover:bg-light'
                  }`}
                >
                  <svg
                    className={`mr-3 h-5 w-5 ${
                      isActive('/chat')
                        ? 'text-primary'
                        : theme === 'dark' ? 'text-gray-400' : 'text-gray-500'
                    }`}
                    xmlns="http://www.w3.org/2000/svg"
                    fill="none"
                    viewBox="0 0 24 24"
                    stroke="currentColor"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={2}
                      d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z"
                    />
                  </svg>
                  Chat
                </Link>

                <Link
                  to="/documents"
                  className={`group flex items-center px-3 py-2 text-base font-medium rounded-md mb-1 ${
                    isActive('/documents')
                      ? theme === 'dark'
                        ? 'bg-dark-lighter text-white'
                        : 'bg-light text-primary'
                      : theme === 'dark'
                        ? 'text-gray-300 hover:bg-dark-lighter hover:text-white'
                        : 'text-gray-700 hover:bg-light'
                  }`}
                >
                  <svg
                    className={`mr-3 h-5 w-5 ${
                      isActive('/documents')
                        ? 'text-primary'
                        : theme === 'dark' ? 'text-gray-400' : 'text-gray-500'
                    }`}
                    xmlns="http://www.w3.org/2000/svg"
                    fill="none"
                    viewBox="0 0 24 24"
                    stroke="currentColor"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={2}
                      d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
                    />
                  </svg>
                  Documents
                </Link>

                <Link
                  to="/settings"
                  className={`group flex items-center px-3 py-2 text-base font-medium rounded-md mb-1 ${
                    isActive('/settings')
                      ? theme === 'dark'
                        ? 'bg-dark-lighter text-white'
                        : 'bg-light text-primary'
                      : theme === 'dark'
                        ? 'text-gray-300 hover:bg-dark-lighter hover:text-white'
                        : 'text-gray-700 hover:bg-light'
                  }`}
                >
                  <svg
                    className={`mr-3 h-5 w-5 ${
                      isActive('/settings')
                        ? 'text-primary'
                        : theme === 'dark' ? 'text-gray-400' : 'text-gray-500'
                    }`}
                    xmlns="http://www.w3.org/2000/svg"
                    fill="none"
                    viewBox="0 0 24 24"
                    stroke="currentColor"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={2}
                      d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z"
                    />
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={2}
                      d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"
                    />
                  </svg>
                  Settings
                </Link>

                {user && user.role === 'admin' && (
                  <Link
                    to="/admin"
                    className={`group flex items-center px-3 py-2 text-base font-medium rounded-md mb-1 ${
                      isActive('/admin')
                        ? theme === 'dark'
                          ? 'bg-dark-lighter text-white'
                          : 'bg-light text-primary'
                        : theme === 'dark'
                          ? 'text-gray-300 hover:bg-dark-lighter hover:text-white'
                          : 'text-gray-700 hover:bg-light'
                    }`}
                  >
                    <svg
                      className={`mr-3 h-5 w-5 ${
                        isActive('/admin')
                          ? 'text-primary'
                          : theme === 'dark' ? 'text-gray-400' : 'text-gray-500'
                      }`}
                      xmlns="http://www.w3.org/2000/svg"
                      fill="none"
                      viewBox="0 0 24 24"
                      stroke="currentColor"
                    >
                      <path
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        strokeWidth={2}
                        d="M12 6V4m0 2a2 2 0 100 4m0-4a2 2 0 110 4m-6 8a2 2 0 100-4m0 4a2 2 0 110-4m0 4v2m0-6V4m6 6v10m6-2a2 2 0 100-4m0 4a2 2 0 110-4m0 4v2m0-6V4"
                      />
                    </svg>
                    Admin
                  </Link>
                )}
                
                {/* Theme Toggle Button */}
                <button
                  onClick={toggleTheme}
                  className={`mt-6 group flex items-center px-3 py-2 text-base font-medium rounded-md ${
                    theme === 'dark'
                      ? 'text-gray-300 hover:bg-dark-lighter'
                      : 'text-gray-600 hover:bg-light'
                  }`}
                >
                  {theme === 'dark' ? (
                    <svg
                      className="mr-3 h-5 w-5 text-yellow-400"
                      xmlns="http://www.w3.org/2000/svg"
                      fill="none"
                      viewBox="0 0 24 24"
                      stroke="currentColor"
                    >
                      <path
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        strokeWidth={2}
                        d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z"
                      />
                    </svg>
                  ) : (
                    <svg
                      className="mr-3 h-5 w-5 text-gray-600"
                      xmlns="http://www.w3.org/2000/svg"
                      fill="none"
                      viewBox="0 0 24 24"
                      stroke="currentColor"
                    >
                      <path
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        strokeWidth={2}
                        d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z"
                      />
                    </svg>
                  )}
                  {theme === 'dark' ? 'Light Mode' : 'Dark Mode'}
                </button>
              </nav>
            </div>
            <div className={`flex-shrink-0 flex p-4 border-t ${theme === 'dark' ? 'border-dark-border' : 'border-light-border'}`}>
              <div className="flex-shrink-0 w-full group block">
                <div className="flex items-center">
                  <div>
                    <div className={`inline-block h-9 w-9 rounded-full text-center leading-9 ${
                      theme === 'dark' ? 'bg-dark-lighter text-primary-light' : 'bg-primary-light text-primary'
                    }`}>
                      {user?.full_name?.charAt(0) || user?.email?.charAt(0) || 'U'}
                    </div>
                  </div>
                  <div className="ml-3">
                    <p className={`text-sm font-medium ${theme === 'dark' ? 'text-white' : 'text-gray-900'}`}>
                      {user?.full_name || user?.email}
                    </p>
                    <button
                      onClick={handleLogout}
                      className={`text-xs font-medium ${
                        theme === 'dark' ? 'text-gray-400 hover:text-white' : 'text-gray-500 hover:text-gray-700'
                      }`}
                    >
                      Logout
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Mobile menu */}
      <div className="md:hidden flex flex-col w-full">
        <div className={`px-4 py-3 flex items-center justify-between ${theme === 'dark' ? 'bg-dark-sidebar' : 'bg-light-sidebar'} border-b ${theme === 'dark' ? 'border-dark-border' : 'border-light-border'}`}>
          <h1 className="text-xl font-bold">Doogie</h1>
          <button
            onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
            className={theme === 'dark' ? 'text-gray-300 hover:text-white' : 'text-gray-600 hover:text-gray-900'}
          >
            <svg
              className="h-6 w-6"
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              {isMobileMenuOpen ? (
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M6 18L18 6M6 6l12 12"
                />
              ) : (
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M4 6h16M4 12h16M4 18h16"
                />
              )}
            </svg>
          </button>
        </div>

        {isMobileMenuOpen && (
          <div className={`px-2 pt-2 pb-3 space-y-1 ${theme === 'dark' ? 'bg-dark-sidebar' : 'bg-light-sidebar'} border-b ${theme === 'dark' ? 'border-dark-border' : 'border-light-border'}`}>
            <Link
              to="/chat"
              className={`block px-3 py-2 rounded-md text-base font-medium ${
                isActive('/chat')
                  ? theme === 'dark' ? 'bg-dark-lighter text-white' : 'bg-light text-primary'
                  : theme === 'dark' ? 'text-gray-300 hover:bg-dark-lighter' : 'text-gray-700 hover:bg-light'
              }`}
              onClick={() => setIsMobileMenuOpen(false)}
            >
              Chat
            </Link>
            <Link
              to="/documents"
              className={`block px-3 py-2 rounded-md text-base font-medium ${
                isActive('/documents')
                  ? theme === 'dark' ? 'bg-dark-lighter text-white' : 'bg-light text-primary'
                  : theme === 'dark' ? 'text-gray-300 hover:bg-dark-lighter' : 'text-gray-700 hover:bg-light'
              }`}
              onClick={() => setIsMobileMenuOpen(false)}
            >
              Documents
            </Link>
            <Link
              to="/settings"
              className={`block px-3 py-2 rounded-md text-base font-medium ${
                isActive('/settings')
                  ? theme === 'dark' ? 'bg-dark-lighter text-white' : 'bg-light text-primary'
                  : theme === 'dark' ? 'text-gray-300 hover:bg-dark-lighter' : 'text-gray-700 hover:bg-light'
              }`}
              onClick={() => setIsMobileMenuOpen(false)}
            >
              Settings
            </Link>
            {user && user.role === 'admin' && (
              <Link
                to="/admin"
                className={`block px-3 py-2 rounded-md text-base font-medium ${
                  isActive('/admin')
                    ? theme === 'dark' ? 'bg-dark-lighter text-white' : 'bg-light text-primary'
                    : theme === 'dark' ? 'text-gray-300 hover:bg-dark-lighter' : 'text-gray-700 hover:bg-light'
                }`}
                onClick={() => setIsMobileMenuOpen(false)}
              >
                Admin
              </Link>
            )}
            <button
              onClick={handleLogout}
              className={`block w-full text-left px-3 py-2 rounded-md text-base font-medium ${
                theme === 'dark'
                  ? 'text-gray-300 hover:bg-dark-lighter'
                  : 'text-gray-700 hover:bg-light'
              }`}
            >
              Logout ({user?.email})
            </button>
          </div>
        )}
      </div>

      {/* Main content */}
      <div className="flex-1 flex flex-col overflow-hidden">
        <main className={`flex-1 overflow-y-auto ${theme === 'dark' ? 'bg-dark' : 'bg-light-off'}`}>
          <div className="py-6">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 md:px-8">
              <Outlet />
            </div>
          </div>
        </main>
      </div>
    </div>
  );
};

export default Layout;