"use client";

import { useState, useRef } from 'react';
import { analyzeFinancialReport } from '@/services/api';
import { FinancialReportResponse } from '@/types';
import { 
  FileText, 
  Upload, 
  DollarSign, 
  TrendingUp, 
  TrendingDown,
  BarChart3,
  PieChart,
  Calculator,
  Eye,
  Download,
  AlertTriangle,
  CheckCircle2,
  Loader2,
  X,
  FileSpreadsheet,
  FileImage,
  Search,
  Filter
} from 'lucide-react';

type LoadingState = "idle" | "uploading" | "analyzing" | "success" | "error";

export default function FinancialReportAnalyzer() {
  const [file, setFile] = useState<File | null>(null);
  const [dragActive, setDragActive] = useState(false);
  const [state, setState] = useState<LoadingState>("idle");
  const [result, setResult] = useState<FinancialReportResponse | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [selectedMetric, setSelectedMetric] = useState<string | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleDrag = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true);
    } else if (e.type === "dragleave") {
      setDragActive(false);
    }
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFile(e.dataTransfer.files[0]);
    }
  };

  const handleFile = (file: File) => {
    // Only PDF files are supported by the backend
    if (file.type !== "application/pdf" && file.type !== "application/octet-stream") {
      setError('Please upload a PDF file');
      return;
    }
    
    if (file.size > 20 * 1024 * 1024) {
      setError('File size must be less than 20MB');
      return;
    }
    
    setFile(file);
    setError(null);
  };

  const analyzeReport = async () => {
    if (!file) return;
    
    setState("analyzing");
    setError(null);
    
    try {
      const analysisResult = await analyzeFinancialReport(file) as any;
      setResult(analysisResult);
      setState("success");
    } catch (err: any) {
      setError(
        err?.response?.data?.detail || "Analysis failed. Please try again."
      );
      setState("error");
    }
  };

  const formatCurrency = (value: number | string | undefined) => {
    if (!value) return 'N/A';
    const num = typeof value === 'string' ? parseFloat(value.replace(/[^0-9.-]/g, '')) : value;
    if (isNaN(num)) return 'N/A';
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
      minimumFractionDigits: 0,
      maximumFractionDigits: 0
    }).format(num);
  };

  const formatPercent = (value: number | string | undefined) => {
    if (!value) return 'N/A';
    const num = typeof value === 'string' ? parseFloat(value.replace(/[^0-9.-]/g, '')) : value;
    if (isNaN(num)) return 'N/A';
    return `${num.toFixed(1)}%`;
  };

  const parseMetricValue = (value: string | number | undefined): number => {
    if (!value) return 0;
    const num = typeof value === 'string' ? parseFloat(value.replace(/[^0-9.-]/g, '')) : value;
    return isNaN(num) ? 0 : num;
  };

  const getFileIcon = (type: string) => {
    if (type.includes('pdf')) return <FileText className="w-8 h-8 text-red-400" />;
    if (type.includes('spreadsheet') || type.includes('excel')) return <FileSpreadsheet className="w-8 h-8 text-green-400" />;
    if (type.includes('image')) return <FileImage className="w-8 h-8 text-blue-400" />;
    return <FileText className="w-8 h-8 text-gray-400" />;
  };

  const MetricCard = ({ title, value, subtitle, change, status }: {
    title: string;
    value: string;
    subtitle?: string;
    change?: number;
    status?: 'good' | 'warning' | 'critical';
  }) => (
    <div className="bg-white/10 backdrop-blur-lg rounded-xl p-6 border border-white/20">
      <div className="flex items-center justify-between mb-2">
        <DollarSign className="w-5 h-5 text-green-400" />
        {change && (
          <span className={`text-sm ${change >= 0 ? 'text-green-400' : 'text-red-400'}`}>
            {change >= 0 ? '+' : ''}{change.toFixed(1)}%
          </span>
        )}
      </div>
      <p className="text-2xl font-bold text-white mb-1">{value}</p>
      <p className="text-gray-400 text-sm">{title}</p>
      {subtitle && <p className="text-gray-500 text-xs">{subtitle}</p>}
    </div>
  );

  return (
    <div className="space-y-8">
      {/* Upload Section */}
      <div className="bg-white/10 backdrop-blur-lg rounded-2xl p-8 border border-white/20">
        <div className="flex items-center space-x-3 mb-6">
          <div className="p-3 bg-green-500/20 rounded-xl">
            <Calculator className="w-6 h-6 text-green-400" />
          </div>
          <div>
            <h2 className="text-2xl font-bold text-white">Financial Report Analyzer</h2>
            <p className="text-gray-300">Upload financial documents for AI-powered analysis and insights</p>
          </div>
        </div>

        {/* File Upload Area */}
        <div
          className={`relative border-2 border-dashed rounded-xl p-8 text-center transition-colors ${
            dragActive 
              ? 'border-green-400 bg-green-500/10' 
              : 'border-white/20 hover:border-white/30 bg-white/5'
          }`}
          onDragEnter={handleDrag}
          onDragLeave={handleDrag}
          onDragOver={handleDrag}
          onDrop={handleDrop}
        >
          <input
            ref={fileInputRef}
            type="file"
            className="hidden"
            accept=".pdf"
            onChange={(e) => e.target.files && handleFile(e.target.files[0])}
          />
          
          {file ? (
            <div className="space-y-4">
              <div className="flex items-center justify-center space-x-3">
                {getFileIcon(file.type)}
                <div>
                  <p className="text-white font-medium">{file.name}</p>
                  <p className="text-gray-400 text-sm">{(file.size / 1024 / 1024).toFixed(2)} MB</p>
                </div>
              </div>
              <div className="flex justify-center space-x-3">
                <button
                  onClick={() => fileInputRef.current?.click()}
                  className="px-4 py-2 bg-white/10 text-white rounded-lg hover:bg-white/20 transition-colors"
                >
                  Change File
                </button>
                <button
                  onClick={() => {
                    setFile(null);
                    setResult(null);
                    setState("idle");
                  }}
                  className="px-4 py-2 bg-red-500/20 text-red-400 rounded-lg hover:bg-red-500/30 transition-colors"
                >
                  Remove
                </button>
              </div>
            </div>
          ) : (
            <div className="space-y-4">
              <Upload className="w-12 h-12 text-gray-400 mx-auto" />
              <div>
                <p className="text-white font-medium mb-2">
                  Drag and drop your financial report here
                </p>
                <p className="text-gray-400 text-sm mb-4">
                  Supports PDF files up to 20MB
                </p>
                <button
                  onClick={() => fileInputRef.current?.click()}
                  className="px-6 py-2 bg-gradient-to-r from-green-600 to-blue-600 text-white rounded-lg hover:from-green-700 hover:to-blue-700 transition-all"
                >
                  Browse Files
                </button>
              </div>
            </div>
          )}
        </div>

        {error && (
          <div className="mt-4 bg-red-500/20 border border-red-500/50 rounded-xl p-4 text-red-200">
            {error}
          </div>
        )}

        {file && state === "idle" && (
          <button
            onClick={analyzeReport}
            className="mt-6 w-full bg-gradient-to-r from-green-600 to-blue-600 text-white font-semibold py-3 px-6 rounded-xl hover:from-green-700 hover:to-blue-700 focus:outline-none focus:ring-2 focus:ring-green-500 focus:ring-offset-2 focus:ring-offset-transparent transition-all flex items-center justify-center space-x-2"
          >
            <BarChart3 className="w-5 h-5" />
            <span>Analyze Financial Report</span>
          </button>
        )}

        {state === "analyzing" && (
          <div className="mt-6 text-center">
            <Loader2 className="w-8 h-8 text-green-400 animate-spin mx-auto mb-3" />
            <p className="text-white font-medium">Analyzing financial data...</p>
            <p className="text-gray-400 text-sm">This may take a few moments</p>
          </div>
        )}
      </div>

      {/* Analysis Results */}
      {result && state === "success" && (
        <div className="space-y-6 animate-fade-in">
          {/* Summary Cards */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-4">
            <MetricCard 
              title="Total Revenue" 
              value={formatCurrency(result.summary?.total_revenue || result.metrics?.revenue)}
            />
            <MetricCard 
              title="Net Profit" 
              value={formatCurrency(result.summary?.net_profit || result.metrics?.net_profit)}
            />
            <MetricCard 
              title="Total Assets" 
              value={formatCurrency(result.metrics?.total_assets)}
            />
            <MetricCard 
              title="Profit Margin" 
              value={formatPercent(result.summary?.profit_margin || result.metrics?.net_margin)}
            />
            <MetricCard 
              title="Growth Rate" 
              value={formatPercent(result.summary?.growth_rate || result.metrics?.revenue_growth_yoy)}
            />
          </div>

          {/* Key Metrics */}
          <div className="bg-white/10 backdrop-blur-lg rounded-2xl p-8 border border-white/20">
            <div className="flex items-center space-x-3 mb-6">
              <Calculator className="w-6 h-6 text-green-400" />
              <h3 className="text-xl font-bold text-white">Key Financial Metrics</h3>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {Object.entries(result.metrics).map(([key, value]) => (
                <div
                  key={key}
                  className="bg-white/5 rounded-xl p-4 border border-white/10 hover:bg-white/10 transition-colors cursor-pointer"
                  onClick={() => setSelectedMetric(key === selectedMetric ? null : key)}
                >
                  <div className="text-lg font-semibold text-white mb-1 capitalize">
                    {key.replace(/_/g, ' ')}
                  </div>
                  <div className="text-2xl font-bold text-white mb-1">
                    {key.includes('margin') || key.includes('ratio') || key.includes('growth') 
                      ? formatPercent(value)
                      : formatCurrency(value)
                    }
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* AI Analysis */}
          <div className="bg-white/10 backdrop-blur-lg rounded-2xl p-8 border border-white/20">
            <div className="flex items-center space-x-3 mb-6">
              <Eye className="w-6 h-6 text-purple-400" />
              <h3 className="text-xl font-bold text-white">AI Financial Analysis</h3>
            </div>
            <div className="prose prose-invert max-w-none">
              <p className="text-gray-300 leading-relaxed whitespace-pre-line">
                {result.analysis}
              </p>
            </div>
          </div>

          {/* Key Highlights */}
          {result.key_highlights && result.key_highlights.length > 0 && (
            <div className="bg-white/10 backdrop-blur-lg rounded-2xl p-8 border border-green-500/20">
              <div className="flex items-center space-x-3 mb-6">
                <CheckCircle2 className="w-6 h-6 text-green-400" />
                <h3 className="text-xl font-bold text-white">Key Highlights</h3>
              </div>
              <ul className="space-y-3">
                {result.key_highlights.map((highlight, index) => (
                  <li key={index} className="flex items-start space-x-2">
                    <span className="text-green-500 mt-1">•</span>
                    <span className="text-gray-300">{highlight}</span>
                  </li>
                ))}
              </ul>
            </div>
          )}

          {/* Key Risks */}
          {result.key_risks && result.key_risks.length > 0 && (
            <div className="bg-white/10 backdrop-blur-lg rounded-2xl p-8 border border-red-500/20">
              <div className="flex items-center space-x-3 mb-6">
                <AlertTriangle className="w-6 h-6 text-red-400" />
                <h3 className="text-xl font-bold text-white">Key Risks</h3>
              </div>
              <ul className="space-y-3">
                {result.key_risks.map((risk, index) => (
                  <li key={index} className="flex items-start space-x-2">
                    <span className="text-red-500 mt-1">•</span>
                    <span className="text-gray-300">{risk}</span>
                  </li>
                ))}
              </ul>
            </div>
          )}

          {/* Document Info */}
          <div className="bg-white/10 backdrop-blur-lg rounded-2xl p-6 border border-white/20">
            <div className="flex items-center justify-between">
              <div>
                <h3 className="text-lg font-semibold text-white">Document Information</h3>
                <p className="text-gray-400 text-sm">
                  {result.page_count} pages processed • {result.raw_text_length} characters analyzed
                </p>
              </div>
              <div className="flex space-x-3">
                <button className="flex items-center space-x-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors">
                  <Download className="w-4 h-4" />
                  <span>Download Report</span>
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
