"use client";

import { useState, useEffect } from "react";
import { getDashboardData, type DashboardData } from "@/services/api";
import {
  TrendingUp,
  Users,
  Target,
  DollarSign,
  BarChart3,
  PieChart,
  LineChart,
  ArrowUp,
  ArrowDown,
  Minus,
  Star,
  Globe,
  Building,
  AlertCircle,
  CheckCircle2,
  Loader2
} from "lucide-react";
import {
  LineChart as RechartsLineChart,
  Line,
  AreaChart,
  Area,
  BarChart as RechartsBarChart,
  Bar,
  PieChart as RechartsPieChart,
  Pie,
  Cell,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer
} from "recharts";

// Initial fallback data - matches DashboardData interface
const fallbackData: DashboardData = {
  score: 78,
  marketAnalysis: {
    marketSize: "$2.4B",
    growthRate: "18.5%",
    competitionLevel: "Medium",
    opportunityScore: 82
  },
  competitors: [
    { name: "TechCorp Inc.", marketShare: "32%", revenue: "$450M", strengths: ["Brand recognition", "Large customer base"], weaknesses: ["Slow innovation", "High pricing"] },
    { name: "StartupX", marketShare: "18%", revenue: "$180M", strengths: ["Agile", "Lower pricing"], weaknesses: ["Limited scale", "Newer brand"] },
    { name: "DataFlow", marketShare: "15%", revenue: "$150M", strengths: ["Tech leadership", "Strong R&D"], weaknesses: ["Small team", "Funding concerns"] },
    { name: "CloudBase", marketShare: "12%", revenue: "$120M", strengths: ["Enterprise focus", "Stable revenue"], weaknesses: ["Legacy tech", "Slow growth"] }
  ],
  revenueForecast: [
    { month: "Jan", actual: 120000, forecast: 120000 },
    { month: "Feb", actual: 135000, forecast: 138000 },
    { month: "Mar", actual: 142000, forecast: 145000 },
    { month: "Apr", actual: 158000, forecast: 162000 },
    { month: "May", actual: 175000, forecast: 178000 },
    { month: "Jun", actual: 189000, forecast: 195000 },
    { month: "Jul", forecast: 208000 },
    { month: "Aug", forecast: 222000 },
    { month: "Sep", forecast: 238000 },
    { month: "Oct", forecast: 255000 },
    { month: "Nov", forecast: 273000 },
    { month: "Dec", forecast: 292000 }
  ],
  financialComparison: [
    { category: "Revenue", yourCompany: 189000, industryAvg: 165000, topPerformer: 245000 },
    { category: "Growth Rate", yourCompany: 18.5, industryAvg: 12.3, topPerformer: 25.8 },
    { category: "Profit Margin", yourCompany: 22.4, industryAvg: 18.7, topPerformer: 28.9 },
    { category: "Customer Acquisition", yourCompany: 450, industryAvg: 320, topPerformer: 680 },
    { category: "Market Share", yourCompany: 8.5, industryAvg: 6.2, topPerformer: 15.3 }
  ],
  marketSegments: [
    { name: "Enterprise", value: 45, color: "#4f62ff" },
    { name: "Mid-Market", value: 30, color: "#7c3aed" },
    { name: "Small Business", value: 20, color: "#06b6d4" },
    { name: "Startup", value: 5, color: "#10b981" }
  ]
};

export default function DashboardPage() {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [data, setData] = useState(fallbackData);

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const fetchDashboardData = async () => {
    try {
      setLoading(true);
      setError(null);
      const dashboardData = await getDashboardData();
      setData(dashboardData);
    } catch (err: any) {
      console.error('Failed to fetch dashboard data:', err);
      setError(err?.message || 'Failed to load dashboard data');
      // Keep fallback data on error
    } finally {
      setLoading(false);
    }
  };

  const refetchData = () => {
    fetchDashboardData();
  };

  const getScoreColor = (score: number) => {
    if (score >= 80) return "text-emerald-400";
    if (score >= 60) return "text-yellow-400";
    return "text-red-400";
  };

  const getScoreBg = (score: number) => {
    if (score >= 80) return "bg-emerald-500/20 border-emerald-500/30";
    if (score >= 60) return "bg-yellow-500/20 border-yellow-500/30";
    return "bg-red-500/20 border-red-500/30";
  };

  const getTrendIcon = (current: number, average: number) => {
    if (current > average * 1.1) return <ArrowUp className="w-4 h-4 text-emerald-400" />;
    if (current < average * 0.9) return <ArrowDown className="w-4 h-4 text-red-400" />;
    return <Minus className="w-4 h-4 text-yellow-400" />;
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-[60vh]">
        <div className="text-center">
          <Loader2 className="w-12 h-12 animate-spin text-brand-400 mx-auto mb-4" />
          <p className="text-slate-400">Loading dashboard data...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-7xl mx-auto animate-fade-in">
      {/* Header */}
      <div className="mb-8">
        <div className="flex items-center justify-between mb-4">
          <div>
            <h1 className="text-3xl font-bold text-white mb-2">Business Intelligence Dashboard</h1>
            <p className="text-slate-400">Real-time insights and performance metrics</p>
            {error && (
              <div className="mt-2 flex items-center gap-2">
                <AlertCircle className="w-4 h-4 text-yellow-400" />
                <p className="text-yellow-400 text-sm">Using cached data - {error}</p>
                <button 
                  onClick={refetchData}
                  className="text-xs text-brand-400 hover:text-brand-300 font-medium underline"
                >
                  Retry
                </button>
              </div>
            )}
          </div>
          <div className="text-right">
            <p className="text-sm text-slate-500">Last updated</p>
            <p className="text-white font-medium">{new Date().toLocaleString()}</p>
          </div>
        </div>
      </div>

      {/* Startup Score Card */}
      <div className="mb-8">
        <div className={`glass rounded-3xl p-8 border ${getScoreBg(data.score)} relative overflow-hidden`}>
          <div className="absolute top-0 right-0 w-32 h-32 bg-brand-500/10 rounded-full blur-3xl"></div>
          <div className="flex items-center justify-between relative z-10">
            <div>
              <h2 className="text-2xl font-bold text-white mb-2">Startup Validation Score</h2>
              <p className="text-slate-300 mb-4">Overall business health and market readiness</p>
              <div className="flex items-center gap-4">
                <div className="flex items-center gap-2">
                  <Star className="w-5 h-5 text-yellow-400" />
                  <span className="text-white font-medium">AI-Powered Analysis</span>
                </div>
                <div className="flex items-center gap-2">
                  <CheckCircle2 className="w-5 h-5 text-emerald-400" />
                  <span className="text-white font-medium">Live Data</span>
                </div>
              </div>
            </div>
            <div className="text-center">
              <div className={`text-6xl font-bold ${getScoreColor(data.score)} mb-2`}>
                {data.score}
              </div>
              <p className="text-slate-300 text-sm">out of 100</p>
              <div className="mt-3 px-3 py-1 rounded-full bg-white/10 inline-block">
                <span className={`text-sm font-medium ${getScoreColor(data.score)}`}>
                  {data.score >= 80 ? 'Strong Go' : data.score >= 60 ? 'Go' : 'Conditional'}
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Market Analysis Summary */}
      <div className="mb-8">
        <h2 className="text-xl font-bold text-white mb-4 flex items-center gap-2">
          <Globe className="w-5 h-5 text-brand-400" />
          Market Analysis Summary
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          <div className="glass rounded-2xl p-5 border border-white/5">
            <div className="flex items-center gap-3 mb-2">
              <DollarSign className="w-5 h-5 text-emerald-400" />
              <p className="text-slate-400 text-sm">Market Size</p>
            </div>
            <p className="text-2xl font-bold text-white">{data.marketAnalysis.marketSize}</p>
          </div>
          <div className="glass rounded-2xl p-5 border border-white/5">
            <div className="flex items-center gap-3 mb-2">
              <TrendingUp className="w-5 h-5 text-blue-400" />
              <p className="text-slate-400 text-sm">Growth Rate</p>
            </div>
            <p className="text-2xl font-bold text-white">{data.marketAnalysis.growthRate}</p>
          </div>
          <div className="glass rounded-2xl p-5 border border-white/5">
            <div className="flex items-center gap-3 mb-2">
              <AlertCircle className="w-5 h-5 text-yellow-400" />
              <p className="text-slate-400 text-sm">Competition</p>
            </div>
            <p className="text-2xl font-bold text-white">{data.marketAnalysis.competitionLevel}</p>
          </div>
          <div className="glass rounded-2xl p-5 border border-white/5">
            <div className="flex items-center gap-3 mb-2">
              <Target className="w-5 h-5 text-purple-400" />
              <p className="text-slate-400 text-sm">Opportunity Score</p>
            </div>
            <p className="text-2xl font-bold text-white">{data.marketAnalysis.opportunityScore}</p>
          </div>
        </div>
      </div>

      {/* Competitor List */}
      <div className="mb-8">
        <h2 className="text-xl font-bold text-white mb-4 flex items-center gap-2">
          <Building className="w-5 h-5 text-brand-400" />
          Competitor Analysis
        </h2>
        <div className="glass rounded-3xl p-6 border border-white/5">
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead>
                <tr className="border-b border-white/10">
                  <th className="text-left py-3 px-4 text-slate-400 font-medium">Company</th>
                  <th className="text-left py-3 px-4 text-slate-400 font-medium">Market Share</th>
                  <th className="text-left py-3 px-4 text-slate-400 font-medium">Revenue</th>
                  <th className="text-left py-3 px-4 text-slate-400 font-medium">Strengths</th>
                  <th className="text-left py-3 px-4 text-slate-400 font-medium">Weaknesses</th>
                </tr>
              </thead>
              <tbody>
                {data.competitors.map((competitor, index) => (
                  <tr key={index} className="border-b border-white/5 hover:bg-white/5 transition-colors">
                    <td className="py-4 px-4">
                      <div className="flex items-center gap-2">
                        <div className="w-8 h-8 rounded-lg bg-brand-500/20 flex items-center justify-center">
                          <Building className="w-4 h-4 text-brand-400" />
                        </div>
                        <span className="text-white font-medium">{competitor.name}</span>
                      </div>
                    </td>
                    <td className="py-4 px-4">
                      <span className="text-white font-medium">{competitor.marketShare}</span>
                    </td>
                    <td className="py-4 px-4">
                      <span className="text-white font-medium">{competitor.revenue}</span>
                    </td>
                    <td className="py-4 px-4">
                      <div className="flex flex-wrap gap-1">
                        {competitor.strengths.map((strength, i) => (
                          <span key={i} className="px-2 py-1 bg-emerald-500/20 text-emerald-400 text-xs rounded-full">
                            {strength}
                          </span>
                        ))}
                      </div>
                    </td>
                    <td className="py-4 px-4">
                      <div className="flex flex-wrap gap-1">
                        {competitor.weaknesses.map((weakness, i) => (
                          <span key={i} className="px-2 py-1 bg-red-500/20 text-red-400 text-xs rounded-full">
                            {weakness}
                          </span>
                        ))}
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>

      {/* Charts Section */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
        {/* Revenue Forecast Chart */}
        <div className="glass rounded-3xl p-6 border border-white/5">
          <h3 className="text-lg font-bold text-white mb-4 flex items-center gap-2">
            <LineChart className="w-5 h-5 text-emerald-400" />
            Revenue Forecast
          </h3>
          <ResponsiveContainer width="100%" height={300}>
            <RechartsLineChart data={data.revenueForecast}>
              <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
              <XAxis dataKey="month" stroke="#9CA3AF" />
              <YAxis stroke="#9CA3AF" />
              <Tooltip 
                contentStyle={{ backgroundColor: '#1F2937', border: '1px solid #374151' }}
                labelStyle={{ color: '#F3F4F6' }}
              />
              <Legend />
              <Line 
                type="monotone" 
                dataKey="actual" 
                stroke="#10B981" 
                strokeWidth={2}
                name="Actual"
                dot={{ fill: '#10B981' }}
              />
              <Line 
                type="monotone" 
                dataKey="forecast" 
                stroke="#4F62FF" 
                strokeWidth={2}
                strokeDasharray="5 5"
                name="Forecast"
                dot={{ fill: '#4F62FF' }}
              />
            </RechartsLineChart>
          </ResponsiveContainer>
        </div>

        {/* Market Segments Pie Chart */}
        <div className="glass rounded-3xl p-6 border border-white/5">
          <h3 className="text-lg font-bold text-white mb-4 flex items-center gap-2">
            <PieChart className="w-5 h-5 text-purple-400" />
            Market Segments
          </h3>
          <ResponsiveContainer width="100%" height={300}>
            <RechartsPieChart>
              <Pie
                data={data.marketSegments}
                cx="50%"
                cy="50%"
                labelLine={false}
                label={({ name, value }) => `${name}: ${value}%`}
                outerRadius={80}
                fill="#8884d8"
                dataKey="value"
              >
                {data.marketSegments.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={entry.color} />
                ))}
              </Pie>
              <Tooltip 
                contentStyle={{ backgroundColor: '#1F2937', border: '1px solid #374151' }}
                labelStyle={{ color: '#F3F4F6' }}
              />
            </RechartsPieChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Financial Comparison Chart */}
      <div className="glass rounded-3xl p-6 border border-white/5">
        <h3 className="text-lg font-bold text-white mb-4 flex items-center gap-2">
          <BarChart3 className="w-5 h-5 text-blue-400" />
          Financial Comparison vs Industry
        </h3>
        <ResponsiveContainer width="100%" height={350}>
          <RechartsBarChart data={data.financialComparison}>
            <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
            <XAxis dataKey="category" stroke="#9CA3AF" />
            <YAxis stroke="#9CA3AF" />
            <Tooltip 
              contentStyle={{ backgroundColor: '#1F2937', border: '1px solid #374151' }}
              labelStyle={{ color: '#F3F4F6' }}
            />
            <Legend />
            <Bar dataKey="yourCompany" fill="#4F62FF" name="Your Company" />
            <Bar dataKey="industryAvg" fill="#6B7280" name="Industry Average" />
            <Bar dataKey="topPerformer" fill="#10B981" name="Top Performer" />
          </RechartsBarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
