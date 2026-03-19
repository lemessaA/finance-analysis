import axios from 'axios';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Dashboard API endpoints
export const dashboardApi = {
  // Get all dashboard data
  getDashboardData: async () => {
    try {
      const response = await api.get('/api/v1/dashboard/dashboard');
      return response.data;
    } catch (error) {
      console.error('Error fetching dashboard data:', error);
      throw error;
    }
  },

  // Get startup score
  getStartupScore: async () => {
    try {
      const response = await api.get('/api/v1/dashboard/dashboard/score');
      return response.data;
    } catch (error) {
      console.error('Error fetching startup score:', error);
      throw error;
    }
  },

  // Get market analysis
  getMarketAnalysis: async () => {
    try {
      const response = await api.get('/api/v1/dashboard/dashboard/market-analysis');
      return response.data;
    } catch (error) {
      console.error('Error fetching market analysis:', error);
      throw error;
    }
  },

  // Get competitors
  getCompetitors: async () => {
    try {
      const response = await api.get('/api/v1/dashboard/dashboard/competitors');
      return response.data;
    } catch (error) {
      console.error('Error fetching competitors:', error);
      throw error;
    }
  },

  // Get revenue forecast
  getRevenueForecast: async () => {
    try {
      const response = await api.get('/api/v1/dashboard/dashboard/revenue-forecast');
      return response.data;
    } catch (error) {
      console.error('Error fetching revenue forecast:', error);
      throw error;
    }
  },

  // Get financial comparison
  getFinancialComparison: async () => {
    try {
      const response = await api.get('/api/v1/dashboard/dashboard/financial-comparison');
      return response.data;
    } catch (error) {
      console.error('Error fetching financial comparison:', error);
      throw error;
    }
  },

  // Get business ideas
  getBusinessIdeas: async () => {
    try {
      const response = await api.get('/api/v1/dashboard/business-ideas');
      return response.data;
    } catch (error) {
      console.error('Error fetching business ideas:', error);
      throw error;
    }
  },

  // Refresh business ideas
  refreshBusinessIdeas: async () => {
    try {
      const response = await api.post('/api/v1/dashboard/business-ideas/refresh');
      return response.data;
    } catch (error) {
      console.error('Error refreshing business ideas:', error);
      throw error;
    }
  },

  // Get AI-generated dashboard data
  getAIGeneratedDashboard: async () => {
    try {
      const response = await api.get('/api/v1/dashboard/ai-generated');
      return response.data;
    } catch (error) {
      console.error('Error fetching AI-generated dashboard:', error);
      throw error;
    }
  },

  // Refresh AI-generated dashboard
  refreshAIDashboard: async () => {
    try {
      const response = await api.post('/api/v1/dashboard/ai-generated/refresh');
      return response.data;
    } catch (error) {
      console.error('Error refreshing AI dashboard:', error);
      throw error;
    }
  },
};

// Export default api for other uses
export default api;
