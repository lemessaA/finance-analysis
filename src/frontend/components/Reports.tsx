"use client";

import { useState, useEffect } from 'react';
import { 
  FileText, 
  Download, 
  Eye, 
  Calendar, 
  Filter,
  Search,
  BarChart3,
  Lightbulb,
  Brain,
  LineChart,
  TrendingUp,
  Target,
  Shield,
  CheckCircle2,
  AlertTriangle,
  X,
  Loader2,
  Trash2
} from 'lucide-react';
import { StartupValidationResponse, MarketIntelligenceResponse, ForecastResponse, FinancialReportResponse } from '@/types';

interface Report {
  id: string;
  type: 'startup' | 'market' | 'forecasting' | 'analyzer';
  title: string;
  description: string;
  score?: number;
  status: 'completed' | 'processing' | 'failed';
  createdAt: string;
  data?: StartupValidationResponse | MarketIntelligenceResponse | ForecastResponse | FinancialReportResponse;
}

export default function Reports() {
  const [reports, setReports] = useState<Report[]>([]);
  const [selectedReport, setSelectedReport] = useState<Report | null>(null);
  const [filter, setFilter] = useState<'all' | 'startup' | 'market' | 'forecasting' | 'analyzer'>('all');
  const [searchTerm, setSearchTerm] = useState('');
  const [showDeleteModal, setShowDeleteModal] = useState(false);
  const [reportToDelete, setReportToDelete] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  // Load reports from localStorage on component mount
  useEffect(() => {
    loadReportsFromStorage();
  }, []);

  const loadReportsFromStorage = () => {
    try {
      const storedReports = localStorage.getItem('analysisReports');
      if (storedReports) {
        const parsedReports = JSON.parse(storedReports);
        setReports(parsedReports);
      }
    } catch (error) {
      console.error('Error loading reports from storage:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const saveReportsToStorage = (reportsToSave: Report[]) => {
    try {
      localStorage.setItem('analysisReports', JSON.stringify(reportsToSave));
    } catch (error) {
      console.error('Error saving reports to storage:', error);
    }
  };

  // Function to add a new report (can be called by other components)
  const addReport = (report: Omit<Report, 'id' | 'createdAt'>) => {
    const newReport: Report = {
      ...report,
      id: Date.now().toString(),
      createdAt: new Date().toISOString(),
    };
    
    const updatedReports = [newReport, ...reports];
    setReports(updatedReports);
    saveReportsToStorage(updatedReports);
  };

  const getTypeIcon = (type: string) => {
    switch (type) {
      case 'startup': return <Lightbulb className="w-5 h-5" />;
      case 'market': return <LineChart className="w-5 h-5" />;
      case 'forecasting': return <Brain className="w-5 h-5" />;
      case 'analyzer': return <BarChart3 className="w-5 h-5" />;
      default: return <FileText className="w-5 h-5" />;
    }
  };

  const getTypeColor = (type: string) => {
    switch (type) {
      case 'startup': return 'bg-purple-500/20 text-purple-400 border-purple-500/30';
      case 'market': return 'bg-blue-500/20 text-blue-400 border-blue-500/30';
      case 'forecasting': return 'bg-green-500/20 text-green-400 border-green-500/30';
      case 'analyzer': return 'bg-orange-500/20 text-orange-400 border-orange-500/30';
      default: return 'bg-gray-500/20 text-gray-400 border-gray-500/30';
    }
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'completed': return <CheckCircle2 className="w-4 h-4 text-green-400" />;
      case 'processing': return <Loader2 className="w-4 h-4 text-yellow-400 animate-spin" />;
      case 'failed': return <AlertTriangle className="w-4 h-4 text-red-400" />;
      default: return <Shield className="w-4 h-4 text-gray-400" />;
    }
  };

  const filteredReports = reports.filter(report => {
    const matchesFilter = filter === 'all' || report.type === filter;
    const matchesSearch = report.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         report.description.toLowerCase().includes(searchTerm.toLowerCase());
    return matchesFilter && matchesSearch;
  });

  const handleDeleteReport = (id: string) => {
    setReportToDelete(id);
    setShowDeleteModal(true);
  };

  const confirmDelete = () => {
    if (reportToDelete) {
      const updatedReports = reports.filter(r => r.id !== reportToDelete);
      setReports(updatedReports);
      saveReportsToStorage(updatedReports);
      setShowDeleteModal(false);
      setReportToDelete(null);
    }
  };

  const downloadReport = (report: Report) => {
    const reportData = {
      ...report,
      downloadedAt: new Date().toISOString(),
      version: '1.0'
    };
    
    const blob = new Blob([JSON.stringify(reportData, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `${report.title.replace(/\s+/g, '_')}_report.json`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', { 
      month: 'short', 
      day: 'numeric', 
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  const getReportScore = (report: Report) => {
    if (report.score) return report.score;
    
    if (!report.data) return null;
    
    switch (report.type) {
      case 'startup':
        return (report.data as StartupValidationResponse)?.overall_score;
      case 'forecasting':
        const forecastData = report.data as ForecastResponse;
        return forecastData.r_squared ? Math.round(forecastData.r_squared * 100) : null;
      default:
        return null;
    }
  };

  const ReportDetailModal = ({ report, onClose }: { report: Report; onClose: () => void }) => {
    if (!report.data) return null;

    const renderReportContent = () => {
      switch (report.type) {
        case 'startup':
          const startupData = report.data as StartupValidationResponse;
          return (
            <div className="space-y-6">
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
                <div className="bg-white/5 rounded-xl p-4">
                  <p className="text-sm text-gray-400 mb-1">Overall Score</p>
                  <p className="text-xl font-bold text-white">{startupData.overall_score}/100</p>
                </div>
                <div className="bg-white/5 rounded-xl p-4">
                  <p className="text-sm text-gray-400 mb-1">Market Score</p>
                  <p className="text-xl font-bold text-white">{startupData.market_score}/100</p>
                </div>
                <div className="bg-white/5 rounded-xl p-4">
                  <p className="text-sm text-gray-400 mb-1">Competition</p>
                  <p className="text-xl font-bold text-white">{startupData.competition_score}/100</p>
                </div>
                <div className="bg-white/5 rounded-xl p-4">
                  <p className="text-sm text-gray-400 mb-1">Risk Score</p>
                  <p className="text-xl font-bold text-white">{startupData.risk_score}/100</p>
                </div>
              </div>

              <div className="bg-white/5 rounded-xl p-4">
                <p className="text-sm text-gray-400 mb-2">Verdict</p>
                <p className="text-lg font-medium text-white">{startupData.verdict}</p>
              </div>

              {startupData.executive_summary && (
                <div>
                  <p className="text-sm text-gray-400 mb-3">Executive Summary</p>
                  <p className="text-gray-300">{startupData.executive_summary}</p>
                </div>
              )}

              <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                <div>
                  <p className="text-sm text-gray-400 mb-3">Key Strengths</p>
                  <ul className="space-y-2">
                    {startupData.key_strengths.map((strength, i) => (
                      <li key={i} className="flex items-start space-x-2">
                        <span className="text-green-500 mt-1">•</span>
                        <span className="text-gray-300">{strength}</span>
                      </li>
                    ))}
                  </ul>
                </div>
                <div>
                  <p className="text-sm text-gray-400 mb-3">Key Risks</p>
                  <ul className="space-y-2">
                    {startupData.key_risks.map((risk, i) => (
                      <li key={i} className="flex items-start space-x-2">
                        <span className="text-red-500 mt-1">•</span>
                        <span className="text-gray-300">{risk}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              </div>
            </div>
          );

        case 'market':
          const marketData = report.data as MarketIntelligenceResponse;
          return (
            <div className="space-y-6">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div className="bg-white/5 rounded-xl p-4">
                  <p className="text-sm text-gray-400 mb-1">Market Size</p>
                  <p className="text-xl font-bold text-white">{marketData.market_size_estimate}</p>
                </div>
                <div className="bg-white/5 rounded-xl p-4">
                  <p className="text-sm text-gray-400 mb-1">CAGR</p>
                  <p className="text-xl font-bold text-white">{marketData.cagr_estimate}</p>
                </div>
              </div>

              <div>
                <p className="text-sm text-gray-400 mb-3">Market Overview</p>
                <p className="text-gray-300">{marketData.market_overview}</p>
              </div>

              <div>
                <p className="text-sm text-gray-400 mb-3">Key Trends</p>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-2">
                  {marketData.key_trends.map((trend, i) => (
                    <div key={i} className="bg-white/5 rounded-lg p-3">
                      <span className="text-gray-300">{trend}</span>
                    </div>
                  ))}
                </div>
              </div>

              <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                <div>
                  <p className="text-sm text-gray-400 mb-3">Opportunities</p>
                  <ul className="space-y-2">
                    {marketData.opportunities.map((opp, i) => (
                      <li key={i} className="flex flex-col space-y-1">
                        <div className="flex items-start space-x-2">
                          <span className="text-green-500 mt-1">•</span>
                          <span className="text-white font-medium">{opp.title}</span>
                        </div>
                        <p className="text-gray-400 text-xs ml-5">{opp.description}</p>
                      </li>
                    ))}
                  </ul>
                </div>
                <div>
                  <p className="text-sm text-gray-400 mb-3">Risks</p>
                  <ul className="space-y-2">
                    {marketData.risks.map((risk, i) => (
                      <li key={i} className="flex items-start space-x-2">
                        <span className="text-red-500 mt-1">•</span>
                        <span className="text-gray-300">{risk}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              </div>
            </div>
          );

        case 'forecasting':
          const forecastData = report.data as ForecastResponse;
          return (
            <div className="space-y-6">
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
                <div className="bg-white/5 rounded-xl p-4">
                  <p className="text-sm text-gray-400 mb-1">Metric</p>
                  <p className="text-xl font-bold text-white">{forecastData.metric}</p>
                </div>
                <div className="bg-white/5 rounded-xl p-4">
                  <p className="text-sm text-gray-400 mb-1">Model</p>
                  <p className="text-xl font-bold text-white">{forecastData.model_used}</p>
                </div>
                <div className="bg-white/5 rounded-xl p-4">
                  <p className="text-sm text-gray-400 mb-1">R² Score</p>
                  <p className="text-xl font-bold text-white">{forecastData.r_squared.toFixed(3)}</p>
                </div>
                <div className="bg-white/5 rounded-xl p-4">
                  <p className="text-sm text-gray-400 mb-1">Confidence</p>
                  <p className="text-xl font-bold text-white">{forecastData.confidence}</p>
                </div>
              </div>

              <div className="bg-white/5 rounded-xl p-4">
                <p className="text-sm text-gray-400 mb-2">Growth Rate</p>
                <p className="text-2xl font-bold text-white">{(forecastData.avg_growth_rate * 100).toFixed(1)}%</p>
              </div>

              <div>
                <p className="text-sm text-gray-400 mb-3">Forecast Values</p>
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                  {forecastData.data_points.filter(p => p.is_forecast).map((point, i) => (
                    <div key={i} className="bg-white/5 rounded-xl p-4 text-center">
                      <p className="text-sm text-gray-400 mb-1">{point.period}</p>
                      <p className="text-xl font-bold text-white">{point.value.toFixed(1)}</p>
                    </div>
                  ))}
                </div>
              </div>

              <div>
                <p className="text-sm text-gray-400 mb-3">Interpretation</p>
                <p className="text-gray-300">{forecastData.interpretation}</p>
              </div>
            </div>
          );

        case 'analyzer':
          const analyzerData = report.data as FinancialReportResponse;
          return (
            <div className="space-y-6">
              <div>
                <p className="text-sm text-gray-400 mb-3">Financial Analysis</p>
                <p className="text-gray-300 whitespace-pre-line">{analyzerData.analysis}</p>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                {Object.entries(analyzerData.metrics).map(([key, value]) => (
                  <div key={key} className="bg-white/5 rounded-xl p-4">
                    <p className="text-sm text-gray-400 mb-1 capitalize">{key.replace(/_/g, ' ')}</p>
                    <p className="text-xl font-bold text-white">{value || 'N/A'}</p>
                  </div>
                ))}
              </div>

              {analyzerData.key_highlights && analyzerData.key_highlights.length > 0 && (
                <div>
                  <p className="text-sm text-gray-400 mb-3">Key Highlights</p>
                  <ul className="space-y-2">
                    {analyzerData.key_highlights.map((highlight, i) => (
                      <li key={i} className="flex items-start space-x-2">
                        <span className="text-green-500 mt-1">•</span>
                        <span className="text-gray-300">{highlight}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              )}

              {analyzerData.key_risks && analyzerData.key_risks.length > 0 && (
                <div>
                  <p className="text-sm text-gray-400 mb-3">Key Risks</p>
                  <ul className="space-y-2">
                    {analyzerData.key_risks.map((risk, i) => (
                      <li key={i} className="flex items-start space-x-2">
                        <span className="text-red-500 mt-1">•</span>
                        <span className="text-gray-300">{risk}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          );

        default:
          return <p className="text-gray-300">No data available for this report.</p>;
      }
    };

    return (
      <div className="fixed inset-0 bg-black/50 backdrop-blur-sm z-50 flex items-center justify-center p-4">
        <div className="bg-slate-900 rounded-2xl border border-white/20 max-w-4xl w-full max-h-[90vh] overflow-y-auto">
          <div className="sticky top-0 bg-slate-900 border-b border-white/10 p-6 flex items-center justify-between">
            <h2 className="text-2xl font-bold text-white">{report.title}</h2>
            <button
              onClick={onClose}
              className="text-gray-400 hover:text-white transition-colors"
            >
              <X className="w-6 h-6" />
            </button>
          </div>
          
          <div className="p-6">
            <div className="flex items-center space-x-3 mb-6">
              <div className={`p-3 rounded-xl ${getTypeColor(report.type)}`}>
                {getTypeIcon(report.type)}
              </div>
              <div>
                <p className="text-sm text-gray-400">{report.type.charAt(0).toUpperCase() + report.type.slice(1)} Report</p>
                <p className="text-white font-medium">{formatDate(report.createdAt)}</p>
              </div>
            </div>

            {renderReportContent()}

            <div className="flex justify-end space-x-3 pt-6 border-t border-white/10">
              <button
                onClick={() => downloadReport(report)}
                className="flex items-center space-x-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
              >
                <Download className="w-4 h-4" />
                <span>Download Report</span>
              </button>
              <button
                onClick={onClose}
                className="px-4 py-2 bg-white/10 text-white rounded-lg hover:bg-white/20 transition-colors"
              >
                Close
              </button>
            </div>
          </div>
        </div>
      </div>
    );
  };

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-64">
        <Loader2 className="w-8 h-8 text-purple-400 animate-spin" />
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-white/10 backdrop-blur-lg rounded-2xl p-8 border border-white/20">
        <div className="flex items-center space-x-3 mb-6">
          <div className="p-3 bg-orange-500/20 rounded-xl">
            <FileText className="w-6 h-6 text-orange-400" />
          </div>
          <div>
            <h2 className="text-2xl font-bold text-white">Reports</h2>
            <p className="text-gray-300">View and manage all your analysis reports</p>
          </div>
        </div>

        {/* Filters and Search */}
        <div className="flex flex-col md:flex-row gap-4">
          <div className="flex-1 relative">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
            <input
              type="text"
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              placeholder="Search reports..."
              className="w-full pl-10 pr-4 py-2 bg-white/5 border border-white/20 rounded-xl text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent"
            />
          </div>
          
          <div className="flex gap-2">
            <button
              onClick={() => setFilter('all')}
              className={`px-4 py-2 rounded-xl transition-colors ${
                filter === 'all' 
                  ? 'bg-orange-600 text-white' 
                  : 'bg-white/10 text-gray-300 hover:bg-white/20'
              }`}
            >
              All
            </button>
            <button
              onClick={() => setFilter('startup')}
              className={`px-4 py-2 rounded-xl transition-colors ${
                filter === 'startup' 
                  ? 'bg-purple-600 text-white' 
                  : 'bg-white/10 text-gray-300 hover:bg-white/20'
              }`}
            >
              Startup
            </button>
            <button
              onClick={() => setFilter('market')}
              className={`px-4 py-2 rounded-xl transition-colors ${
                filter === 'market' 
                  ? 'bg-blue-600 text-white' 
                  : 'bg-white/10 text-gray-300 hover:bg-white/20'
              }`}
            >
              Market
            </button>
            <button
              onClick={() => setFilter('forecasting')}
              className={`px-4 py-2 rounded-xl transition-colors ${
                filter === 'forecasting' 
                  ? 'bg-green-600 text-white' 
                  : 'bg-white/10 text-gray-300 hover:bg-white/20'
              }`}
            >
              Forecasting
            </button>
            <button
              onClick={() => setFilter('analyzer')}
              className={`px-4 py-2 rounded-xl transition-colors ${
                filter === 'analyzer' 
                  ? 'bg-orange-600 text-white' 
                  : 'bg-white/10 text-gray-300 hover:bg-white/20'
              }`}
            >
              Financial
            </button>
          </div>
        </div>
      </div>

      {/* Reports List */}
      <div className="space-y-4">
        {filteredReports.length === 0 ? (
          <div className="bg-white/10 backdrop-blur-lg rounded-2xl p-12 border border-white/20 text-center">
            <FileText className="w-16 h-16 text-gray-400 mx-auto mb-4" />
            <h3 className="text-xl font-semibold text-white mb-2">No reports found</h3>
            <p className="text-gray-400">
              {searchTerm || filter !== 'all' 
                ? 'Try adjusting your filters or search terms' 
                : 'Start by running an analysis to generate your first report'}
            </p>
          </div>
        ) : (
          filteredReports.map((report) => (
            <div
              key={report.id}
              className="bg-white/10 backdrop-blur-lg rounded-2xl p-6 border border-white/20 hover:bg-white/15 transition-all duration-200"
            >
              <div className="flex items-start justify-between">
                <div className="flex items-start space-x-4 flex-1">
                  <div className={`p-3 rounded-xl ${getTypeColor(report.type)}`}>
                    {getTypeIcon(report.type)}
                  </div>
                  <div className="flex-1">
                    <div className="flex items-center space-x-3 mb-2">
                      <h3 className="text-lg font-semibold text-white">{report.title}</h3>
                      {getStatusIcon(report.status)}
                    </div>
                    <p className="text-gray-300 mb-3">{report.description}</p>
                    <div className="flex items-center space-x-6 text-sm text-gray-400">
                      <div className="flex items-center space-x-1">
                        <Calendar className="w-4 h-4" />
                        <span>{formatDate(report.createdAt)}</span>
                      </div>
                      <div className="flex items-center space-x-1">
                        <span className={`px-2 py-1 rounded-full text-xs font-medium ${getTypeColor(report.type)}`}>
                          {report.type.charAt(0).toUpperCase() + report.type.slice(1)}
                        </span>
                      </div>
                      {getReportScore(report) && (
                        <div className="flex items-center space-x-1">
                          <Target className="w-4 h-4" />
                          <span>Score: {getReportScore(report)}/100</span>
                        </div>
                      )}
                    </div>
                  </div>
                </div>
                
                <div className="flex items-center space-x-2 ml-4">
                  {report.status === 'completed' && (
                    <>
                      <button
                        onClick={() => setSelectedReport(report)}
                        className="p-2 text-blue-400 hover:bg-blue-500/20 rounded-lg transition-colors"
                        title="View Report"
                      >
                        <Eye className="w-5 h-5" />
                      </button>
                      <button
                        onClick={() => downloadReport(report)}
                        className="p-2 text-green-400 hover:bg-green-500/20 rounded-lg transition-colors"
                        title="Download Report"
                      >
                        <Download className="w-5 h-5" />
                      </button>
                    </>
                  )}
                  <button
                    onClick={() => handleDeleteReport(report.id)}
                    className="p-2 text-red-400 hover:bg-red-500/20 rounded-lg transition-colors"
                    title="Delete Report"
                  >
                    <Trash2 className="w-5 h-5" />
                  </button>
                </div>
              </div>
            </div>
          ))
        )}
      </div>

      {/* Report Detail Modal */}
      {selectedReport && (
        <ReportDetailModal
          report={selectedReport}
          onClose={() => setSelectedReport(null)}
        />
      )}

      {/* Delete Confirmation Modal */}
      {showDeleteModal && (
        <div className="fixed inset-0 bg-black/50 backdrop-blur-sm z-50 flex items-center justify-center p-4">
          <div className="bg-slate-900 rounded-2xl border border-white/20 max-w-md w-full p-6">
            <div className="flex items-center space-x-3 mb-4">
              <div className="p-3 bg-red-500/20 rounded-xl">
                <AlertTriangle className="w-6 h-6 text-red-400" />
              </div>
              <div>
                <h3 className="text-lg font-semibold text-white">Delete Report</h3>
                <p className="text-gray-300 text-sm">This action cannot be undone</p>
              </div>
            </div>
            
            <p className="text-gray-300 mb-6">
              Are you sure you want to delete this report? This will permanently remove the analysis data.
            </p>
            
            <div className="flex justify-end space-x-3">
              <button
                onClick={() => setShowDeleteModal(false)}
                className="px-4 py-2 bg-white/10 text-white rounded-lg hover:bg-white/20 transition-colors"
              >
                Cancel
              </button>
              <button
                onClick={confirmDelete}
                className="px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors"
              >
                Delete Report
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
