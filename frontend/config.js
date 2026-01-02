// Configuration file for frontend
// Update this with your Railway backend URL after deployment
const BACKEND_CONFIG = {
    url: 'wss://your-railway-app.railway.app' // Replace with your actual Railway URL
};

// Make it available globally
if (typeof window !== 'undefined') {
    window.__BACKEND_URL__ = BACKEND_CONFIG.url;
}

