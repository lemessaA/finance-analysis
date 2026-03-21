"use client";

import { useState } from "react";
import { validateStartup } from "@/services/api";
import type { StartupValidationResponse, LoadingState } from "@/types";
import {
  Lightbulb, Send, CheckCircle2, XCircle, AlertTriangle,
  TrendingUp, Users, Shield, BarChart3, Loader2
} from "lucide-react";

const VERDICT_CONFIG = {
  "STRONG GO":      { color: "verdict-strong-go",  icon: CheckCircle2,   label: "STRONG GO" },
  "GO":             { color: "verdict-go",          icon: CheckCircle2,   label: "GO" },
  "CONDITIONAL GO": { color: "verdict-conditional", icon: AlertTriangle,  label: "CONDITIONAL GO" },
  "NO GO":          { color: "verdict-no-go",       icon: XCircle,        label: "NO GO" },
};

function ScoreBar({ label, score, color }: { label: string; score: number; color: string }) {
  return (
    <div>
      <div className="flex justify-between text-sm mb-1">
        <span className="text-slate-400">{label}</span>
        <span className="font-semibold text-white">{score.toFixed(0)}/100</span>
      </div>
      <div className="h-2 bg-surface rounded-full overflow-hidden">
        <div
          className={`h-full ${color} rounded-full transition-all duration-700`}
          style={{ width: `${score}%` }}
        />
      </div>
    </div>
  );
}

export default function StartupPage() {
  const [form, setForm] = useState({
    idea: "",
    industry: "",
    targetMarket: "Global",
    businessStage: "Early Stage",
    description: "",
  });
  const [state, setState] = useState<LoadingState>("idle");
  const [result, setResult] = useState<StartupValidationResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!form.idea.trim() || !form.industry.trim()) return;
    
    // Validate minimum length requirements
    if (form.idea.trim().length < 10) {
      setError("Startup idea must be at least 10 characters long.");
      setState("error");
      return;
    }
    
    if (form.industry.trim().length < 2) {
      setError("Industry must be at least 2 characters long.");
      setState("error");
      return;
    }

    setState("loading");
    setError(null);
    setResult(null);

    try {
      const data = await validateStartup(form);
      setResult(data);
      setState("success");
    } catch (err: any) {
      setError(err?.response?.data?.detail || "Validation failed. Please try again.");
      setState("error");
    }
  };

  const verdict = result?.verdict as keyof typeof VERDICT_CONFIG | undefined;
  const verdictCfg = verdict ? VERDICT_CONFIG[verdict] ?? VERDICT_CONFIG["NO GO"] : null;

  return (
    <div className="max-w-4xl animate-fade-in">
      <div className="mb-8">
        <div className="flex items-center gap-3 mb-3">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-brand-500 to-purple-600 flex items-center justify-center shadow-glow-brand">
            <Lightbulb className="w-5 h-5 text-white" />
          </div>
          <h1 className="text-2xl font-bold text-white">Startup Idea Validator</h1>
        </div>
        <p className="text-slate-400">
          Our multi-agent pipeline analyzes your idea across market research, competitor
          landscape, risk factors, and produces a VC-grade validation report.
        </p>
      </div>

      {/* Form */}
      <div className="glass rounded-2xl p-6 mb-8 border border-surface-border">
        <form onSubmit={handleSubmit} className="space-y-5">
          <div>
            <label className="block text-sm font-medium text-slate-300 mb-2">
              Startup Idea *
            </label>
            <textarea
              rows={3}
              value={form.idea}
              onChange={(e) => setForm({ ...form, idea: e.target.value })}
              placeholder="Describe your startup idea in detail (minimum 10 characters)..."
              className="w-full bg-surface border border-surface-border rounded-xl px-4 py-3 text-white placeholder-slate-500 focus:outline-none focus:border-brand-500 focus:ring-1 focus:ring-brand-500 resize-none transition"
              required
              minLength={10}
            />
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-slate-300 mb-2">Industry *</label>
              <input
                type="text"
                value={form.industry}
                onChange={(e) => setForm({ ...form, industry: e.target.value })}
                placeholder="e.g. HealthTech, FinTech, EdTech (min 2 characters)"
                className="w-full bg-surface border border-surface-border rounded-xl px-4 py-3 text-white placeholder-slate-500 focus:outline-none focus:border-brand-500 focus:ring-1 focus:ring-brand-500 transition"
                required
                minLength={2}
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-slate-300 mb-2">Target Market</label>
              <input
                type="text"
                value={form.targetMarket}
                onChange={(e) => setForm({ ...form, targetMarket: e.target.value })}
                placeholder="e.g. United States, Europe"
                className="w-full bg-surface border border-surface-border rounded-xl px-4 py-3 text-white placeholder-slate-500 focus:outline-none focus:border-brand-500 focus:ring-1 focus:ring-brand-500 transition"
              />
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium text-slate-300 mb-2">
              Additional Context <span className="text-slate-500">(optional)</span>
            </label>
            <textarea
              rows={2}
              value={form.description}
              onChange={(e) => setForm({ ...form, description: e.target.value })}
              placeholder="Business model, team background, constraints..."
              className="w-full bg-surface border border-surface-border rounded-xl px-4 py-3 text-white placeholder-slate-500 focus:outline-none focus:border-brand-500 focus:ring-1 focus:ring-brand-500 resize-none transition"
            />
          </div>

          <button
            type="submit"
            disabled={state === "loading"}
            className="flex items-center justify-center gap-2 w-full py-3 px-6 bg-gradient-to-r from-brand-600 to-purple-600 text-white font-semibold rounded-xl hover:from-brand-500 hover:to-purple-500 transition-all duration-200 disabled:opacity-60 disabled:cursor-not-allowed shadow-glow-brand"
          >
            {state === "loading" ? (
              <>
                <Loader2 className="w-4 h-4 animate-spin" />
                Running multi-agent analysis...
              </>
            ) : (
              <>
                <Send className="w-4 h-4" />
                Validate Startup Idea
              </>
            )}
          </button>
        </form>
      </div>

      {/* Error */}
      {state === "error" && (
        <div className="glass rounded-2xl p-5 border border-red-500/30 bg-red-500/10 mb-6 animate-slide-up">
          <div className="flex items-center gap-2 text-red-400">
            <XCircle className="w-5 h-5" />
            <p className="font-medium">{error}</p>
          </div>
        </div>
      )}

      {/* Results */}
      {result && state === "success" && (
        <div className="space-y-6 animate-slide-up">
          {/* Verdict + Executive Summary */}
          <div className="glass rounded-2xl p-6 border border-surface-border">
            <div className="flex items-start justify-between gap-4 mb-4">
              <div>
                <h2 className="text-lg font-bold text-white mb-1">Validation Report</h2>
                <p className="text-slate-400 text-sm">{result.idea}</p>
              </div>
              {verdictCfg && (
                <span className={`flex items-center gap-1.5 px-4 py-1.5 rounded-full text-sm font-bold flex-shrink-0 ${verdictCfg.color}`}>
                  <verdictCfg.icon className="w-4 h-4" />
                  {verdictCfg.label}
                </span>
              )}
            </div>
            <p className="text-slate-300 leading-relaxed border-t border-surface-border pt-4">
              {result.executive_summary}
            </p>
          </div>

          {/* Scores */}
          <div className="glass rounded-2xl p-6 border border-surface-border">
            <h3 className="font-semibold text-white mb-5 flex items-center gap-2">
              <BarChart3 className="w-4 h-4 text-brand-400" /> Score Breakdown
            </h3>
            <div className="space-y-4">
              <ScoreBar label="Overall Viability" score={result.overall_score} color="bg-brand-500" />
              <ScoreBar label="Market Opportunity" score={result.market_score} color="bg-emerald-500" />
              <ScoreBar label="Competitive Positioning" score={result.competition_score} color="bg-purple-500" />
              <ScoreBar label="Risk-Adjusted Score" score={result.risk_score} color="bg-orange-500" />
            </div>
          </div>

          {/* Strengths & Risks */}
          <div className="grid grid-cols-2 gap-6">
            <div className="glass rounded-2xl p-5 border border-emerald-500/20">
              <h3 className="font-semibold text-emerald-400 mb-3 flex items-center gap-2">
                <CheckCircle2 className="w-4 h-4" /> Key Strengths
              </h3>
              <ul className="space-y-2">
                {result.key_strengths.map((s, i) => (
                  <li key={i} className="text-sm text-slate-300 flex items-start gap-2">
                    <span className="text-emerald-500 mt-0.5 flex-shrink-0">•</span> {s}
                  </li>
                ))}
              </ul>
            </div>
            <div className="glass rounded-2xl p-5 border border-red-500/20">
              <h3 className="font-semibold text-red-400 mb-3 flex items-center gap-2">
                <Shield className="w-4 h-4" /> Key Risks
              </h3>
              <ul className="space-y-2">
                {result.key_risks.map((r, i) => (
                  <li key={i} className="text-sm text-slate-300 flex items-start gap-2">
                    <span className="text-red-500 mt-0.5 flex-shrink-0">•</span> {r}
                  </li>
                ))}
              </ul>
            </div>
          </div>

          {/* Recommendations */}
          <div className="glass rounded-2xl p-6 border border-surface-border">
            <h3 className="font-semibold text-white mb-4 flex items-center gap-2">
              <TrendingUp className="w-4 h-4 text-brand-400" /> Recommendations
            </h3>
            <ol className="space-y-2">
              {result.recommendations.map((rec, i) => (
                <li key={i} className="flex items-start gap-3 text-sm text-slate-300">
                  <span className="flex-shrink-0 w-6 h-6 rounded-full bg-brand-500/20 text-brand-300 text-xs font-bold flex items-center justify-center">
                    {i + 1}
                  </span>
                  {rec}
                </li>
              ))}
            </ol>
          </div>

          {/* Research Detail */}
          <div className="glass rounded-2xl p-6 border border-surface-border">
            <h3 className="font-semibold text-white mb-3 flex items-center gap-2">
              <Users className="w-4 h-4 text-brand-400" /> Market Research
            </h3>
            <p className="text-slate-400 text-sm leading-relaxed whitespace-pre-line">
              {result.market_research}
            </p>
          </div>
        </div>
      )}
    </div>
  );
}
