"use client";

import { useState } from "react";
import { getMarketIntelligence } from "@/services/api";
import type { MarketIntelligenceResponse, LoadingState } from "@/types";
import {
  LineChart,
  Search,
  Globe,
  TrendingUp,
  Target,
  AlertOctagon,
  Swords,
  Loader2,
  DollarSign,
  Activity
} from "lucide-react";

export default function MarketIntelligencePage() {
  const [form, setForm] = useState({
    industry: "",
    target_market: "Global",
  });
  const [state, setState] = useState<LoadingState>("idle");
  const [result, setResult] = useState<MarketIntelligenceResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!form.industry.trim()) return;

    setState("loading");
    setError(null);
    setResult(null);

    try {
      const data = await getMarketIntelligence(form);
      setResult(data);
      setState("success");
    } catch (err: any) {
      setError(
        err?.response?.data?.detail || "Analysis failed. Please try again."
      );
      setState("error");
    }
  };

  return (
    <div className="max-w-6xl mx-auto animate-fade-in">
      <div className="mb-8">
        <div className="flex items-center gap-3 mb-3">
          <div className="w-12 h-12 rounded-2xl bg-gradient-to-br from-blue-500 to-indigo-600 flex items-center justify-center shadow-lg shadow-blue-500/20">
            <LineChart className="w-6 h-6 text-white" />
          </div>
          <h1 className="text-3xl font-bold text-white tracking-tight">
            Market Intelligence
          </h1>
        </div>
        <p className="text-slate-400 max-w-2xl text-lg">
          Generate comprehensive market landscapes, competitive analysis, and strategic insights instantly using AI.
        </p>
      </div>

      {/* Input Form */}
      <div className="glass rounded-3xl p-8 mb-10 border border-white/5 shadow-2xl">
        <form onSubmit={handleSubmit} className="flex flex-col md:flex-row gap-5 items-end">
          <div className="flex-1 w-full relative group">
            <label className="block text-sm font-medium text-slate-300 mb-2 ml-1">
              Industry or Sector <span className="text-blue-400">*</span>
            </label>
            <div className="relative">
              <Search className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-slate-400 group-focus-within:text-blue-400 transition-colors" />
              <input
                type="text"
                value={form.industry}
                onChange={(e) => setForm({ ...form, industry: e.target.value })}
                placeholder="e.g. Electric Vehicles, B2B SaaS, HealthTech"
                className="w-full bg-white/5 border border-white/10 rounded-2xl pl-12 pr-4 py-4 text-white placeholder-slate-500 focus:outline-none focus:border-blue-500/50 focus:bg-white/10 transition-all text-lg"
                required
              />
            </div>
          </div>

          <div className="flex-1 w-full relative group">
            <label className="block text-sm font-medium text-slate-300 mb-2 ml-1">
              Target Market
            </label>
            <div className="relative">
              <Globe className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-slate-400 group-focus-within:text-blue-400 transition-colors" />
              <input
                type="text"
                value={form.target_market}
                onChange={(e) =>
                  setForm({ ...form, target_market: e.target.value })
                }
                placeholder="e.g. North America, Global, UK"
                className="w-full bg-white/5 border border-white/10 rounded-2xl pl-12 pr-4 py-4 text-white placeholder-slate-500 focus:outline-none focus:border-blue-500/50 focus:bg-white/10 transition-all text-lg"
              />
            </div>
          </div>

          <button
            type="submit"
            disabled={state === "loading" || !form.industry.trim()}
            className="w-full md:w-auto px-8 py-4 bg-gradient-to-r from-blue-600 to-indigo-600 text-white font-semibold rounded-2xl hover:from-blue-500 hover:to-indigo-500 transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed shadow-xl shadow-blue-500/25 flex items-center justify-center gap-2 whitespace-nowrap text-lg"
          >
            {state === "loading" ? (
              <>
                <Loader2 className="w-5 h-5 animate-spin" />
                Analyzing Market...
              </>
            ) : (
              <>
                Generate Report
              </>
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
          
          {/* Header Stats */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            <div className="glass rounded-3xl p-6 border border-white/5 relative overflow-hidden group">
              <div className="absolute top-0 right-0 w-32 h-32 bg-indigo-500/10 rounded-full blur-3xl group-hover:bg-indigo-500/20 transition-all"></div>
              <div className="flex items-center gap-4 mb-4">
                <div className="w-12 h-12 rounded-xl bg-indigo-500/20 flex items-center justify-center border border-indigo-500/30">
                  <Target className="w-6 h-6 text-indigo-400" />
                </div>
                <div>
                  <h3 className="text-slate-400 font-medium">Industry Focus</h3>
                  <p className="text-xl font-bold text-white capitalize">{result.industry}</p>
                </div>
              </div>
            </div>

            <div className="glass rounded-3xl p-6 border border-white/5 relative overflow-hidden group">
              <div className="absolute top-0 right-0 w-32 h-32 bg-emerald-500/10 rounded-full blur-3xl group-hover:bg-emerald-500/20 transition-all"></div>
              <div className="flex items-center gap-4 mb-4">
                <div className="w-12 h-12 rounded-xl bg-emerald-500/20 flex items-center justify-center border border-emerald-500/30">
                  <DollarSign className="w-6 h-6 text-emerald-400" />
                </div>
                <div>
                  <h3 className="text-slate-400 font-medium">Est. Market Size</h3>
                  <p className="text-xl font-bold text-white">{result.market_size_estimate}</p>
                </div>
              </div>
            </div>

            <div className="glass rounded-3xl p-6 border border-white/5 relative overflow-hidden group">
              <div className="absolute top-0 right-0 w-32 h-32 bg-blue-500/10 rounded-full blur-3xl group-hover:bg-blue-500/20 transition-all"></div>
              <div className="flex items-center gap-4 mb-4">
                <div className="w-12 h-12 rounded-xl bg-blue-500/20 flex items-center justify-center border border-blue-500/30">
                  <Activity className="w-6 h-6 text-blue-400" />
                </div>
                <div>
                  <h3 className="text-slate-400 font-medium">Projected CAGR</h3>
                  <p className="text-xl font-bold text-white">{result.cagr_estimate}</p>
                </div>
              </div>
            </div>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
            {/* Left Column: Overview & Trends */}
            <div className="lg:col-span-2 space-y-8">
              <div className="glass rounded-3xl p-8 border border-white/5 shadow-xl">
                <h2 className="text-2xl font-bold text-white mb-6 flex items-center gap-3">
                  <Globe className="w-6 h-6 text-blue-400" />
                  Market Overview
                </h2>
                <p className="text-slate-300 leading-relaxed text-lg">
                  {result.market_overview}
                </p>
              </div>

              <div className="glass rounded-3xl p-8 border border-white/5 shadow-xl">
                <h2 className="text-2xl font-bold text-white mb-6 flex items-center gap-3">
                  <TrendingUp className="w-6 h-6 text-blue-400" />
                  Key Market Trends
                </h2>
                <div className="grid gap-4">
                  {result.key_trends.map((trend, i) => (
                    <div key={i} className="flex items-start gap-4 p-4 rounded-2xl bg-white/5 border border-white/5 hover:bg-white/10 transition-colors">
                      <div className="w-8 h-8 rounded-full bg-blue-500/20 flex items-center justify-center flex-shrink-0 mt-0.5 border border-blue-500/30">
                        <span className="text-blue-400 font-bold">{i + 1}</span>
                      </div>
                      <p className="text-slate-300 leading-relaxed">{trend}</p>
                    </div>
                  ))}
                </div>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                <div className="glass rounded-3xl p-8 border border-emerald-500/20 shadow-xl relative overflow-hidden">
                  <div className="absolute -top-10 -right-10 w-40 h-40 bg-emerald-500/10 rounded-full blur-3xl"></div>
                  <h3 className="text-xl font-bold text-emerald-400 mb-6 flex items-center gap-2">
                    <Target className="w-5 h-5" /> Opportunities
                  </h3>
                  <ul className="space-y-4 relative z-10">
                    {result.opportunities.map((opp, i) => (
                      <li key={i} className="flex items-start gap-3 text-slate-300">
                        <div className="w-1.5 h-1.5 rounded-full bg-emerald-500 mt-2.5 flex-shrink-0"></div>
                        <span>{opp}</span>
                      </li>
                    ))}
                  </ul>
                </div>

                <div className="glass rounded-3xl p-8 border border-red-500/20 shadow-xl relative overflow-hidden">
                  <div className="absolute -top-10 -right-10 w-40 h-40 bg-red-500/10 rounded-full blur-3xl"></div>
                   <h3 className="text-xl font-bold text-red-400 mb-6 flex items-center gap-2">
                    <AlertOctagon className="w-5 h-5" /> Risks & Threats
                  </h3>
                  <ul className="space-y-4 relative z-10">
                    {result.risks.map((risk, i) => (
                      <li key={i} className="flex items-start gap-3 text-slate-300">
                        <div className="w-1.5 h-1.5 rounded-full bg-red-500 mt-2.5 flex-shrink-0"></div>
                        <span>{risk}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              </div>
            </div>

            {/* Right Column: Competitor Landscape */}
            <div className="space-y-6">
              <div className="flex items-center justify-between mb-2">
                <h2 className="text-2xl font-bold text-white flex items-center gap-3">
                  <Swords className="w-6 h-6 text-purple-400" />
                  Competitor Landscape
                </h2>
              </div>
              
              <div className="grid gap-6">
                {result.top_competitors.map((comp, i) => (
                  <div key={i} className="glass rounded-3xl p-6 border border-white/5 hover:border-purple-500/30 transition-all shadow-xl group">
                    <div className="flex justify-between items-start mb-4">
                      <h3 className="text-xl font-bold text-white group-hover:text-purple-400 transition-colors">{comp.name}</h3>
                      {comp.market_share_estimate && (
                         <span className="px-3 py-1 rounded-full bg-purple-500/20 text-purple-300 text-xs font-bold border border-purple-500/30 whitespace-nowrap">
                           Share: {comp.market_share_estimate}
                         </span>
                      )}
                    </div>
                    <p className="text-slate-400 text-sm mb-5 leading-relaxed">
                      {comp.description}
                    </p>
                    
                    <div className="space-y-4">
                      <div>
                        <h4 className="text-xs font-bold text-emerald-400 uppercase tracking-wider mb-2">Strengths</h4>
                        <div className="flex flex-wrap gap-2">
                          {comp.strengths.slice(0, 3).map((s, j) => (
                            <span key={j} className="text-xs px-2.5 py-1 rounded-md bg-emerald-500/10 text-emerald-300 border border-emerald-500/20">
                              {s}
                            </span>
                          ))}
                        </div>
                      </div>
                      <div>
                        <h4 className="text-xs font-bold text-red-400 uppercase tracking-wider mb-2">Weaknesses</h4>
                        <div className="flex flex-wrap gap-2">
                          {comp.weaknesses.slice(0, 3).map((w, j) => (
                            <span key={j} className="text-xs px-2.5 py-1 rounded-md bg-red-500/10 text-red-300 border border-red-500/20">
                              {w}
                            </span>
                          ))}
                        </div>
                      </div>
                    </div>
                  </div>
                ))}
              </div>

              {result.top_competitors.length === 0 && (
                <div className="p-8 text-center text-slate-500 glass rounded-3xl border border-white/5">
                  No significant competitors identified.
                </div>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
