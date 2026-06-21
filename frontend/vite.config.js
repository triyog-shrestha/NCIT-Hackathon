import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// Dev server proxies /api/* straight to the Flask app in main.py, so the
// browser never needs to know the backend's real host/port and CORS never
// comes up. In production, point this at wherever main.py is actually
// deployed, or serve both behind the same reverse proxy.
export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    proxy: {
      '/api': {
        target: process.env.VITE_API_TARGET || 'http://127.0.0.1:5000',
        changeOrigin: true,
      },
    },
  },
})
