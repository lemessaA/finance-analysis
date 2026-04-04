"use client";

import { useState } from "react";
import { analyzeFinancialReport } from "@/services/api";
import AdvancedFinancialAnalysis from "@/components/AdvancedFinancialAnalysis";
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
  Lightbulb,
  Brain,
  Zap,
  Shield
} from "lucide-react";

export default function FinancialReportsPage() {
  const [analysisMode, setAnalysisMode] = useState<string>("basic");
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
      const data = await analyzeFinancialReport(file) as any;
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

  if (analysisMode === "advanced") {
    return <AdvancedFinancialAnalysis />;
  }

  return (
    <div className="max-w-6xl mx-auto animate-fade-in">
      <div className="mb-8">
        <div className="flex items-center justify-between mb-3">
          <div className="flex items-center gap-3">
            <div className="w-12 h-12 rounded-2xl bg-gradient-to-br from-emerald-500 to-teal-600 flex items-center justify-center shadow-lg shadow-emerald-500/20">
              <FileText className="w-6 h-6 text-white" />
            </div>
            <h1 className="text-3xl font-bold text-white tracking-tight">
              Financial Report Analyzer
            </h1>
          </div>
          
          {/* Mode Toggle */}
          <div className="flex items-center gap-2 bg-white/10 rounded-xl p-1">
            <button
              onClick={() => setAnalysisMode("basic")}
              className={`px-4 py-2 rounded-lg transition-all ${
                analysisMode === "basic"
                  ? "bg-emerald-600 text-white"
                  : "text-gray-300 hover:text-white"
              }`}
            >
              Basic Analysis
            </button>
            <button
              onClick={() => setAnalysisMode("advanced")}
              className={`px-4 py-2 rounded-lg transition-all flex items-center gap-2 ${
                analysisMode === "advanced"
                  ? "bg-purple-600 text-white"
                  : "text-gray-300 hover:text-white"
              }`}
            >
              <Brain className="w-4 h-4" />
              Advanced AI
            </button>
          </div>
        </div>
        <p className="text-slate-400 max-w-2xl text-lg">
          Upload PDF financial statements (10-K, 10-Q, Income Statements) and instantly extract key metrics using AI.
        </p>
      </div>

      {/* Feature Comparison */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        <div className="glass rounded-2xl p-6 border border-emerald-500/20 bg-emerald-500/5">
          <div className="flex items-center gap-3 mb-3">
            <BarChart className="w-6 h-6 text-emerald-500" />
            <h3 className="text-lg font-semibold text-white">Basic Analysis</h3>
          </div>
          <ul className="space-y-2 text-sm text-gray-300">
            <li className="flex items-start gap-2">
              <CheckCircle2 className="w-4 h-4 text-emerald-500 mt-0.5 flex-shrink-0" />
              <span>Key financial metrics extraction</span>
            </li>
            <li className="flex items-start gap-2">
              <CheckCircle2 className="w-4 h-4 text-emerald-500 mt-0.5 flex-shrink-0" />
              <span>Basic financial ratios</span>
            </li>
            <li className="flex items-start gap-2">
              <CheckCircle2 className="w-4 h-4 text-emerald-500 mt-0.5 flex-shrink-0" />
              <span>Quick insights and highlights</span>
            </li>
          </ul>
        </div>
        
        <div className="glass rounded-2xl p-6 border border-purple-500/20 bg-purple-500/5">
          <div className="flex items-center gap-3 mb-3">
            <Brain className="w-6 h-6 text-purple-500" />
            <h3 className="text-lg font-semibold text-white">Advanced AI Analysis</h3>
          </div>
          <ul className="space-y-2 text-sm text-gray-300">
            <li className="flex items-start gap-2">
              <Zap className="w-4 h-4 text-purple-500 mt-0.5 flex-shrink-0" />
              <span>Comprehensive financial health scoring</span>
            </li>
            <li className="flex items-start gap-2">
              <Zap className="w-4 h-4 text-purple-500 mt-0.5 flex-shrink-0" />
              <span>Advanced risk assessment</span>
            </li>
            <li className="flex items-start gap-2">
              <Zap className="w-4 h-4 text-purple-500 mt-0.5 flex-shrink-0" />
              <span>Industry benchmarking & predictions</span>
            </li>
            <li className="flex items-start gap-2">
              <Zap className="w-4 h-4 text-purple-500 mt-0.5 flex-shrink-0" />
              <span>AI-powered recommendations</span>
            </li>
          </ul>
        </div>
        
        <div className="glass rounded-2xl p-6 border border-blue-500/20 bg-blue-500/5">
          <div className="flex items-center gap-3 mb-3">
            <Shield className="w-6 h-6 text-blue-500" />
            <h3 className="text-lg font-semibold text-white">Enhanced Features</h3>
          </div>
          <ul className="space-y-2 text-sm text-gray-300">
            <li className="flex items-start gap-2">
              <Lightbulb className="w-4 h-4 text-blue-500 mt-0.5 flex-shrink-0" />
              <span>Trend analysis with historical data</span>
            </li>
            <li className="flex items-start gap-2">
              <Lightbulb className="w-4 h-4 text-blue-500 mt-0.5 flex-shrink-0" />
              <span>Predictive insights & forecasting</span>
            </li>
            <li className="flex items-start gap-2">
              <Lightbulb className="w-4 h-4 text-blue-500 mt-0.5 flex-shrink-0" />
              <span>Multi-report comparison</span>
            </li>
          </ul>
        </div>
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
                <h3 className="text-white font-semibold text-lg">Basic Analysis Complete</h3>
                <p className="text-slate-400 text-sm">Report ID: <span className="font-mono text-emerald-400/80">{result.filename}</span></p>
             </div>
             <div className="ml-auto">
                <button 
                  onClick={() => setAnalysisMode("advanced")}
                  className="px-4 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700 transition-all flex items-center gap-2"
                >
                  <Brain className="w-4 h-4" />
                  Upgrade to Advanced
                </button>
             </div>
          </div>

          {/* Key Metrics Grid */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            <div className="glass rounded-2xl p-6 border border-white/10">
              <div className="flex items-center gap-3 mb-4">
                <div className="p-2 bg-emerald-500/20 rounded-lg">
                  <DollarSign className="w-5 h-5 text-emerald-500" />
                </div>
                <div>
                  <p className="text-sm text-gray-400">Revenue</p>
                  <p className="text-xl font-bold text-white">{formatCurrency(result.metrics.revenue)}</p>
                </div>
              </div>
            </div>

            <div className="glass rounded-2xl p-6 border border-white/10">
              <div className="flex items-center gap-3 mb-4">
                <div className="p-2 bg-blue-500/20 rounded-lg">
                  <TrendingUp className="w-5 h-5 text-blue-500" />
                </div>
                <div>
                  <p className="text-sm text-gray-400">Net Profit</p>
                  <p className="text-xl font-bold text-white">{formatCurrency(result.metrics.net_profit)}</p>
                </div>
              </div>
            </div>

            <div className="glass rounded-2xl p-6 border border-white/10">
              <div className="flex items-center gap-3 mb-4">
                <div className="p-2 bg-purple-500/20 rounded-lg">
                  <Percent className="w-5 h-5 text-purple-500" />
                </div>
                <div>
                  <p className="text-sm text-gray-400">Net Margin</p>
                  <p className="text-xl font-bold text-white">{formatPercent(result.metrics.net_margin)}</p>
                </div>
              </div>
            </div>

            <div className="glass rounded-2xl p-6 border border-white/10">
              <div className="flex items-center gap-3 mb-4">
                <div className="p-2 bg-orange-500/20 rounded-lg">
                  <BarChart className="w-5 h-5 text-orange-500" />
                </div>
                <div>
                  <p className="text-sm text-gray-400">Total Assets</p>
                  <p className="text-xl font-bold text-white">{formatCurrency(result.metrics.total_assets)}</p>
                </div>
              </div>
            </div>
          </div>

          {/* All Metrics Table */}
          <div className="glass rounded-3xl p-8 border border-white/10">
            <h3 className="text-xl font-semibold text-white mb-6 flex items-center gap-3">
              <BookOpen className="w-6 h-6 text-blue-500" />
              Extracted Financial Metrics
            </h3>
            
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {Object.entries(result.metrics).map(([key, value]) => (
                <div key={key} className="bg-white/5 rounded-xl p-4 border border-white/10">
                  <div className="text-sm text-gray-400 mb-1 capitalize">
                    {key.replace(/_/g, ' ')}
                  </div>
                  <div className="text-lg font-bold text-white">
                    {key.includes('margin') || key.includes('growth') ? formatPercent(value) : 
                     key.includes('ratio') ? formatNumber(value) : formatCurrency(value)}
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Analysis Text */}
          {result.analysis && (
            <div className="glass rounded-3xl p-8 border border-white/10">
              <h3 className="text-xl font-semibold text-white mb-6 flex items-center gap-3">
                <Lightbulb className="w-6 h-6 text-yellow-500" />
                AI Analysis Summary
              </h3>
              <div className="prose prose-invert max-w-none">
                <p className="text-gray-300 leading-relaxed whitespace-pre-line">
                  {result.analysis}
                </p>
              </div>
            </div>
          )}

          {/* Key Highlights */}
          {result.key_highlights && result.key_highlights.length > 0 && (
            <div className="glass rounded-3xl p-8 border border-white/10">
              <h3 className="text-xl font-semibold text-white mb-6 flex items-center gap-3">
                <CheckCircle2 className="w-6 h-6 text-green-500" />
                Key Highlights
              </h3>
              <ul className="space-y-3">
                {result.key_highlights.map((highlight, index) => (
                  <li key={index} className="flex items-start gap-3">
                    <CheckCircle2 className="w-5 h-5 text-green-500 mt-0.5 flex-shrink-0" />
                    <span className="text-gray-300">{highlight}</span>
                  </li>
                ))}
              </ul>
            </div>
          )}

          {/* Key Risks */}
          {result.key_risks && result.key_risks.length > 0 && (
            <div className="glass rounded-3xl p-8 border border-white/10">
              <h3 className="text-xl font-semibold text-white mb-6 flex items-center gap-3">
                <AlertTriangle className="w-6 h-6 text-red-500" />
                Key Risks Identified
              </h3>
              <ul className="space-y-3">
                {result.key_risks.map((risk, index) => (
                  <li key={index} className="flex items-start gap-3">
                    <AlertTriangle className="w-5 h-5 text-red-500 mt-0.5 flex-shrink-0" />
                    <span className="text-gray-300">{risk}</span>
                  </li>
                ))}
              </ul>
            </div>
          )}

          {/* Upgrade CTA */}
          <div className="glass rounded-3xl p-8 border border-purple-500/20 bg-purple-500/5">
            <div className="flex items-center justify-between">
              <div>
                <h3 className="text-xl font-semibold text-white mb-2">Unlock Advanced AI Analysis</h3>
                <p className="text-gray-300 mb-4">
                  Get comprehensive financial health scoring, risk assessment, industry benchmarking, and AI-powered recommendations.
                </p>
                <button 
                  onClick={() => setAnalysisMode("advanced")}
                  className="px-6 py-3 bg-purple-600 text-white rounded-lg hover:bg-purple-700 transition-all flex items-center gap-2"
                >
                  <Brain className="w-5 h-5" />
                  Try Advanced Analysis
                </button>
              </div>
              <div className="hidden md:block">
                <Brain className="w-16 h-16 text-purple-500/50" />
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
