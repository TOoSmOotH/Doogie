import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import path from 'path';

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
  server: {
    port: 3000,
    host: '0.0.0.0', // Listen on all interfaces, not just localhost
    proxy: {
      '/api': {
        target: 'http://api:8000', // Use Docker service name instead of localhost
        changeOrigin: true,
      },
      '/ws': {
        target: 'ws://api:8000', // Use Docker service name instead of localhost
        ws: true,
      },
    },
  },
  build: {
    outDir: 'dist',
    emptyOutDir: true,
  },
});