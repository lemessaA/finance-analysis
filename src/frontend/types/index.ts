// All TypeScript types for the AI Business Intelligence Platform

// ─── Startup Validator ────────────────────────────────────────────────────────
export interface StartupValidationRequest {
  idea: string;
  industry: string;
  target_market?: string;
  additional_context?: string;
}

export interface StartupValidationResponse {
  idea: string;
  industry: string;
  target_market: string;
  market_research: string;
  competitor_analysis: string;
  overall_score: number;
  market_score: number;
  competition_score: number;
  risk_score: number;
  verdict: "STRONG GO" | "GO" | "CONDITIONAL GO" | "NO GO";
  key_strengths: string[];
  key_risks: string[];
  recommendations: string[];
  executive_summary: string;
  error?: string | null;
}

// ─── Financial Analyzer ───────────────────────────────────────────────────────
export interface FinancialMetrics {
  revenue?: string;
  revenue_growth_yoy?: string;
  gross_margin?: string;
  ebitda?: string;
  ebitda_margin?: string;
  net_income?: string;
  net_margin?: string;
  operating_cash_flow?: string;
  free_cash_flow?: string;
  eps?: string;
  current_ratio?: string;
  debt_to_equity?: string;
}

export interface FinancialReportResponse {
  filename: string;
  page_count: number;
  metrics: FinancialMetrics;
  analysis: string;
  key_highlights: string[];
  key_risks: string[];
  raw_text_length: number;
}

// ─── Forecasting Engine ───────────────────────────────────────────────────────
export interface DataPoint {
  period: string;
  value: number;
}

export interface CompetitorModel {
  name: string;
  description: string;
  strengths: string[];
  weaknesses: string[];
  market_share_estimate?: string;
}

export interface MarketIntelligenceRequest {
  industry: string;
  target_market?: string;
}

export interface MarketIntelligenceResponse {
  industry: string;
  target_market: string;
  market_size_estimate: string;
  cagr_estimate: string;
  market_overview: string;
  key_trends: string[];
  opportunities: string[];
  risks: string[];
  top_competitors: CompetitorModel[];
  error?: string | null;
}

export interface ForecastRequest {
  metric: string;
  historical_data: DataPoint[];
  forecast_periods: number;
  model_type?: "linear" | "polynomial" | "auto";
}

export interface ForecastDataPoint {
  period: string;
  value: number;
  lower_bound?: number;
  upper_bound?: number;
  is_forecast: boolean;
}

export interface ForecastResponse {
  metric: string;
  model_used: string;
  r_squared: number;
  avg_growth_rate: number;
  data_points: ForecastDataPoint[];
  interpretation: string;
  confidence: "High" | "Medium" | "Low";
}

// ─── UI State ─────────────────────────────────────────────────────────────────
export type LoadingState = "idle" | "loading" | "success" | "error";

export interface ApiError {
  detail: string;
  status: number;
}
