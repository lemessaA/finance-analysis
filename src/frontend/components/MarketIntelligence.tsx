"use client";

import { useState } from 'react';
import { getMarketIntelligence } from '@/services/api';
import { MarketIntelligenceResponse } from '@/types';
import { 
  LineChart, 
  TrendingUp, 
  Target, 
  Globe, 
  Users, 
  DollarSign,
  Building,
  AlertTriangle,
  CheckCircle2,
  Send,
  Loader2,
  BarChart3
} from 'lucide-react';

type LoadingState = "idle" | "loading" | "success" | "error";

export default function MarketIntelligence() {
  const [form, setForm] = useState({
    industry: "",
    targetMarket: "Global",
  });
  
  const [state, setState] = useState<LoadingState>("idle");
  const [result, setResult] = useState<MarketIntelligenceResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

  // Sample examples for users
  const sampleExamples = [
    {
      industry: "Agriculture Technology",
      targetMarket: "Ethiopia",
      description: "Digital farming solutions and agricultural marketplace platforms"
    },
    {
      industry: "FinTech",
      targetMarket: "Ethiopian SMEs",
      description: "Mobile banking, digital payments, and microfinance for Ethiopian small businesses"
    },
    {
      industry: "Renewable Energy",
      targetMarket: "Ethiopia Rural",
      description: "Solar energy solutions and off-grid power systems for rural Ethiopian communities"
    },
    {
      industry: "E-commerce",
      targetMarket: "Addis Ababa",
      description: "Online retail and delivery platforms targeting Addis Ababa urban consumers"
    },
    {
      industry: "Health Technology",
      targetMarket: "Ethiopia",
      description: "Digital health platforms and telemedicine solutions for Ethiopian healthcare"
    }
  ];

  const loadExample = (example: typeof sampleExamples[0]) => {
    setForm({
      industry: example.industry,
      targetMarket: example.targetMarket,
    });
    setError(null);
    setState("idle");
  };

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
        err?.response?.data?.detail || "Market analysis failed. Please try again."
      );
      setState("error");
    }
  };

  const CompetitorCard = ({ competitor }: { competitor: any }) => (
    <div className="bg-white/5 rounded-xl p-4 border border-white/10 hover:bg-white/10 transition-colors">
      <div className="flex items-start justify-between mb-3">
        <h4 className="font-semibold text-white">{competitor.name}</h4>
        <span className="text-sm text-purple-400 font-medium">{competitor.market_share_estimate}</span>
      </div>
      <p className="text-gray-400 text-sm mb-3">{competitor.description}</p>
      <div className="space-y-2">
        <div>
          <span className="text-xs text-green-400 font-medium">Strengths:</span>
          <ul className="text-xs text-gray-300 mt-1 space-y-1">
            {competitor.strengths.slice(0, 2).map((strength: string, i: number) => (
              <li key={i} className="flex items-start space-x-1">
                <span>•</span>
                <span>{strength}</span>
              </li>
            ))}
          </ul>
        </div>
        <div>
          <span className="text-xs text-red-400 font-medium">Weaknesses:</span>
          <ul className="text-xs text-gray-300 mt-1 space-y-1">
            {competitor.weaknesses.slice(0, 2).map((weakness: string, i: number) => (
              <li key={i} className="flex items-start space-x-1">
                <span>•</span>
                <span>{weakness}</span>
              </li>
            ))}
          </ul>
        </div>
      </div>
    </div>
  );

  return (
    <div className="space-y-8">
      {/* Input Form */}
      <div className="bg-white/10 backdrop-blur-lg rounded-2xl p-8 border border-white/20">
        <div className="flex items-center space-x-3 mb-6">
          <div className="p-3 bg-blue-500/20 rounded-xl">
            <LineChart className="w-6 h-6 text-blue-400" />
          </div>
          <div>
            <h2 className="text-2xl font-bold text-white">Market Intelligence</h2>
            <p className="text-gray-300">Get comprehensive Ethiopian market analysis and competitor insights</p>
          </div>
        </div>

        {/* Example Templates */}
        <div className="mb-6 p-4 bg-blue-500/10 rounded-xl border border-blue-500/30">
          <p className="text-sm font-medium text-blue-300 mb-3">📊 Sample Ethiopian Market Examples:</p>
          <div className="space-y-2">
            {sampleExamples.map((example, index) => (
              <button
                key={index}
                onClick={() => loadExample(example)}
                className="w-full text-left p-3 bg-white/5 rounded-lg hover:bg-white/10 transition-colors text-sm"
              >
                <span className="text-blue-400 font-medium">{example.industry} → {example.targetMarket}:</span>
                <span className="text-gray-300 ml-2">{example.description}</span>
              </button>
            ))}
          </div>
        </div>

        <form onSubmit={handleSubmit} className="space-y-6">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <label className="block text-sm font-medium text-gray-200 mb-2">
                Industry *
              </label>
              <input
                type="text"
                value={form.industry}
                onChange={(e) => setForm({ ...form, industry: e.target.value })}
                className="w-full px-4 py-3 bg-white/5 border border-white/20 rounded-xl text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all"
                placeholder="e.g., Agriculture Technology, FinTech, Renewable Energy..."
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
                className="w-full px-4 py-3 bg-white/5 border border-white/20 rounded-xl text-white focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all"
              >
                <option value="Ethiopia">Ethiopia</option>
                <option value="Addis Ababa">Addis Ababa</option>
                <option value="Ethiopia Rural">Ethiopia Rural</option>
                <option value="Ethiopian SMEs">Ethiopian SMEs</option>
                <option value="East Africa">East Africa</option>
                <option value="Global">Global</option>
              </select>
            </div>
          </div>

          {error && (
            <div className="bg-red-500/20 border border-red-500/50 rounded-xl p-4 text-red-200">
              {error}
            </div>
          )}

          <button
            type="submit"
            disabled={state === "loading"}
            className="w-full bg-gradient-to-r from-blue-600 to-purple-600 text-white font-semibold py-3 px-6 rounded-xl hover:from-blue-700 hover:to-purple-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 focus:ring-offset-transparent transition-all disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center space-x-2"
          >
            {state === "loading" ? (
              <>
                <Loader2 className="w-5 h-5 animate-spin" />
                <span>Analyzing Market...</span>
              </>
            ) : (
              <>
                <Send className="w-5 h-5" />
                <span>Analyze Market</span>
              </>
            )}
          </button>
        </form>
      </div>

      {/* Results */}
      {result && state === "success" && (
        <div className="space-y-6 animate-fade-in">
          {/* Market Overview */}
          <div className="bg-white/10 backdrop-blur-lg rounded-2xl p-8 border border-white/20">
            <div className="flex items-center space-x-3 mb-6">
              <Globe className="w-6 h-6 text-blue-400" />
              <h3 className="text-xl font-bold text-white">Market Overview</h3>
            </div>
            
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">
              <div className="text-center">
                <div className="inline-flex items-center justify-center w-12 h-12 bg-blue-500/20 rounded-xl mb-3">
                  <DollarSign className="w-6 h-6 text-blue-400" />
                </div>
                <h4 className="text-lg font-bold text-white mb-1">Market Size</h4>
                <p className="text-gray-300">{result.market_size_estimate}</p>
              </div>
              
              <div className="text-center">
                <div className="inline-flex items-center justify-center w-12 h-12 bg-green-500/20 rounded-xl mb-3">
                  <TrendingUp className="w-6 h-6 text-green-400" />
                </div>
                <h4 className="text-lg font-bold text-white mb-1">Growth Rate</h4>
                <p className="text-gray-300">{result.cagr_estimate}</p>
              </div>
              
              <div className="text-center">
                <div className="inline-flex items-center justify-center w-12 h-12 bg-purple-500/20 rounded-xl mb-3">
                  <Building className="w-6 h-6 text-purple-400" />
                </div>
                <h4 className="text-lg font-bold text-white mb-1">Industry</h4>
                <p className="text-gray-300">{result.industry}</p>
              </div>
            </div>
            
            <div className="prose prose-invert max-w-none">
              <p className="text-gray-300 leading-relaxed">{result.market_overview}</p>
            </div>
          </div>

          {/* Key Trends */}
          <div className="bg-white/10 backdrop-blur-lg rounded-2xl p-8 border border-white/20">
            <div className="flex items-center space-x-3 mb-6">
              <BarChart3 className="w-6 h-6 text-purple-400" />
              <h3 className="text-xl font-bold text-white">Key Trends</h3>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {result.key_trends.map((trend, i) => (
                <div key={i} className="flex items-start space-x-3 p-3 bg-white/5 rounded-xl">
                  <TrendingUp className="w-5 h-5 text-purple-400 mt-0.5 flex-shrink-0" />
                  <span className="text-gray-300">{trend}</span>
                </div>
              ))}
            </div>
          </div>

          {/* Opportunities & Risks */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <div className="bg-white/10 backdrop-blur-lg rounded-2xl p-6 border border-green-500/20">
              <div className="flex items-center space-x-3 mb-4">
                <CheckCircle2 className="w-5 h-5 text-green-400" />
                <h3 className="text-lg font-bold text-green-400">Opportunities</h3>
              </div>
              <ul className="space-y-3">
                {result.opportunities.map((opportunity, i) => (
                  <li key={i} className="flex items-start space-x-2">
                    <span className="text-green-500 mt-1">•</span>
                    <span className="text-gray-300 text-sm">{opportunity}</span>
                  </li>
                ))}
              </ul>
            </div>
            
            <div className="bg-white/10 backdrop-blur-lg rounded-2xl p-6 border border-red-500/20">
              <div className="flex items-center space-x-3 mb-4">
                <AlertTriangle className="w-5 h-5 text-red-400" />
                <h3 className="text-lg font-bold text-red-400">Risks</h3>
              </div>
              <ul className="space-y-3">
                {result.risks.map((risk, i) => (
                  <li key={i} className="flex items-start space-x-2">
                    <span className="text-red-500 mt-1">•</span>
                    <span className="text-gray-300 text-sm">{risk}</span>
                  </li>
                ))}
              </ul>
            </div>
          </div>

          {/* Top Competitors */}
          <div className="bg-white/10 backdrop-blur-lg rounded-2xl p-8 border border-white/20">
            <div className="flex items-center space-x-3 mb-6">
              <Users className="w-6 h-6 text-blue-400" />
              <h3 className="text-xl font-bold text-white">Top Competitors</h3>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {result.top_competitors.map((competitor, i) => (
                <CompetitorCard key={i} competitor={competitor} />
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
