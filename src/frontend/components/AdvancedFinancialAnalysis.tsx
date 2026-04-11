"use client";

import { useState, useEffect } from "react";
import {
  BarChart as RechartsBarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  RadarChart,
  PolarGrid,
  PolarAngleAxis,
  PolarRadiusAxis,
import {
  BarChart as RechartsBarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  RadarChart,
  PolarGrid,
  PolarAngleAxis,
  PolarRadiusAxis,
  Radar,
  Legend
} from "recharts";
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import {
  FileText,
  Upload,
  Loader2,
  TrendingUp,
  AlertTriangle,
  CheckCircle2,
  BarChart3,
  Target,
  Shield,
  Brain,
  Download,
  Eye,
  Calendar,
  DollarSign,
  Percent,
  Activity,
  Zap,
  Award,
  ArrowUpRight,
  ArrowDownRight,
  Minus,
  Filter,
  Search,
  X,
  MessageSquare,
  Send,
  Presentation
} from "lucide-react";

interface ChatMessage {
  role: "user" | "ai";
  content: string;
}

interface AdvancedAnalysisResult {
  analysis_id: string;
  filename: string;
  page_count: number;
  base_analysis: any;
  financial_ratios: any;
  trend_analysis?: any[];
  risk_assessment: any[];
  industry_benchmarking?: any[];
  financial_health_score: {
    overall_score: number;
    health_category: string;
    grade: string;
    score_components: any;
  };
  predictive_insights: any;
  recommendations: {
    immediate_actions: string[];
    short_term_goals: string[];
    long_term_strategy: string[];
    risk_mitigation: string[];
  };
  analysis_metadata: {
    industry?: string;
    has_historical_data: boolean;
    data_quality_score: number;
  };
}

interface AnalysisHistory {
  analyses: AdvancedAnalysisResult[];
  selectedAnalysis: AdvancedAnalysisResult | null;
  showComparison: boolean;
  comparisonAnalyses: string[];
}

export default function AdvancedFinancialAnalysis() {
  const [file, setFile] = useState<File | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [currentAnalysis, setCurrentAnalysis] = useState<AdvancedAnalysisResult | null>(null);
  const [analysisHistory, setAnalysisHistory] = useState<AnalysisHistory>({
    analyses: [],
    selectedAnalysis: null,
    showComparison: false,
    comparisonAnalyses: []
  });
  const [error, setError] = useState<string | null>(null);
  const [selectedIndustry, setSelectedIndustry] = useState<string>("");
  const [analysisDepth, setAnalysisDepth] = useState<"basic" | "standard" | "comprehensive">("comprehensive");
  const [showResults, setShowResults] = useState(false);
  
  // Chat feature state
  const [chatMessages, setChatMessages] = useState<ChatMessage[]>([]);
  const [chatInput, setChatInput] = useState("");
  const [isChatLoading, setIsChatLoading] = useState(false);
  
  // Pitch deck state
  const [pitchDeckContent, setPitchDeckContent] = useState<string | null>(null);
  const [investorScore, setInvestorScore] = useState<number | null>(null);
  const [isPitchDeckLoading, setIsPitchDeckLoading] = useState(false);

  // Integrations state
  const [syncSource, setSyncSource] = useState<"pdf" | "quickbooks" | "stripe">("pdf");
  const [isSyncing, setIsSyncing] = useState(false);

  const industries = [
    { value: "technology", label: "Technology" },
    { value: "manufacturing", label: "Manufacturing" },
    { value: "retail", label: "Retail" },
    { value: "healthcare", label: "Healthcare" },
    { value: "finance", label: "Finance" }
  ];

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setFile(e.target.files[0]);
      setError(null);
    }
  };

  const performAdvancedAnalysis = async () => {
    if (syncSource === "pdf" && !file) return;

    setIsLoading(true);
    setError(null);

    try {
      if (syncSource !== "pdf") {
        setIsSyncing(true);
        // Simulate a 2-second external API sync (QuickBooks/Stripe)
        await new Promise(r => setTimeout(r, 2000));
        setIsSyncing(false);
      }

      // If we're mocking the external sync, we pass a dummy file to the backend
      // In a real implementation, the backend would have a separate endpoint for this
      const formData = new FormData();
      if (syncSource === "pdf" && file) {
        formData.append("file", file);
      } else {
        const dummyBlob = new Blob(["Simulated financial extract from " + syncSource], { type: "application/pdf" });
        formData.append("file", new File([dummyBlob], `${syncSource}_import.pdf`));
      }

      const apiBase = process.env.NEXT_PUBLIC_API_URL || "";
      const url = `${apiBase}/api/v1/advanced/analyze-advanced?industry=${selectedIndustry}&analysis_depth=${analysisDepth}`;

      const response = await fetch(url, {
        method: "POST",
        body: formData
      });

      if (!response.ok) {
        let errorMessage = `Analysis failed (HTTP ${response.status})`;
        try {
          const errData = await response.json();
          errorMessage = errData?.detail || errData?.error?.message || errorMessage;
        } catch {}
        throw new Error(errorMessage);
      }

      const result = await response.json();
      setCurrentAnalysis(result.analysis_result);
      setAnalysisHistory(prev => ({
        ...prev,
        analyses: [result.analysis_result, ...prev.analyses]
      }));
      setChatMessages([
        { role: 'ai', content: `Hello! I've finished analyzing your ${result.analysis_result.page_count}-page financial report. Do you have any questions about the liquidity, risk, or projections?` }
      ]);
      setShowResults(true);
    } catch (err: any) {
      setError(err.message || "Advanced analysis failed. Please try again.");
    } finally {
      setIsLoading(false);
    }
  };

  const handleSendMessage = async () => {
    if (!chatInput.trim() || !currentAnalysis?.analysis_id) return;

    const userMessage = chatInput.trim();
    setChatInput("");
    setChatMessages(prev => [...prev, { role: "user", content: userMessage }]);
    setIsChatLoading(true);

    try {
      const apiBase = process.env.NEXT_PUBLIC_API_URL || "";
      const response = await fetch(`${apiBase}/api/v1/advanced/chat`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          analysis_id: currentAnalysis.analysis_id,
          message: userMessage
        })
      });

      if (!response.ok) throw new Error("Failed to send message");

      const result = await response.json();
      setChatMessages(prev => [...prev, { role: "ai", content: result.answer }]);
    } catch (err) {
      setChatMessages(prev => [...prev, { role: "ai", content: "Error: I couldn't process your request right now." }]);
    } finally {
      setIsChatLoading(false);
    }
  };

  const handleGeneratePitchDeck = async () => {
    if (!currentAnalysis?.analysis_id) return;
    setIsPitchDeckLoading(true);
    try {
      const apiBase = process.env.NEXT_PUBLIC_API_URL || "";
      const response = await fetch(`${apiBase}/api/v1/advanced/generate-pitch-deck`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ analysis_id: currentAnalysis.analysis_id })
      });
      if (!response.ok) throw new Error("Failed to generate pitch deck");
      const result = await response.json();
      setInvestorScore(result.investor_readiness_score);
      setPitchDeckContent(result.pitch_content);
    } catch (err) {
      setError("Failed to generate pitch deck.");
    } finally {
      setIsPitchDeckLoading(false);
    }
  };

  const getHealthScoreColor = (score: number) => {
    if (score >= 85) return "text-green-500";
    if (score >= 70) return "text-blue-500";
    if (score >= 55) return "text-yellow-500";
    if (score >= 40) return "text-orange-500";
    return "text-red-500";
  };

  const getHealthScoreBg = (score: number) => {
    if (score >= 85) return "bg-green-500/10 border-green-500/30";
    if (score >= 70) return "bg-blue-500/10 border-blue-500/30";
    if (score >= 55) return "bg-yellow-500/10 border-yellow-500/30";
    if (score >= 40) return "bg-orange-500/10 border-orange-500/30";
    return "bg-red-500/10 border-red-500/30";
  };

  const getRiskLevelColor = (level: string) => {
    switch (level) {
      case "low": return "text-green-500";
      case "medium": return "text-yellow-500";
      case "high": return "text-orange-500";
      case "critical": return "text-red-500";
      default: return "text-gray-500";
    }
  };

  const formatCurrency = (value: any) => {
    if (!value || value === "Not disclosed") return "Not disclosed";
    const num = Number(value);
    if (isNaN(num)) return value;
    return `$${num.toLocaleString()}`;
  };

  const formatPercent = (value: any) => {
    if (!value || value === "Not disclosed") return "Not disclosed";
    const num = Number(value);
    if (isNaN(num)) return value;
    return `${(num * 100).toFixed(1)}%`;
  };

  const renderFinancialHealthScore = (score: any) => (
    <div className={`glass rounded-2xl p-6 border ${getHealthScoreBg(score.overall_score)}`}>
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-xl font-semibold text-white">Financial Health Score</h3>
        <div className={`text-3xl font-bold ${getHealthScoreColor(score.overall_score)}`}>
          {score.overall_score}/100
        </div>
      </div>
      
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-4">
        <div className="text-center">
          <div className="text-sm text-gray-400 mb-1">Grade</div>
          <div className={`text-2xl font-bold ${getHealthScoreColor(score.overall_score)}`}>
            {score.grade}
          </div>
        </div>
        <div className="text-center">
          <div className="text-sm text-gray-400 mb-1">Category</div>
          <div className="text-lg font-medium text-white capitalize">
            {score.health_category}
          </div>
        </div>
        <div className="text-center">
          <div className="text-sm text-gray-400 mb-1">Profitability</div>
          <div className="text-lg font-medium text-white">
            {score.score_components.profitability}/100
          </div>
        </div>
        <div className="text-center">
          <div className="text-sm text-gray-400 mb-1">Liquidity</div>
          <div className="text-lg font-medium text-white">
            {score.score_components.liquidity}/100
          </div>
        </div>
      </div>
      
      <div className="w-full bg-white/10 rounded-full h-2 mb-2">
        <div 
          className={`h-2 rounded-full transition-all duration-500 ${
            score.overall_score >= 85 ? 'bg-green-500' :
            score.overall_score >= 70 ? 'bg-blue-500' :
            score.overall_score >= 55 ? 'bg-yellow-500' :
            score.overall_score >= 40 ? 'bg-orange-500' : 'bg-red-500'
          }`}
          style={{ width: `${score.overall_score}%` }}
        />
      </div>
    </div>
  );

  const renderRiskAssessment = (risks: any[]) => (
    <div className="glass rounded-2xl p-6 border border-white/10">
      <h3 className="text-xl font-semibold text-white mb-4 flex items-center gap-2">
        <Shield className="w-6 h-6 text-orange-500" />
        Risk Assessment
      </h3>
      
      <div className="space-y-3">
        {risks.map((risk, index) => (
          <div key={index} className="bg-white/5 rounded-xl p-4 border border-white/10">
            <div className="flex items-start justify-between mb-2">
              <div className="flex-1">
                <div className="flex items-center gap-2 mb-1">
                  <span className={`text-sm font-medium capitalize ${getRiskLevelColor(risk.level)}`}>
                    {risk.category} Risk
                  </span>
                  <span className={`text-xs px-2 py-1 rounded-full ${getRiskLevelColor(risk.level)} bg-current/20`}>
                    {risk.level}
                  </span>
                </div>
                <p className="text-gray-300 text-sm">{risk.description}</p>
              </div>
              <div className="text-lg font-bold text-white ml-4">
                {risk.score}/100
              </div>
            </div>
            
            {risk.mitigation_suggestions && (
              <div className="mt-3">
                <p className="text-xs text-gray-400 mb-2">Mitigation Strategies:</p>
                <ul className="space-y-1">
                  {risk.mitigation_suggestions.slice(0, 2).map((suggestion: string, i: number) => (
                    <li key={i} className="text-xs text-gray-300 flex items-start gap-1">
                      <span className="text-green-500 mt-0.5">•</span>
                      {suggestion}
                    </li>
                  ))}
                </ul>
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );

  const renderRecommendations = (recommendations: any) => (
    <div className="glass rounded-2xl p-6 border border-white/10">
      <h3 className="text-xl font-semibold text-white mb-4 flex items-center gap-2">
        <Brain className="w-6 h-6 text-purple-500" />
        AI Recommendations
      </h3>
      
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div>
          <h4 className="text-lg font-medium text-white mb-3 flex items-center gap-2">
            <Zap className="w-5 h-5 text-yellow-500" />
            Immediate Actions
          </h4>
          <ul className="space-y-2">
            {recommendations.immediate_actions.map((action: string, index: number) => (
              <li key={index} className="flex items-start gap-2">
                <ArrowUpRight className="w-4 h-4 text-red-500 mt-0.5 flex-shrink-0" />
                <span className="text-gray-300 text-sm">{action}</span>
              </li>
            ))}
          </ul>
        </div>
        
        <div>
          <h4 className="text-lg font-medium text-white mb-3 flex items-center gap-2">
            <Target className="w-5 h-5 text-blue-500" />
            Short-term Goals
          </h4>
          <ul className="space-y-2">
            {recommendations.short_term_goals.map((goal: string, index: number) => (
              <li key={index} className="flex items-start gap-2">
                <Target className="w-4 h-4 text-blue-500 mt-0.5 flex-shrink-0" />
                <span className="text-gray-300 text-sm">{goal}</span>
              </li>
            ))}
          </ul>
        </div>
        
        <div>
          <h4 className="text-lg font-medium text-white mb-3 flex items-center gap-2">
            <Award className="w-5 h-5 text-green-500" />
            Long-term Strategy
          </h4>
          <ul className="space-y-2">
            {recommendations.long_term_strategy.map((strategy: string, index: number) => (
              <li key={index} className="flex items-start gap-2">
                <Award className="w-4 h-4 text-green-500 mt-0.5 flex-shrink-0" />
                <span className="text-gray-300 text-sm">{strategy}</span>
              </li>
            ))}
          </ul>
        </div>
        
        <div>
          <h4 className="text-lg font-medium text-white mb-3 flex items-center gap-2">
            <Shield className="w-5 h-5 text-orange-500" />
            Risk Mitigation
          </h4>
          <ul className="space-y-2">
            {recommendations.risk_mitigation.map((mitigation: string, index: number) => (
              <li key={index} className="flex items-start gap-2">
                <Shield className="w-4 h-4 text-orange-500 mt-0.5 flex-shrink-0" />
                <span className="text-gray-300 text-sm">{mitigation}</span>
              </li>
            ))}
          </ul>
        </div>
      </div>
    </div>
  );

  const renderFinancialRatios = (ratios: any) => (
    <div className="glass rounded-2xl p-6 border border-white/10">
      <h3 className="text-xl font-semibold text-white mb-4 flex items-center gap-2">
        <BarChart3 className="w-6 h-6 text-blue-500" />
        Financial Ratios Analysis
      </h3>
      
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {Object.entries(ratios.liquidity_ratios).map(([key, value]) => (
          <div key={key} className="bg-white/5 rounded-xl p-4">
            <div className="text-sm text-gray-400 mb-1 capitalize">
              {key.replace(/_/g, ' ')}
            </div>
            <div className="text-xl font-bold text-white">
              {typeof value === 'number' ? value.toFixed(2) : String(value)}
            </div>
          </div>
        ))}
        
        {Object.entries(ratios.profitability_ratios).map(([key, value]) => (
          <div key={key} className="bg-white/5 rounded-xl p-4">
            <div className="text-sm text-gray-400 mb-1 capitalize">
              {key.replace(/_/g, ' ')}
            </div>
            <div className="text-xl font-bold text-white">
              {typeof value === 'number' ? formatPercent(value) : String(value)}
            </div>
          </div>
        ))}
        
        {Object.entries(ratios.efficiency_ratios).map(([key, value]) => (
          <div key={key} className="bg-white/5 rounded-xl p-4">
            <div className="text-sm text-gray-400 mb-1 capitalize">
              {key.replace(/_/g, ' ')}
            </div>
            <div className="text-xl font-bold text-white">
              {typeof value === 'number' ? value.toFixed(2) : String(value)}
            </div>
          </div>
        ))}
      </div>
    </div>
  );

  if (!showResults) {
    return (
      <div className="max-w-6xl mx-auto animate-fade-in">
        <div className="mb-8">
          <div className="flex items-center gap-3 mb-3">
            <div className="w-12 h-12 rounded-2xl bg-gradient-to-br from-purple-500 to-pink-600 flex items-center justify-center shadow-lg shadow-purple-500/20">
              <Brain className="w-6 h-6 text-white" />
            </div>
            <h1 className="text-3xl font-bold text-white tracking-tight">
              Advanced Financial Analysis
            </h1>
          </div>
          <p className="text-slate-400 max-w-2xl text-lg">
            AI-powered comprehensive financial analysis with risk assessment, industry benchmarking, and predictive insights.
          </p>
        </div>

        <div className="glass rounded-2xl p-8 border border-white/10 relative overflow-hidden">
          <div className="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-purple-500 via-pink-500 to-orange-500"></div>
          
          <div className="flex gap-4 mb-6 pb-6 border-b border-white/10">
            <button
              onClick={() => setSyncSource("pdf")}
              className={`px-4 py-2 rounded-lg font-medium transition-all ${syncSource === "pdf" ? 'bg-purple-600 text-white' : 'text-gray-400 hover:text-white hover:bg-white/5'}`}
            >
              PDF Upload
            </button>
            <button
              onClick={() => setSyncSource("quickbooks")}
              className={`px-4 py-2 rounded-lg font-medium transition-all ${syncSource === "quickbooks" ? 'bg-green-600 text-white' : 'text-gray-400 hover:text-white hover:bg-white/5'}`}
            >
              QuickBooks Sync
            </button>
            <button
              onClick={() => setSyncSource("stripe")}
              className={`px-4 py-2 rounded-lg font-medium transition-all ${syncSource === "stripe" ? 'bg-blue-600 text-white' : 'text-gray-400 hover:text-white hover:bg-white/5'}`}
            >
              Stripe Sync
            </button>
          </div>

          {syncSource === "pdf" ? (
            <div className="flex flex-col items-center justify-center border-2 border-dashed border-white/10 rounded-xl p-8 bg-black/20 hover:bg-white/5 transition-colors group cursor-pointer relative">
              <input
                type="file"
                className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
                accept=".pdf"
                onChange={handleFileChange}
              />
              <div className="w-16 h-16 rounded-full bg-purple-500/20 flex items-center justify-center mb-4 group-hover:scale-110 transition-transform">
                <Upload className="w-8 h-8 text-purple-400" />
              </div>
              <h3 className="text-xl font-medium text-white mb-2">
                {file ? file.name : "Upload Financial Report (PDF)"}
              </h3>
              <p className="text-gray-400 text-sm text-center max-w-sm">
                Upload your balance sheets, income statements, or full audit reports for deep analysis.
              </p>
            </div>
          ) : (
            <div className="flex flex-col items-center justify-center border border-white/10 rounded-xl p-8 bg-black/20">
              <div className={`w-16 h-16 rounded-2xl flex items-center justify-center mb-4 ${syncSource === 'quickbooks' ? 'bg-green-500/20 text-green-400' : 'bg-blue-500/20 text-blue-400'}`}>
                <Activity className="w-8 h-8" />
              </div>
              <h3 className="text-xl font-medium text-white mb-2">
                Connect {syncSource === "quickbooks" ? "QuickBooks Online" : "Stripe"}
              </h3>
              <p className="text-gray-400 text-sm text-center max-w-sm mb-6">
                Pull your real-time ledger data directly to perform predictive analysis and anomaly detection.
              </p>
              <button className="px-6 py-2 bg-white/10 text-white rounded-lg border border-white/20 hover:bg-white/20 transition-all font-medium text-sm">
                Authenticate Account
              </button>
            </div>
          )}

          <div className="mt-8 grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <label className="block text-sm font-medium text-slate-300 mb-2">
                Industry (Optional)
              </label>
              <select
                value={selectedIndustry}
                onChange={(e) => setSelectedIndustry(e.target.value)}
                className="w-full px-4 py-3 bg-white/5 border border-white/20 rounded-xl text-white focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent"
              >
                <option value="">Select Industry</option>
                {industries.map(industry => (
                  <option key={industry.value} value={industry.value}>
                    {industry.label}
                  </option>
                ))}
              </select>
            </div>
            
            <div>
              <label className="block text-sm font-medium text-slate-300 mb-2">
                Analysis Depth
              </label>
              <select
                value={analysisDepth}
                onChange={(e) => setAnalysisDepth(e.target.value as any)}
                className="w-full px-4 py-3 bg-white/5 border border-white/20 rounded-xl text-white focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent"
              >
                <option value="basic">Basic</option>
                <option value="standard">Standard</option>
                <option value="comprehensive">Comprehensive</option>
              </select>
            </div>
          </div>
          
          <div className="mt-8">
            <button
              onClick={performAdvancedAnalysis}
              disabled={isLoading || (syncSource === "pdf" && !file)}
              className="w-full py-4 bg-gradient-to-r from-purple-600 to-pink-600 text-white rounded-xl font-semibold text-lg hover:from-purple-500 hover:to-pink-500 transition-all flex items-center justify-center gap-2 shadow-xl shadow-purple-500/25 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {isLoading ? (
                <>
                  <Loader2 className="w-6 h-6 animate-spin" />
                  {isSyncing ? `Syncing from ${syncSource}...` : 'Analyzing Data...'}
                </>
              ) : (
                <>
                  <Zap className="w-6 h-6" />
                  Extract & Analyze Data
                </>
              )}
            </button>
          </div>
        </div>

        {error && (
          <div className="glass rounded-2xl p-6 border border-red-500/30 bg-red-500/10 mb-6">
            <div className="flex items-center gap-3 text-red-400">
              <AlertTriangle className="w-6 h-6" />
              <p className="text-lg font-medium">{error}</p>
            </div>
          </div>
        )}

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="glass rounded-2xl p-6 border border-white/10">
            <div className="flex items-center gap-3 mb-3">
              <div className="p-2 bg-purple-500/20 rounded-lg">
                <Target className="w-5 h-5 text-purple-400" />
              </div>
              <h3 className="text-lg font-semibold text-white">Financial Health Score</h3>
            </div>
            <p className="text-gray-300 text-sm">
              Comprehensive scoring system evaluating profitability, liquidity, leverage, and risk factors.
            </p>
          </div>
          
          <div className="glass rounded-2xl p-6 border border-white/10">
            <div className="flex items-center gap-3 mb-3">
              <div className="p-2 bg-blue-500/20 rounded-lg">
                <Shield className="w-5 h-5 text-blue-400" />
              </div>
              <h3 className="text-lg font-semibold text-white">Risk Assessment</h3>
            </div>
            <p className="text-gray-300 text-sm">
              Advanced risk analysis with scoring and mitigation strategies for multiple risk categories.
            </p>
          </div>
          
          <div className="glass rounded-2xl p-6 border border-white/10">
            <div className="flex items-center gap-3 mb-3">
              <div className="p-2 bg-green-500/20 rounded-lg">
                <TrendingUp className="w-5 h-5 text-green-400" />
              </div>
              <h3 className="text-lg font-semibold text-white">Industry Benchmarking</h3>
            </div>
            <p className="text-gray-300 text-sm">
              Compare performance against industry standards and identify competitive advantages.
            </p>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-6xl mx-auto animate-fade-in">
      <div className="mb-8 flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="w-12 h-12 rounded-2xl bg-gradient-to-br from-purple-500 to-pink-600 flex items-center justify-center shadow-lg shadow-purple-500/20">
            <Brain className="w-6 h-6 text-white" />
          </div>
          <div>
            <h1 className="text-3xl font-bold text-white tracking-tight">
              Analysis Results
            </h1>
            <p className="text-slate-400">
              {currentAnalysis?.filename} • {currentAnalysis?.page_count} pages
            </p>
          </div>
        </div>
        
        <div className="flex gap-4">
          <button
            onClick={handleGeneratePitchDeck}
            disabled={isPitchDeckLoading}
            className="px-6 py-3 bg-gradient-to-r from-purple-600 to-pink-600 text-white rounded-xl hover:from-purple-500 hover:to-pink-500 transition-all flex items-center gap-2 disabled:opacity-50"
          >
            {isPitchDeckLoading ? <Loader2 className="w-5 h-5 animate-spin" /> : <Presentation className="w-5 h-5" />}
            Generate Pitch Deck
          </button>
          <button
            onClick={() => setShowResults(false)}
            className="px-6 py-3 bg-white/10 text-white rounded-xl hover:bg-white/20 transition-all"
          >
            New Analysis
          </button>
        </div>
      </div>

      {investorScore !== null && pitchDeckContent && (
        <div className="glass rounded-2xl p-8 mb-8 border border-purple-500/30">
          <div className="flex items-center justify-between border-b border-white/10 pb-6 mb-6">
            <h2 className="text-2xl font-bold text-white flex items-center gap-3">
              <Presentation className="w-8 h-8 text-purple-400" />
              Investor Pitch Deck & Readiness
            </h2>
            <div className="text-center bg-black/30 rounded-xl px-6 py-3 border border-white/10">
              <div className="text-sm text-gray-400 mb-1">Investor Readiness Score</div>
              <div className={`text-3xl font-bold ${getHealthScoreColor(investorScore)}`}>
                {investorScore}/100
              </div>
            </div>
          </div>
          <div className="prose prose-invert prose-purple max-w-none">
            <ReactMarkdown remarkPlugins={[remarkGfm]}>
              {pitchDeckContent}
            </ReactMarkdown>
          </div>
        </div>
      )}

      {currentAnalysis && (
        <div className="space-y-8">
          {/* Financial Health Score */}
          {renderFinancialHealthScore(currentAnalysis.financial_health_score)}
          
          {/* Key Metrics Overview */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            {Object.entries(currentAnalysis.base_analysis.metrics).slice(0, 8).map(([key, value]) => (
              <div key={key} className="bg-white/5 rounded-xl p-4">
                <div className="text-sm text-gray-400 mb-1 capitalize">
                  {key.replace(/_/g, ' ')}
                </div>
                <div className="text-xl font-bold text-white">
                  {key.includes('margin') || key.includes('growth') ? formatPercent(value) : formatCurrency(value)}
                </div>
              </div>
            ))}
          </div>
          
          {/* Financial Ratios */}
          {renderFinancialRatios(currentAnalysis.financial_ratios)}
          
          {/* Interactive Data Visualizations */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mt-6">
            <div className="glass rounded-2xl p-6 border border-white/10">
              <h3 className="text-xl font-semibold text-white mb-6 flex items-center gap-2">
                <BarChart3 className="w-6 h-6 text-purple-500" />
                Key Metrics Overview
              </h3>
              <div className="h-[300px] w-full">
                <ResponsiveContainer width="100%" height="100%">
                  <RechartsBarChart
                    data={Object.entries(currentAnalysis.base_analysis.metrics)
                      .slice(0, 5)
                      .filter(([_, v]) => typeof v === 'number')
                      .map(([k, v]) => ({
                        name: k.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase()),
                        value: v
                      }))}
                    margin={{ top: 5, right: 30, left: 20, bottom: 5 }}
                  >
                    <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.1)" />
                    <XAxis dataKey="name" stroke="rgba(255,255,255,0.5)" tick={{fill: 'rgba(255,255,255,0.7)', fontSize: 12}} />
                    <YAxis stroke="rgba(255,255,255,0.5)" tick={{fill: 'rgba(255,255,255,0.7)', fontSize: 12}} />
                    <Tooltip 
                      contentStyle={{ backgroundColor: 'rgba(17, 24, 39, 0.9)', borderColor: 'rgba(255,255,255,0.1)', color: '#fff', borderRadius: '8px' }}
                      itemStyle={{ color: '#a855f7' }}
                      formatter={(value: any) => formatCurrency(value)}
                    />
                    <Bar dataKey="value" fill="#8b5cf6" radius={[4, 4, 0, 0]} />
                  </RechartsBarChart>
                </ResponsiveContainer>
              </div>
            </div>

            <div className="glass rounded-2xl p-6 border border-white/10">
              <h3 className="text-xl font-semibold text-white mb-6 flex items-center gap-2">
                <Shield className="w-6 h-6 text-orange-500" />
                Risk Radar
              </h3>
              <div className="h-[300px] w-full">
                <ResponsiveContainer width="100%" height="100%">
                  <RadarChart cx="50%" cy="50%" outerRadius="80%" data={currentAnalysis.risk_assessment.map(r => ({
                    subject: r.category,
                    A: r.score,
                    fullMark: 100,
                  }))}>
                    <PolarGrid stroke="rgba(255,255,255,0.2)" />
                    <PolarAngleAxis dataKey="subject" tick={{fill: 'rgba(255,255,255,0.7)', fontSize: 12}} />
                    <PolarRadiusAxis angle={30} domain={[0, 100]} tick={{fill: 'rgba(255,255,255,0.5)'}} />
                    <Radar name="Risk Score" dataKey="A" stroke="#f97316" fill="#f97316" fillOpacity={0.4} />
                    <Tooltip 
                      contentStyle={{ backgroundColor: 'rgba(17, 24, 39, 0.9)', borderColor: 'rgba(255,255,255,0.1)', color: '#fff', borderRadius: '8px' }}
                      itemStyle={{ color: '#f97316' }}
                    />
                  </RadarChart>
                </ResponsiveContainer>
              </div>
            </div>
          </div>
          
          {/* Risk Assessment Details */}
          {renderRiskAssessment(currentAnalysis.risk_assessment)}
          
          {/* Industry Benchmarking (Feature 5) */}
          {currentAnalysis.industry_benchmarking && currentAnalysis.industry_benchmarking.length > 0 && (
            <div className="glass rounded-2xl p-6 border border-white/10">
              <h3 className="text-xl font-semibold text-white mb-4 flex items-center gap-2">
                <Target className="w-6 h-6 text-blue-500" />
                Industry Benchmarks Overview
              </h3>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                {currentAnalysis.industry_benchmarking.map((bm: any, idx: number) => (
                  <div key={idx} className="bg-white/5 rounded-xl p-4 border border-white/5 relative overflow-hidden">
                    <div className="text-sm text-gray-400 capitalize">{bm.metric?.replace(/_/g, ' ') || "Metric"}</div>
                    <div className="font-bold text-white text-lg mt-1">{bm.startup_value || "N/A"}</div>
                    <div className={`text-xs mt-2 font-medium bg-black/30 w-fit px-2 py-1 rounded flex items-center gap-1 ${bm.comparison === 'above_average' ? 'text-green-400' : bm.comparison === 'below_average' ? 'text-red-400' : 'text-blue-400'}`}>
                      {bm.comparison === 'above_average' ? <TrendingUp className="w-3 h-3"/> : bm.comparison === 'below_average' ? <ArrowDownRight className="w-3 h-3"/> : <Minus className="w-3 h-3"/>}
                      {bm.comparison?.replace(/_/g, ' ') || "Average"}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Anomaly Detection Alerts (Feature 6) */}
          {currentAnalysis.risk_assessment && currentAnalysis.risk_assessment.some(r => r.level === 'critical' || r.category.toLowerCase().includes('fraud') || r.category.toLowerCase().includes('anomaly')) && (
            <div className="bg-red-500/10 border border-red-500/20 rounded-2xl p-6">
              <h3 className="text-xl font-semibold text-red-500 mb-4 flex items-center gap-2">
                <AlertTriangle className="w-6 h-6" />
                Automated Anomaly Detection
              </h3>
              <ul className="space-y-3">
                {currentAnalysis.risk_assessment
                    .filter(r => r.level === 'critical' || r.category.toLowerCase().includes('fraud') || r.category.toLowerCase().includes('anomaly'))
                    .map((r, idx) => (
                  <li key={idx} className="flex gap-3 text-red-100">
                    <Zap className="w-5 h-5 text-red-500 flex-shrink-0 mt-0.5" />
                    <div>
                      <strong className="block text-red-400">{r.category} detected</strong>
                      <span className="text-sm opacity-90">{r.finding}</span>
                    </div>
                  </li>
                ))}
              </ul>
            </div>
          )}
          
          {/* Recommendations */}
          {renderRecommendations(currentAnalysis.recommendations)}
          
          {/* AI Financial Chat */}
          <div className="glass rounded-2xl border border-white/10 overflow-hidden flex flex-col h-[500px]">
            <div className="p-6 border-b border-white/10 bg-white/5">
              <h3 className="text-xl font-semibold text-white flex items-center gap-2">
                <MessageSquare className="w-6 h-6 text-purple-400" />
                Chat with your Financials
              </h3>
              <p className="text-sm text-gray-400 mt-1">Ask questions directly about your submitted report and analysis.</p>
            </div>
            
            <div className="flex-1 overflow-y-auto p-6 space-y-4 bg-black/20">
              {chatMessages.map((msg, i) => (
                <div key={i} className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
                  <div className={`max-w-[80%] rounded-2xl p-4 ${msg.role === 'user' ? 'bg-purple-600 text-white' : 'glass border border-white/10 text-gray-200'}`}>
                    {msg.role === 'ai' && <Brain className="w-4 h-4 mb-2 text-purple-400" />}
                    <div className="text-sm leading-relaxed whitespace-pre-wrap">{msg.content}</div>
                  </div>
                </div>
              ))}
              {isChatLoading && (
                <div className="flex justify-start">
                  <div className="glass border border-white/10 rounded-2xl p-4 flex items-center gap-2">
                    <Loader2 className="w-4 h-4 animate-spin text-purple-400" />
                    <span className="text-sm text-gray-400">Analyzing...</span>
                  </div>
                </div>
              )}
            </div>
            
            <div className="p-4 border-t border-white/10 bg-white/5">
              <form 
                onSubmit={(e) => { e.preventDefault(); handleSendMessage(); }}
                className="relative"
              >
                <input
                  type="text"
                  value={chatInput}
                  onChange={(e) => setChatInput(e.target.value)}
                  placeholder="Ask a question about your financials..."
                  className="w-full pl-4 pr-12 py-4 bg-black/30 border border-white/10 rounded-xl text-white focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all"
                />
                <button
                  type="submit"
                  disabled={isChatLoading || !chatInput.trim()}
                  className="absolute right-2 top-2 p-2 bg-gradient-to-r from-purple-600 to-pink-600 text-white rounded-lg hover:from-purple-500 hover:to-pink-500 transition-all disabled:opacity-50"
                >
                  <Send className="w-5 h-5" />
                </button>
              </form>
            </div>
          </div>

          {/* Analysis Metadata */}
          <div className="glass rounded-2xl p-6 border border-white/10">
            <h3 className="text-lg font-semibold text-white mb-4">Analysis Information</h3>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm">
              <div>
                <span className="text-gray-400">Data Quality Score:</span>
                <span className="text-white ml-2">{currentAnalysis.analysis_metadata.data_quality_score}/100</span>
              </div>
              <div>
                <span className="text-gray-400">Industry:</span>
                <span className="text-white ml-2 capitalize">
                  {currentAnalysis.analysis_metadata.industry || "Not specified"}
                </span>
              </div>
              <div>
                <span className="text-gray-400">Historical Data:</span>
                <span className="text-white ml-2">
                  {currentAnalysis.analysis_metadata.has_historical_data ? "Available" : "Not available"}
                </span>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
