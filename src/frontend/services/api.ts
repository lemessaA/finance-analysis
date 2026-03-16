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
