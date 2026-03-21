"use client";

import { useState } from "react";
import { analyzeFinancialReport } from "@/services/api";
import type { FinancialReportResponse, LoadingState } from "@/types";
import {
  FileText,
  Upload,
  Loader2,
  DollarSign,
  TrendingUp,
  AlertOctagon,
  Percent,
  BarChart,
  CheckCircle2,
  BookOpen,
  AlertTriangle,
  Lightbulb
} from "lucide-react";

export default function FinancialReportsPage() {
  const [file, setFile] = useState<File | null>(null);
  const [state, setState] = useState<LoadingState>("idle");
  const [result, setResult] = useState<FinancialReportResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setFile(e.target.files[0]);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!file) return;

    setState("loading");
    setError(null);
    setResult(null);

    try {
      const data = await analyzeFinancialReport(file);
      setResult(data);
      setState("success");
    } catch (err: any) {
      setError(
        err?.response?.data?.detail || "Report analysis failed. Please try again."
      );
      setState("error");
    }
  };

  const formatCurrency = (val: any) => {
    if (!val || val === "Not disclosed") return "Not disclosed";
    const num = Number(val);
    if (isNaN(num)) return val;
    return `$${num.toLocaleString()}`;
  };

  const formatPercent = (val: any) => {
    if (!val || val === "Not disclosed") return "Not disclosed";
    const num = Number(val);
    if (isNaN(num)) return val;
    return `${(num * 100).toFixed(1)}%`;
  };

  const formatNumber = (val: any) => {
    if (!val || val === "Not disclosed") return "Not disclosed";
    const num = Number(val);
    if (isNaN(num)) return val;
    return num.toLocaleString();
  };

  return (
    <div className="max-w-6xl mx-auto animate-fade-in">
      <div className="mb-8">
        <div className="flex items-center gap-3 mb-3">
          <div className="w-12 h-12 rounded-2xl bg-gradient-to-br from-emerald-500 to-teal-600 flex items-center justify-center shadow-lg shadow-emerald-500/20">
            <FileText className="w-6 h-6 text-white" />
          </div>
          <h1 className="text-3xl font-bold text-white tracking-tight">
            Financial Report Analyzer
          </h1>
        </div>
        <p className="text-slate-400 max-w-2xl text-lg">
          Upload PDF financial statements (10-K, 10-Q, Income Statements) and instantly extract key metrics using AI.
        </p>
      </div>

      {/* Upload Form */}
      <div className="glass rounded-3xl p-8 mb-10 border border-white/5 shadow-2xl">
        <form onSubmit={handleSubmit} className="flex flex-col md:flex-row gap-5 items-end">
          <div className="flex-1 w-full relative">
            <label className="block text-sm font-medium text-slate-300 mb-2 ml-1">
              Financial Report (PDF) <span className="text-emerald-400">*</span>
            </label>
            <div className="relative flex items-center justify-center w-full">
              <label htmlFor="dropzone-file" className="flex flex-col items-center justify-center w-full h-32 border-2 border-dashed border-white/10 rounded-2xl cursor-pointer bg-white/5 hover:bg-white/10 hover:border-emerald-500/50 transition-all">
                  <div className="flex flex-col items-center justify-center pt-5 pb-6">
                      <Upload className="w-8 h-8 mb-3 text-slate-400" />
                      <p className="mb-2 text-sm text-slate-400">
                        {file ? <span className="font-semibold text-emerald-400">{file.name}</span> : <span><span className="font-semibold">Click to upload</span> or drag and drop</span>}
                      </p>
                      <p className="text-xs text-slate-500">PDF, MAX 20MB</p>
                  </div>
                  <input id="dropzone-file" type="file" className="hidden" accept=".pdf" onChange={handleFileChange} />
              </label>
            </div>
          </div>

          <button
            type="submit"
            disabled={state === "loading" || !file}
            className="w-full md:w-auto h-32 px-8 bg-gradient-to-r from-emerald-600 to-teal-600 text-white font-semibold rounded-2xl hover:from-emerald-500 hover:to-teal-500 transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed shadow-xl shadow-emerald-500/25 flex items-center justify-center gap-2 whitespace-nowrap text-lg"
          >
            {state === "loading" ? (
              <div className="flex flex-col items-center gap-2">
                <Loader2 className="w-6 h-6 animate-spin" />
                <span>Extracting Metrics...</span>
              </div>
            ) : (
              <div className="flex flex-col items-center gap-2">
                <BarChart className="w-6 h-6" />
                <span>Analyze Report</span>
              </div>
            )}
          </button>
        </form>
      </div>

      {/* Error State */}
      {state === "error" && (
        <div className="glass rounded-2xl p-6 border border-red-500/30 bg-red-500/10 mb-8 animate-slide-up">
          <div className="flex items-center gap-3 text-red-400">
            <AlertOctagon className="w-6 h-6" />
            <p className="text-lg font-medium">{error}</p>
          </div>
        </div>
      )}

      {/* Results Dashboard */}
      {result && state === "success" && (
        <div className="space-y-8 animate-slide-up pb-20">
          
          <div className="glass rounded-3xl p-6 flex items-center gap-4 border border-emerald-500/20 bg-emerald-500/5">
             <CheckCircle2 className="w-6 h-6 text-emerald-500 flex-shrink-0" />
             <div>
                <h3 className="text-white font-semibold text-lg">Analysis Complete</h3>
                <p className="text-slate-400 text-sm">Report ID: <span className="font-mono text-emerald-400/80">{result.filename}</span></p>
             </div>
          </div>

          <h2 className="text-2xl font-bold text-white mb-6 flex items-center gap-3">
            <DollarSign className="w-6 h-6 text-emerald-400" />
            Core Financial Metrics
          </h2>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-6">
            
            <div className="glass rounded-3xl p-6 border border-white/5 relative overflow-hidden group">
              <div className="absolute top-0 right-0 w-32 h-32 bg-emerald-500/10 rounded-full blur-3xl group-hover:bg-emerald-500/20 transition-all"></div>
              <p className="text-slate-400 font-medium mb-2">Revenue</p>
              <p className="text-xl font-bold text-white">{formatCurrency(result.metrics.revenue)}</p>
            </div>

            <div className="glass rounded-3xl p-6 border border-white/5 relative overflow-hidden group">
              <div className="absolute top-0 right-0 w-32 h-32 bg-blue-500/10 rounded-full blur-3xl group-hover:bg-blue-500/20 transition-all"></div>
              <p className="text-slate-400 font-medium mb-2">Net Profit</p>
              <p className="text-xl font-bold text-white">{formatCurrency(result.metrics.net_profit)}</p>
            </div>

            <div className="glass rounded-3xl p-6 border border-white/5 relative overflow-hidden group">
              <div className="absolute top-0 right-0 w-32 h-32 bg-purple-500/10 rounded-full blur-3xl group-hover:bg-purple-500/20 transition-all"></div>
              <p className="text-slate-400 font-medium mb-2">Total Assets</p>
              <p className="text-xl font-bold text-white">{formatCurrency(result.metrics.total_assets)}</p>
            </div>

            <div className="glass rounded-3xl p-6 border border-white/5 relative overflow-hidden group">
              <div className="absolute top-0 right-0 w-32 h-32 bg-orange-500/10 rounded-full blur-3xl group-hover:bg-orange-500/20 transition-all"></div>
              <p className="text-slate-400 font-medium mb-2">Total Liabilities</p>
              <p className="text-xl font-bold text-white">{formatCurrency(result.metrics.total_liabilities)}</p>
            </div>

            <div className="glass rounded-3xl p-6 border border-white/5 relative overflow-hidden group">
              <div className="absolute top-0 right-0 w-32 h-32 bg-cyan-500/10 rounded-full blur-3xl group-hover:bg-cyan-500/20 transition-all"></div>
              <p className="text-slate-400 font-medium mb-2">Cash Flow</p>
              <p className="text-xl font-bold text-white">{formatCurrency(result.metrics.cash_flow)}</p>
            </div>

          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-8 mt-8">
            <div className="glass rounded-3xl p-8 border border-white/5 shadow-xl">
               <h3 className="text-xl font-bold text-white mb-6 flex items-center gap-2">
                <Percent className="w-5 h-5 text-emerald-400" /> Margin Analysis
              </h3>
              <div className="space-y-4">
                 <div className="flex justify-between items-center p-4 bg-white/5 rounded-xl">
                    <span className="text-slate-300">Gross Margin</span>
                    <span className="text-white font-bold">{formatPercent(result.metrics.gross_margin)}</span>
                 </div>
                 <div className="flex justify-between items-center p-4 bg-white/5 rounded-xl">
                    <span className="text-slate-300">EBITDA Margin</span>
                    <span className="text-white font-bold">{formatPercent(result.metrics.ebitda_margin)}</span>
                 </div>
                 <div className="flex justify-between items-center p-4 bg-white/5 rounded-xl">
                    <span className="text-slate-300">Net Profit Margin</span>
                    <span className="text-white font-bold">{formatPercent(result.metrics.net_margin)}</span>
                 </div>
                 <div className="flex justify-between items-center p-4 bg-white/5 rounded-xl">
                    <span className="text-slate-300">Operating Income</span>
                    <span className="text-white font-bold">{formatCurrency(result.metrics.operating_income)}</span>
                 </div>
              </div>
            </div>

            <div className="glass rounded-3xl p-8 border border-white/5 shadow-xl">
               <h3 className="text-xl font-bold text-white mb-6 flex items-center gap-2">
                <TrendingUp className="w-5 h-5 text-blue-400" /> Key Indicators
              </h3>
               <div className="space-y-4">
                 <div className="flex justify-between items-center p-4 bg-white/5 rounded-xl border border-blue-500/10">
                    <span className="text-slate-300">Revenue Growth (YoY)</span>
                    <span className={`font-bold ${Number(result.metrics.revenue_growth_yoy || 0) > 0 ? 'text-emerald-400' : 'text-slate-300'}`}>
                      {formatPercent(result.metrics.revenue_growth_yoy)}
                    </span>
                 </div>
                 <div className="flex justify-between items-center p-4 bg-white/5 rounded-xl border border-blue-500/10">
                    <span className="text-slate-300">Current Ratio</span>
                    <span className="font-bold text-white">
                      {formatNumber(result.metrics.current_ratio)}
                    </span>
                 </div>
                 <div className="p-4 bg-white/5 rounded-xl mt-4 border border-purple-500/20">
                    <span className="text-slate-300 block mb-1 text-sm">Debt to Equity Ratio</span>
                    <span className="text-white font-bold text-xl">{formatNumber(result.metrics.debt_to_equity)}</span>
                 </div>
              </div>
            </div>
          </div>

          {/* Narrative Analysis Section */}
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 mt-8">
            <div className="lg:col-span-2 glass rounded-3xl p-8 border border-white/5 shadow-xl">
              <h3 className="text-xl font-bold text-white mb-6 flex items-center gap-2">
                <BookOpen className="w-5 h-5 text-emerald-400" /> Executive Analysis
              </h3>
              <p className="text-slate-300 leading-relaxed whitespace-pre-wrap">
                {result.analysis}
              </p>
            </div>

            <div className="space-y-8">
              <div className="glass rounded-3xl p-8 border border-white/5 shadow-xl">
                <h3 className="text-xl font-bold text-white mb-6 flex items-center gap-2">
                  <Lightbulb className="w-5 h-5 text-yellow-400" /> Key Highlights
                </h3>
                {result.key_highlights && result.key_highlights.length > 0 ? (
                  <ul className="space-y-3">
                    {result.key_highlights.map((highlight, i) => (
                      <li key={i} className="flex gap-3 text-slate-300">
                        <span className="text-yellow-400 mt-1">•</span>
                        <span>{highlight}</span>
                      </li>
                    ))}
                  </ul>
                ) : (
                  <p className="text-slate-500 italic">No highlights extracted.</p>
                )}
              </div>

              <div className="glass rounded-3xl p-8 border border-white/5 shadow-xl">
                <h3 className="text-xl font-bold text-white mb-6 flex items-center gap-2">
                  <AlertTriangle className="w-5 h-5 text-red-400" /> Key Risks
                </h3>
                {result.key_risks && result.key_risks.length > 0 ? (
                  <ul className="space-y-3">
                    {result.key_risks.map((risk, i) => (
                      <li key={i} className="flex gap-3 text-slate-300">
                        <span className="text-red-400 mt-1">•</span>
                        <span>{risk}</span>
                      </li>
                    ))}
                  </ul>
                ) : (
                  <p className="text-slate-500 italic">No key risks identified.</p>
                )}
              </div>
            </div>
          </div>

        </div>
      )}
    </div>
  );
}
