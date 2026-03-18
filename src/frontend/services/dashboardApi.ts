import axios from 'axios';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Dashboard API endpoints
export const dashboardApi = {
  // Get all dashboard data
  getDashboardData: async () => {
    try {
      const response = await api.get('/api/dashboard/dashboard');
      return response.data;
    } catch (error) {
      console.error('Error fetching dashboard data:', error);
      throw error;
    }
  },

  // Get startup score
  getStartupScore: async () => {
    try {
      const response = await api.get('/api/dashboard/dashboard/score');
      return response.data;
    } catch (error) {
      console.error('Error fetching startup score:', error);
      throw error;
    }
  },

  // Get market analysis
  getMarketAnalysis: async () => {
    try {
      const response = await api.get('/api/dashboard/dashboard/market-analysis');
      return response.data;
    } catch (error) {
      console.error('Error fetching market analysis:', error);
      throw error;
    }
  },

  // Get competitors
  getCompetitors: async () => {
    try {
      const response = await api.get('/api/dashboard/dashboard/competitors');
      return response.data;
    } catch (error) {
      console.error('Error fetching competitors:', error);
      throw error;
    }
  },

  // Get revenue forecast
  getRevenueForecast: async () => {
    try {
      const response = await api.get('/api/dashboard/dashboard/revenue-forecast');
      return response.data;
    } catch (error) {
      console.error('Error fetching revenue forecast:', error);
      throw error;
    }
  },

  // Get financial comparison
  getFinancialComparison: async () => {
    try {
      const response = await api.get('/api/dashboard/dashboard/financial-comparison');
      return response.data;
    } catch (error) {
      console.error('Error fetching financial comparison:', error);
      throw error;
    }
  },
};

// Export default api for other uses
export default api;
