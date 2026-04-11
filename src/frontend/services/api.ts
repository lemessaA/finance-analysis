import { apiClient } from '@/services/enhancedApi';

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

// Health check API
export async function healthCheck() {
  const response = await apiClient.get('/api/v1/health/');
  return response;
}
