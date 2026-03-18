import axios from "axios";
import type {
  StartupValidationRequest,
  StartupValidationResponse,
  FinancialReportResponse,
  ForecastRequest,
  ForecastResponse,
  MarketIntelligenceRequest,
  MarketIntelligenceResponse,
} from "@/types";

const api = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000",
  timeout: 120000, // 2 min — agents take time
  headers: { "Content-Type": "application/json" },
});

// ─── Startup Validator ────────────────────────────────────────────────────────
export async function validateStartup(
  payload: StartupValidationRequest
): Promise<StartupValidationResponse> {
  const { data } = await api.post<StartupValidationResponse>(
    "/api/v1/startup/validate",
    payload
  );
  return data;
}

// ─── Financial Analyzer ───────────────────────────────────────────────────────
export async function analyzeFinancialReport(
  file: File
): Promise<FinancialReportResponse> {
  const formData = new FormData();
  formData.append("file", file);
  const { data } = await api.post<FinancialReportResponse>(
    "/api/v1/financial/analyze",
    formData,
    { headers: { "Content-Type": "multipart/form-data" } }
  );
  return data;
}

// ─── Forecasting ──────────────────────────────────────────────────────────────
export async function generateForecast(
  payload: ForecastRequest
): Promise<ForecastResponse> {
  const { data } = await api.post<ForecastResponse>(
    "/api/v1/forecasting/forecast",
    payload
  );
  return data;
}

// ─── Health ───────────────────────────────────────────────────────────────────
export async function checkHealth(): Promise<boolean> {
  try {
    await api.get("/api/v1/health/");
    return true;
  } catch {
    return false;
  }
}

// ─── Market Intelligence ──────────────────────────────────────────────────────
export async function getMarketIntelligence(
  payload: MarketIntelligenceRequest
): Promise<MarketIntelligenceResponse> {
  const { data } = await api.post<MarketIntelligenceResponse>(
    "/api/v1/market/analyze",
    payload
  );
  return data;
}

// ─── Dashboard API ─────────────────────────────────────────────────────────────
export interface DashboardData {
  score: number;
  marketAnalysis: {
    marketSize: string;
    growthRate: string;
    competitionLevel: string;
    opportunityScore: number;
  };
  competitors: Array<{
    name: string;
    marketShare: string;
    revenue: string;
    strengths: string[];
    weaknesses: string[];
  }>;
  revenueForecast: Array<{
    month: string;
    actual: number;
    forecast: number;
  }>;
  financialComparison: Array<{
    category: string;
    yourCompany: number;
    industryAvg: number;
    topPerformer: number;
  }>;
  marketSegments: Array<{
    name: string;
    value: number;
    color: string;
  }>;
}

export async function getDashboardData(): Promise<DashboardData> {
  const { data } = await api.get<DashboardData>("/api/v1/dashboard/dashboard");
  return data;
}

export async function getStartupScore(): Promise<{
  score: number;
  breakdown: Record<string, number>;
  recommendation: string;
}> {
  const { data } = await api.get("/api/v1/dashboard/dashboard/score");
  return data;
}

export async function getMarketAnalysis(): Promise<{
  marketSize: string;
  growthRate: string;
  competitionLevel: string;
  opportunityScore: number;
  details?: Record<string, any>;
}> {
  const { data } = await api.get("/api/v1/dashboard/dashboard/market-analysis");
  return data;
}

export async function getCompetitors(): Promise<Array<{
  name: string;
  marketShare: string;
  revenue: string;
  strengths: string[];
  weaknesses: string[];
  description?: string;
}>> {
  const { data } = await api.get("/api/v1/dashboard/dashboard/competitors");
  return data;
}

export async function getRevenueForecast(): Promise<{
  forecast: Array<{
    month: string;
    actual: number;
    forecast: number;
  }>;
  model_used: string;
  confidence: number;
  next_month_forecast: number;
}> {
  const { data } = await api.get("/api/v1/dashboard/dashboard/revenue-forecast");
  return data;
}

export async function getFinancialComparison(): Promise<{
  metrics: Array<{
    category: string;
    yourCompany: number;
    industryAvg: number;
    topPerformer: number;
    percentile?: number;
  }>;
  overall_ranking: string;
  key_insights: string[];
}> {
  const { data } = await api.get("/api/v1/dashboard/dashboard/financial-comparison");
  return data;
}
