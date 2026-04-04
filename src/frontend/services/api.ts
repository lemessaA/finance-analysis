import { apiClient } from '@/services/enhancedApi';

// Get current language from localStorage
const getCurrentLanguage = () => {
  if (typeof window !== 'undefined') {
    return localStorage.getItem('language') || 'en';
  }
  return 'en';
};

// Add language interceptor
apiClient.interceptors.request.use((config) => {
  const language = getCurrentLanguage();
  config.headers = {
    ...config.headers,
    'Accept-Language': language,
    'Content-Language': language,
  };
  return config;
});

// Startup validation API
export async function validateStartup(data: {
  idea: string;
  industry: string;
  targetMarket: string;
  businessStage: string;
  description?: string;
}) {
  const requestData = {
    idea: data.idea,
    industry: data.industry,
    target_market: data.targetMarket,
    business_stage: data.businessStage,
    additional_context: data.description
  };
  const response = await apiClient.post('/api/v1/startup/validate', requestData);
  return response;
}

// Market intelligence API
export async function getMarketIntelligence(data?: {
  industry?: string;
  targetMarket?: string;
}) {
  const requestData = {
    industry: data?.industry || "Technology",
    target_market: data?.targetMarket || "Global"
  };
  const response = await apiClient.post('/api/v1/market/analyze', requestData);
  return response;
}

// Financial Report Analyzer APIs
export async function analyzeFinancialReport(file: File) {
  const formData = new FormData();
  formData.append('file', file);

  const response = await apiClient.post('/api/v1/financial/analyze', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
  return response;
}

export async function compareFinancialReports(baselineReportId: string, currentReportId: string) {
  const response = await apiClient.post('/api/v1/financial/compare', {
    baseline_report_id: baselineReportId,
    current_report_id: currentReportId,
  });
  return response;
}

// ML forecasting API
export async function generateForecast(data: {
  metric: string;
  historical_data: Array<{ period: string; value: number }>;
  forecast_periods?: number;
  model_type?: string;
}) {
  const response = await apiClient.post('/api/v1/forecasting/forecast', data);
  return response;
}

// Dashboard Stats API
export async function getPlatformStats(): Promise<{
  status: string;
  data: {
    total_analyses: number;
    success_rate: number;
    api_calls: number;
    avg_score: number;
    recent_activity: Array<{
      type: 'startup' | 'market' | 'forecasting' | 'analyzer';
      title: string;
      score?: number;
      time: string;
      status: string;
    }>;
    breakdown: {
      startup_validations: number;
      market_intelligence: number;
      financial_forecasts: number;
      financial_analyses: number;
    };
  };
  last_updated: string;
}> {
  const response = await apiClient.get('/api/v1/database/stats');
  return response;
}

// Health check API
export async function healthCheck() {
  const response = await apiClient.get('/api/v1/health');
  return response;
}
