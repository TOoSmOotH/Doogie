/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  darkMode: 'class', // or 'media' for OS preference
  theme: {
    extend: {
      colors: {
        primary: {
          DEFAULT: '#5436DA', // Purple similar to Claude
          dark: '#4520C5',
          light: '#7C68E3',
        },
        secondary: {
          DEFAULT: '#10b981',
          dark: '#059669',
        },
        dark: {
          DEFAULT: '#1A1A1A', // Dark background
          lighter: '#2D2D2D', // Slightly lighter dark
          sidebar: '#202123', // Dark sidebar
          border: '#383838', // Border color for dark mode
        },
        light: {
          DEFAULT: '#FFFFFF',
          off: '#F7F7F8', // Off-white background
          sidebar: '#F0F0F0', // Light sidebar
          border: '#E5E5E5', // Border color for light mode
        },
        danger: '#ef4444', // Added for btn-danger
        warning: '#f59e0b',
        success: '#10b981',
      },
      fontFamily: {
        sans: [
          '-apple-system',
          'BlinkMacSystemFont',
          '"Segoe UI"',
          'Roboto',
          '"Helvetica Neue"',
          'Arial',
          'sans-serif',
        ],
        mono: [
          'ui-monospace',
          'SFMono-Regular',
          'Menlo',
          'Monaco',
          'Consolas',
          '"Liberation Mono"',
          '"Courier New"',
          'monospace',
        ],
      },
      animation: {
        'fade-in': 'fadeIn 0.5s ease-in-out',
        'slide-in': 'slideIn 0.5s ease-in-out',
        'slide-up': 'slideUp 0.5s ease-in-out',
        'pulse-slow': 'pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite',
      },
      keyframes: {
        fadeIn: {
          '0%': { opacity: 0 },
          '100%': { opacity: 1 },
        },
        slideIn: {
          '0%': { transform: 'translateX(-10px)', opacity: 0 },
          '100%': { transform: 'translateX(0)', opacity: 1 },
        },
        slideUp: {
          '0%': { transform: 'translateY(10px)', opacity: 0 },
          '100%': { transform: 'translateY(0)', opacity: 1 },
        },
      },
    },
  },
  plugins: [],
}