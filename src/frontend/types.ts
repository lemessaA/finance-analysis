// API Response Types
export interface StartupValidationResponse {
  idea: string;
  overall_score: number;
  market_score: number;
  competition_score: number;
  risk_score: number;
  verdict: string;
  key_strengths: string[];
  key_risks: string[];
  recommendations: string[];
  executive_summary?: string;
  market_research?: string;
}

export interface MarketIntelligenceResponse {
  industry: string;
  market_size_estimate: string;
  cagr_estimate: string;
  market_overview: string;
  key_trends: string[];
  risks: string[];
  top_competitors: Array<{
    name: string;
    market_share: string;
    market_share_estimate?: string;
    revenue: string;
    description?: string;
    strengths: string[];
    weaknesses: string[];
  }>;
  market_analysis: {
    market_size: string;
    growth_rate: string;
    competition_level: string;
    opportunity_score: number;
    trends: string[];
  };
  competitor_analysis: {
    top_competitors: Array<{
      name: string;
      market_share: string;
      revenue: string;
      strengths: string[];
      weaknesses: string[];
    }>;
  };
  opportunities: Array<{
    title: string;
    description: string;
    market_potential: string;
    difficulty: string;
  }>;
}

export interface FinancialReportResponse {
  filename: string;
  analysis: string;
  page_count: number;
  raw_text_length: number;
  key_highlights?: string[];
  key_risks?: string[];
  summary: {
    total_revenue: number;
    total_expenses: number;
    net_profit: number;
    profit_margin: number;
    growth_rate: number;
  };
  metrics: {
    revenue: number;
    net_profit: number;
    total_assets: number;
    total_liabilities: number;
    cash_flow: number;
    gross_margin: number;
    ebitda_margin: number;
    net_margin: number;
    operating_income: number;
    revenue_growth_yoy: number;
    current_ratio: number;
    debt_to_equity: number;
  };
  insights: Array<{
    category: string;
    insight: string;
    impact: 'high' | 'medium' | 'low';
  }>;
  recommendations: string[];
}

export interface ForecastRequest {
  metric: string;
  historical_data: DataPoint[];
  forecast_periods?: number;
  model_type?: string;
}

export interface ForecastResponse {
  metric: string;
  model_used: string;
  r_squared: number;
  avg_growth_rate: number;
  data_points: Array<{
    period: string;
    value: number;
    lower_bound?: number;
    upper_bound?: number;
    is_forecast: boolean;
  }>;
  interpretation: string;
  confidence: string;
}

export interface DataPoint {
  period: string;
  value: number;
}

export type LoadingState = 'idle' | 'loading' | 'success' | 'error';

export interface ApiError {
  message: string;
  detail: string;
  status: number;
}
