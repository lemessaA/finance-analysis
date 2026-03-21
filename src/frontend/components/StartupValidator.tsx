"use client";

import { useState } from 'react';
import { validateStartup } from '@/services/api';
import { StartupValidationResponse } from '@/types';
import { 
  Lightbulb, 
  TrendingUp, 
  Shield, 
  CheckCircle2, 
  AlertTriangle,
  Target,
  Users,
  BarChart3,
  Send,
  Loader2
} from 'lucide-react';

type LoadingState = "idle" | "loading" | "success" | "error";

export default function StartupValidator() {
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
      setError(
        err?.response?.data?.detail || "Validation failed. Please try again."
      );
      setState("error");
    }
  };

  const getVerdictConfig = (verdict: string) => {
    switch (verdict) {
      case "GO":
        return { color: "bg-green-500", icon: CheckCircle2, label: "GO" };
      case "CONDITIONAL GO":
        return { color: "bg-yellow-500", icon: AlertTriangle, label: "CONDITIONAL GO" };
      default:
        return { color: "bg-red-500", icon: Shield, label: "NO GO" };
    }
  };

  const ScoreBar = ({ label, score, color }: { label: string; score: number; color: string }) => (
    <div>
      <div className="flex justify-between mb-2">
        <span className="text-sm text-gray-300">{label}</span>
        <span className="text-sm font-medium text-white">{score}/100</span>
      </div>
      <div className="w-full bg-gray-700 rounded-full h-2">
        <div
          className={`${color} h-2 rounded-full transition-all duration-500`}
          style={{ width: `${score}%` }}
        />
      </div>
    </div>
  );

  return (
    <div className="space-y-8">
      {/* Input Form */}
      <div className="bg-white/10 backdrop-blur-lg rounded-2xl p-8 border border-white/20">
        <div className="flex items-center space-x-3 mb-6">
          <div className="p-3 bg-purple-500/20 rounded-xl">
            <Lightbulb className="w-6 h-6 text-purple-400" />
          </div>
          <div>
            <h2 className="text-2xl font-bold text-white">Startup Validator</h2>
            <p className="text-gray-300">Get AI-powered validation for your startup idea</p>
          </div>
        </div>

        <form onSubmit={handleSubmit} className="space-y-6">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <label className="block text-sm font-medium text-gray-200 mb-2">
                Startup Idea *
              </label>
              <textarea
                value={form.idea}
                onChange={(e) => setForm({ ...form, idea: e.target.value })}
                className="w-full px-4 py-3 bg-white/5 border border-white/20 rounded-xl text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all"
                placeholder="Describe your startup idea in detail..."
                rows={4}
                required
              />
            </div>
            
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-200 mb-2">
                  Industry *
                </label>
                <input
                  type="text"
                  value={form.industry}
                  onChange={(e) => setForm({ ...form, industry: e.target.value })}
                  className="w-full px-4 py-3 bg-white/5 border border-white/20 rounded-xl text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all"
                  placeholder="e.g., HealthTech, FinTech, SaaS"
                  required
                />
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-200 mb-2">
                  Target Market
                </label>
                <select
                  value={form.targetMarket}
                  onChange={(e) => setForm({ ...form, targetMarket: e.target.value })}
                  className="w-full px-4 py-3 bg-white/5 border border-white/20 rounded-xl text-white focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all"
                >
                  <option value="Global">Global</option>
                  <option value="North America">North America</option>
                  <option value="Europe">Europe</option>
                  <option value="Asia">Asia</option>
                  <option value="United States">United States</option>
                </select>
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-200 mb-2">
                  Business Stage
                </label>
                <select
                  value={form.businessStage}
                  onChange={(e) => setForm({ ...form, businessStage: e.target.value })}
                  className="w-full px-4 py-3 bg-white/5 border border-white/20 rounded-xl text-white focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all"
                >
                  <option value="Idea Stage">Idea Stage</option>
                  <option value="Early Stage">Early Stage</option>
                  <option value="Growth Stage">Growth Stage</option>
                  <option value="Mature">Mature</option>
                </select>
              </div>
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-200 mb-2">
              Additional Context
            </label>
            <textarea
              value={form.description}
              onChange={(e) => setForm({ ...form, description: e.target.value })}
              className="w-full px-4 py-3 bg-white/5 border border-white/20 rounded-xl text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all"
              placeholder="Any additional information about your startup..."
              rows={3}
            />
          </div>

          {error && (
            <div className="bg-red-500/20 border border-red-500/50 rounded-xl p-4 text-red-200">
              {error}
            </div>
          )}

          <button
            type="submit"
            disabled={state === "loading"}
            className="w-full bg-gradient-to-r from-purple-600 to-blue-600 text-white font-semibold py-3 px-6 rounded-xl hover:from-purple-700 hover:to-blue-700 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:ring-offset-2 focus:ring-offset-transparent transition-all disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center space-x-2"
          >
            {state === "loading" ? (
              <>
                <Loader2 className="w-5 h-5 animate-spin" />
                <span>Validating...</span>
              </>
            ) : (
              <>
                <Send className="w-5 h-5" />
                <span>Validate Startup</span>
              </>
            )}
          </button>
        </form>
      </div>

      {/* Results */}
      {result && state === "success" && (
        <div className="space-y-6 animate-fade-in">
          {/* Verdict Card */}
          <div className="bg-white/10 backdrop-blur-lg rounded-2xl p-8 border border-white/20">
            <div className="flex items-start justify-between mb-6">
              <div>
                <h3 className="text-xl font-bold text-white mb-2">Validation Report</h3>
                <p className="text-gray-300">{result.idea}</p>
              </div>
              {(() => {
                const verdictCfg = getVerdictConfig(result.verdict);
                const VerdictIcon = verdictCfg.icon;
                return (
                  <div className={`flex items-center space-x-2 px-4 py-2 rounded-full ${verdictCfg.color} bg-opacity-20`}>
                    <VerdictIcon className="w-5 h-5 text-white" />
                    <span className="text-white font-bold">{verdictCfg.label}</span>
                  </div>
                );
              })()}
            </div>
            
            <div className="prose prose-invert max-w-none">
              <p className="text-gray-300 leading-relaxed border-t border-white/10 pt-6">
                {result.executive_summary}
              </p>
            </div>
          </div>

          {/* Scores */}
          <div className="bg-white/10 backdrop-blur-lg rounded-2xl p-8 border border-white/20">
            <div className="flex items-center space-x-3 mb-6">
              <BarChart3 className="w-6 h-6 text-purple-400" />
              <h3 className="text-xl font-bold text-white">Score Breakdown</h3>
            </div>
            <div className="space-y-6">
              <ScoreBar label="Overall Viability" score={result.overall_score} color="bg-purple-500" />
              <ScoreBar label="Market Opportunity" score={result.market_score} color="bg-green-500" />
              <ScoreBar label="Competitive Positioning" score={result.competition_score} color="bg-blue-500" />
              <ScoreBar label="Risk-Adjusted Score" score={result.risk_score} color="bg-orange-500" />
            </div>
          </div>

          {/* Strengths & Risks */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <div className="bg-white/10 backdrop-blur-lg rounded-2xl p-6 border border-green-500/20">
              <div className="flex items-center space-x-3 mb-4">
                <CheckCircle2 className="w-5 h-5 text-green-400" />
                <h3 className="text-lg font-bold text-green-400">Key Strengths</h3>
              </div>
              <ul className="space-y-3">
                {result.key_strengths.map((strength, i) => (
                  <li key={i} className="flex items-start space-x-2">
                    <span className="text-green-500 mt-1">•</span>
                    <span className="text-gray-300 text-sm">{strength}</span>
                  </li>
                ))}
              </ul>
            </div>
            
            <div className="bg-white/10 backdrop-blur-lg rounded-2xl p-6 border border-red-500/20">
              <div className="flex items-center space-x-3 mb-4">
                <Shield className="w-5 h-5 text-red-400" />
                <h3 className="text-lg font-bold text-red-400">Key Risks</h3>
              </div>
              <ul className="space-y-3">
                {result.key_risks.map((risk, i) => (
                  <li key={i} className="flex items-start space-x-2">
                    <span className="text-red-500 mt-1">•</span>
                    <span className="text-gray-300 text-sm">{risk}</span>
                  </li>
                ))}
              </ul>
            </div>
          </div>

          {/* Recommendations */}
          <div className="bg-white/10 backdrop-blur-lg rounded-2xl p-8 border border-white/20">
            <div className="flex items-center space-x-3 mb-6">
              <Target className="w-6 h-6 text-blue-400" />
              <h3 className="text-xl font-bold text-white">Recommendations</h3>
            </div>
            <ol className="space-y-4">
              {result.recommendations.map((rec, i) => (
                <li key={i} className="flex items-start space-x-4">
                  <div className="flex-shrink-0 w-8 h-8 rounded-full bg-blue-500/20 text-blue-300 text-sm font-bold flex items-center justify-center">
                    {i + 1}
                  </div>
                  <span className="text-gray-300">{rec}</span>
                </li>
              ))}
            </ol>
          </div>

          {/* Market Research */}
          <div className="bg-white/10 backdrop-blur-lg rounded-2xl p-8 border border-white/20">
            <div className="flex items-center space-x-3 mb-6">
              <Users className="w-6 h-6 text-purple-400" />
              <h3 className="text-xl font-bold text-white">Market Research</h3>
            </div>
            <div className="prose prose-invert max-w-none">
              <p className="text-gray-300 leading-relaxed whitespace-pre-line">
                {result.market_research}
              </p>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
