import React from 'react';

const LoadingScreen: React.FC = () => {
  return (
    <div className="flex items-center justify-center min-h-screen bg-gray-900">
      <div className="text-center">
        <div className="inline-block animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-primary mb-4"></div>
        <h2 className="text-xl font-semibold text-white">Loading...</h2>
        <p className="text-gray-400">Please wait while we prepare your experience</p>
      </div>
    </div>
  );
};

export default LoadingScreen;