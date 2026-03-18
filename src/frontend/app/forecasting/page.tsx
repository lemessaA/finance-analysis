"use client";

import { useState } from "react";
import { generateForecast } from "@/services/api";
import type { ForecastRequest, ForecastResponse, LoadingState, DataPoint } from "@/types";
import {
  TrendingUp,
  LineChart,
  Calendar,
  Layers,
  Activity,
  AlertOctagon,
  Loader2,
  CheckCircle2,
  Target
} from "lucide-react";

export default function ForecastingPage() {
  const [form, setForm] = useState<ForecastRequest>({
    metric: "Revenue",
    historical_data: [
      { period: "2023-01", value: 100 },
      { period: "2023-04", value: 120 },
      { period: "2023-07", value: 135 },
      { period: "2023-10", value: 160 },
      { period: "2024-01", value: 190 },
      { period: "2024-04", value: 230 },
    ],
    forecast_periods: 4,
  });

  const [state, setState] = useState<LoadingState>("idle");
  const [result, setResult] = useState<ForecastResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setState("loading");
    setError(null);
    setResult(null);

    try {
      const data = await generateForecast(form);
      setResult(data);
      setState("success");
    } catch (err: any) {
      setError(
        err?.response?.data?.detail || "Forecasting failed. Please try again."
      );
      setState("error");
    }
  };

  const updateDataPoint = (index: number, field: keyof DataPoint, value: string) => {
    const newData = [...form.historical_data];
    if (field === "value") {
      newData[index][field] = Number(value) || 0;
    } else {
      newData[index][field] = value;
    }
    setForm({ ...form, historical_data: newData });
  };

  const addDataPoint = () => {
    setForm({
      ...form,
      historical_data: [...form.historical_data, { period: "", value: 0 }],
    });
  };

  const removeDataPoint = (index: number) => {
    if (form.historical_data.length <= 3) return; // need minimum data points
    const newData = form.historical_data.filter((_, i) => i !== index);
    setForm({ ...form, historical_data: newData });
  };

  return (
    <div className="max-w-6xl mx-auto animate-fade-in">
      <div className="mb-8">
        <div className="flex items-center gap-3 mb-3">
          <div className="w-12 h-12 rounded-2xl bg-gradient-to-br from-indigo-500 to-purple-600 flex items-center justify-center shadow-lg shadow-indigo-500/20">
            <LineChart className="w-6 h-6 text-white" />
          </div>
          <h1 className="text-3xl font-bold text-white tracking-tight">
            Financial Forecasting Agent
          </h1>
        </div>
        <p className="text-slate-400 max-w-2xl text-lg">
          Provide historical business metrics and our AI will automatically select the best predictive model (Linear, Exponential, ARIMA) to forecast future growth.
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        
        {/* Left Column: Input Form */}
        <div className="lg:col-span-1 border border-white/5 bg-white/5 rounded-3xl p-6 shadow-xl h-fit">
          <form onSubmit={handleSubmit} className="space-y-6">
            <div>
              <label className="block text-sm font-medium text-slate-300 mb-2">
                Metric Name
              </label>
              <div className="relative">
                 <Layers className="absolute left-4 top-1/2 -translate-y-1/2 w-4 h-4 text-indigo-400" />
                 <input
                  type="text"
                  value={form.metric}
                  onChange={(e) => setForm({ ...form, metric: e.target.value })}
                  className="w-full bg-surface border border-white/10 rounded-xl pl-11 pr-4 py-3 text-white placeholder-slate-500 focus:outline-none focus:border-indigo-500/50 transition-all font-medium"
                  required
                 />
              </div>
            </div>

            <div>
              <div className="flex justify-between items-center mb-2">
                 <label className="block text-sm font-medium text-slate-300">
                  Historical Data Points
                 </label>
                 <button type="button" onClick={addDataPoint} className="text-xs text-indigo-400 hover:text-indigo-300 font-bold transition-colors">
                    + Add Point
                 </button>
              </div>
              
              <div className="space-y-3 max-h-[300px] overflow-y-auto pr-2 custom-scrollbar">
                {form.historical_data.map((point, i) => (
                  <div key={i} className="flex items-center gap-2">
                    <input
                      type="text"
                      placeholder="YYYY-MM"
                      value={point.period}
                      onChange={(e) => updateDataPoint(i, "period", e.target.value)}
                      className="w-1/2 bg-surface border border-white/10 rounded-lg px-3 py-2 text-sm text-white focus:outline-none focus:border-indigo-500"
                      required
                    />
                    <input
                      type="number"
                      placeholder="Value"
                      value={point.value}
                      onChange={(e) => updateDataPoint(i, "value", e.target.value)}
                      className="w-1/2 bg-surface border border-white/10 rounded-lg px-3 py-2 text-sm text-white focus:outline-none focus:border-indigo-500"
                      required
                    />
                    <button
                      type="button"
                      onClick={() => removeDataPoint(i)}
                      disabled={form.historical_data.length <= 3}
                      className="p-2 text-slate-500 hover:text-red-400 disabled:opacity-30 transition-colors"
                    >
                      &times;
                    </button>
                  </div>
                ))}
              </div>
              <p className="text-xs text-slate-500 mt-2 italic">* Minimum 3 data points required for regression.</p>
            </div>

            <div>
              <label className="block text-sm font-medium text-slate-300 mb-2">
                Periods to Forecast
              </label>
               <input
                type="number"
                min="1"
                max="12"
                value={form.forecast_periods}
                onChange={(e) => setForm({ ...form, forecast_periods: Number(e.target.value) })}
                className="w-full bg-surface border border-white/10 rounded-xl px-4 py-3 text-white focus:outline-none focus:border-indigo-500/50 transition-all font-medium"
                required
               />
            </div>

            <button
              type="submit"
              disabled={state === "loading" || form.historical_data.length < 3}
              className="w-full py-4 bg-gradient-to-r from-indigo-600 to-purple-600 text-white font-semibold rounded-xl hover:from-indigo-500 hover:to-purple-500 transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed shadow-glow-brand flex items-center justify-center gap-2"
            >
              {state === "loading" ? (
                <>
                  <Loader2 className="w-5 h-5 animate-spin" />
                  Running ML Models...
                </>
              ) : (
                <>
                  <Activity className="w-5 h-5" />
                  Generate Forecast
                </>
              )}
            </button>
          </form>
        </div>

        {/* Right Column: Results Dashboard */}
        <div className="lg:col-span-2 relative">
          <div className="sticky top-6 flex justify-end mb-6">
            <div className="w-full max-w-md">
              <div className="glass rounded-2xl p-6 border border-white/10 bg-white/5">
                <h2 className="text-xl font-semibold text-white mb-3">Quick Start</h2>
                <ol className="list-decimal list-inside text-slate-300 space-y-2 text-sm">
                  <li>Enter a metric name (e.g., Revenue, MRR, Users).</li>
                  <li>Provide at least 3 historical data points (YYYY-MM and value).</li>
                  <li>Set how many future periods you want to forecast.</li>
                  <li>Click <span className="font-semibold text-white">Generate Forecast</span> to run the model.</li>
                </ol>
                <p className="text-xs text-slate-500 mt-3">Tip: Use consistent intervals (monthly/quarterly) for best results.</p>
              </div>
            </div>
          </div>

          {state === "idle" && (
            <div className="h-full flex flex-col items-center justify-center p-12 text-center border-2 border-dashed border-white/10 rounded-3xl bg-white/5">
              <LineChart className="w-16 h-16 text-slate-600 mb-4" />
              <h3 className="text-xl font-bold text-slate-400 mb-2">Awaiting Data</h3>
              <p className="text-slate-500 max-w-sm">Enter your historical metrics on the left and our agent will run statistical regression to predict future performance.</p>
            </div>
          )}

           {state === "error" && (
            <div className="glass rounded-2xl p-6 border border-red-500/30 bg-red-500/10 animate-slide-up">
              <div className="flex items-center gap-3 text-red-400">
                <AlertOctagon className="w-6 h-6" />
                <p className="text-lg font-medium">{error}</p>
              </div>
            </div>
           )}

           {result && state === "success" && (
             <div className="space-y-6 animate-slide-up">
                
                {/* Metics Row */}
                <div className="grid grid-cols-3 gap-4">
                   <div className="glass rounded-2xl p-5 border border-white/5 bg-indigo-500/5 hover:bg-indigo-500/10 transition-colors">
                      <p className="text-slate-400 text-sm font-medium mb-1">Model Selected</p>
                      <p className="text-xl font-bold text-white capitalize">{result.model_used.replace('_', ' ')}</p>
                   </div>
                   <div className="glass rounded-2xl p-5 border border-white/5 bg-purple-500/5 hover:bg-purple-500/10 transition-colors">
                      <p className="text-slate-400 text-sm font-medium mb-1">Confidence Score (R²)</p>
                      <div className="flex items-end gap-2">
                        <p className="text-xl font-bold text-white">{result.r_squared.toFixed(3)}</p>
                        <span className={`text-xs p-1 rounded font-bold mb-1 ${result.r_squared > 0.8 ? 'bg-emerald-500/20 text-emerald-400' : 'bg-orange-500/20 text-orange-400'}`}>
                           {result.confidence}
                        </span>
                      </div>
                   </div>
                   <div className="glass rounded-2xl p-5 border border-white/5 bg-blue-500/5 hover:bg-blue-500/10 transition-colors">
                      <p className="text-slate-400 text-sm font-medium mb-1">Avg Growth Rate</p>
                      <p className={`text-xl font-bold ${result.avg_growth_rate > 0 ? 'text-emerald-400' : 'text-red-400'}`}>
                         {(result.avg_growth_rate * 100).toFixed(1)}% / period
                      </p>
                   </div>
                </div>

                {/* AI Executive Summary Narrative */}
                <div className="glass rounded-3xl p-8 border border-white/5 shadow-xl relative overflow-hidden">
                   <div className="absolute top-0 right-0 w-32 h-32 bg-purple-500/10 rounded-full blur-3xl"></div>
                   <h3 className="text-xl font-bold text-white mb-4 flex items-center gap-2">
                      <Target className="w-5 h-5 text-purple-400" /> Agent Synthesis
                   </h3>
                   <p className="text-slate-300 leading-relaxed text-lg whitespace-pre-line relative z-10">
                      {result.interpretation}
                   </p>
                </div>

                {/* Forecasted Data points */}
                <div className="glass rounded-3xl p-6 border border-white/5 shadow-xl">
                   <h3 className="text-lg font-bold text-white mb-4 flex items-center gap-2">
                      <Calendar className="w-5 h-5 text-indigo-400" /> Projected Timeline
                   </h3>
                   <div className="space-y-3">
                      {result.data_points.map((point, idx) => (
                         <div key={idx} className={`flex justify-between items-center p-4 rounded-xl border ${point.is_forecast ? 'border-indigo-500/20 bg-indigo-500/5' : 'border-white/5 bg-white/5'}`}>
                            <div className="flex items-center gap-2">
                              <span className="font-mono text-indigo-300 font-bold">{point.period}</span>
                              {point.is_forecast && <span className="text-[10px] bg-indigo-500 text-white px-1.5 py-0.5 rounded font-bold uppercase">Forecast</span>}
                            </div>
                            <span className="text-white font-bold text-lg">{point.value.toLocaleString(undefined, { maximumFractionDigits: 1 })}</span>
                         </div>
                      ))}
                   </div>
                </div>

             </div>
           )}
        </div>

      </div>
    </div>
  );
}
