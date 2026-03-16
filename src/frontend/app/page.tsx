import Link from "next/link";
import { Lightbulb, FileText, TrendingUp, Zap, Shield, BarChart3 } from "lucide-react";

const features = [
  {
    icon: Lightbulb,
    title: "Startup Idea Validator",
    description:
      "Multi-agent AI pipeline validates your startup idea with market research, competitor analysis, and risk scoring.",
    href: "/startup",
    color: "from-brand-500 to-purple-600",
    glow: "shadow-glow-brand",
    badge: "4 AI Agents",
  },
  {
    icon: FileText,
    title: "Financial Report Analyzer",
    description:
      "Upload any financial PDF. Our AI extracts revenue, margins, EPS, cash flows, and produces a full narrative analysis.",
    href: "/reports",
    color: "from-emerald-500 to-teal-600",
    glow: "shadow-glow-green",
    badge: "PyMuPDF + GPT-4o",
  },
  {
    icon: TrendingUp,
    title: "Financial Forecasting Engine",
    description:
      "Input historical data and get ML-powered forecasts with confidence intervals and an LLM-generated interpretation.",
    href: "/dashboard",
    color: "from-orange-500 to-pink-600",
    glow: "",
    badge: "Scikit-learn + LLM",
  },
];

const stats = [
  { label: "AI Agents", value: "6", icon: Zap },
  { label: "ML Models", value: "2", icon: BarChart3 },
  { label: "Analysis Modes", value: "3", icon: Shield },
];

export default function HomePage() {
  return (
    <div className="min-h-full animate-fade-in">
      {/* Hero */}
      <div className="mb-12">
        <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-brand-600/20 border border-brand-500/30 text-brand-300 text-xs font-medium mb-4">
          <Zap className="w-3 h-3" />
          Powered by GPT-4o + LangGraph
        </div>
        <h1 className="text-4xl font-bold text-white mb-4">
          AI Business Intelligence{" "}
          <span className="gradient-text">Platform</span>
        </h1>
        <p className="text-slate-400 text-lg max-w-2xl">
          A production-grade multi-agent platform for startup validation, financial
          document analysis, and intelligent forecasting — all in one unified dashboard.
        </p>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-3 gap-4 mb-12">
        {stats.map(({ label, value, icon: Icon }) => (
          <div key={label} className="glass rounded-2xl p-5 card-hover">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-xl bg-brand-500/20 flex items-center justify-center">
                <Icon className="w-5 h-5 text-brand-400" />
              </div>
              <div>
                <p className="text-2xl font-bold text-white">{value}</p>
                <p className="text-xs text-slate-400">{label}</p>
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Feature Cards */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {features.map(({ icon: Icon, title, description, href, color, glow, badge }) => (
          <Link key={href} href={href} className="group">
            <div
              className={`glass rounded-2xl p-6 h-full card-hover border border-surface-border group-hover:border-brand-500/40 transition-all duration-300`}
            >
              {/* Icon */}
              <div
                className={`w-12 h-12 rounded-2xl bg-gradient-to-br ${color} flex items-center justify-center mb-4 ${glow}`}
              >
                <Icon className="w-6 h-6 text-white" />
              </div>

              {/* Badge */}
              <span className="inline-block px-2 py-0.5 rounded-md bg-white/5 text-slate-400 text-xs font-mono mb-3">
                {badge}
              </span>

              <h2 className="text-lg font-bold text-white mb-2 group-hover:text-brand-300 transition-colors">
                {title}
              </h2>
              <p className="text-slate-400 text-sm leading-relaxed">{description}</p>

              <div className="mt-4 flex items-center text-brand-400 text-sm font-medium opacity-0 group-hover:opacity-100 transition-opacity">
                Open module →
              </div>
            </div>
          </Link>
        ))}
      </div>

      {/* Pipeline Diagram */}
      <div className="mt-12 glass rounded-2xl p-6 border border-surface-border">
        <h3 className="text-sm font-semibold text-slate-300 mb-4 uppercase tracking-wider">
          Agent Pipeline — Startup Validator
        </h3>
        <div className="flex items-center gap-2 overflow-x-auto pb-2">
          {["Market Research", "Competitor Analysis", "Decision Synthesis"].map(
            (step, i, arr) => (
              <div key={step} className="flex items-center gap-2 flex-shrink-0">
                <div className="px-4 py-2 rounded-xl bg-brand-600/20 border border-brand-500/30 text-brand-300 text-sm font-medium">
                  {step}
                </div>
                {i < arr.length - 1 && (
                  <div className="text-slate-600 text-lg">→</div>
                )}
              </div>
            )
          )}
        </div>
      </div>
    </div>
  );
}
