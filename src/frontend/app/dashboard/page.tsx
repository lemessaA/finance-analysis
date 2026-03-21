"use client";

import { useState, useEffect } from 'react';
import { useAuth } from '@/contexts/AuthContext';
import { getPlatformStats } from '@/services/api';
import StartupValidator from '@/components/StartupValidator';
import MarketIntelligence from '@/components/MarketIntelligence';
import FinancialForecasting from '@/components/FinancialForecasting';
import Reports from '@/components/Reports';
import FinancialReportAnalyzer from '@/components/FinancialReportAnalyzer';
import { 
  Brain, 
  TrendingUp, 
  BarChart3, 
  FileText, 
  Settings, 
  LogOut,
  User,
  Menu,
  X,
  Home,
  Lightbulb,
  LineChart,
  Target,
  Shield,
  Activity,
  DollarSign,
  Globe,
  Search,
  Calculator
} from 'lucide-react';

export default function DashboardPage() {
  const { user, logout } = useAuth();
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const [activeTab, setActiveTab] = useState('overview');
  const [stats, setStats] = useState([
    { name: 'Total Analyses', value: '24', icon: BarChart3, color: 'from-blue-500 to-blue-600', change: '+12%' },
    { name: 'Success Rate', value: '87%', icon: Target, color: 'from-green-500 to-green-600', change: '+5%' },
    { name: 'API Calls', value: '1,284', icon: Activity, color: 'from-purple-500 to-purple-600', change: '+18%' },
    { name: 'Avg. Score', value: '72.5', icon: TrendingUp, color: 'from-orange-500 to-orange-600', change: '+8%' },
  ]);
  const [recentActivity, setRecentActivity] = useState([
    { id: 1, type: 'startup', title: 'AI Meal Planning App', score: 85, time: '2 hours ago', status: 'success' },
    { id: 2, type: 'market', title: 'SaaS Market Analysis', score: null, time: '4 hours ago', status: 'completed' },
    { id: 3, type: 'forecasting', title: 'Revenue Forecast Q1', score: 92, time: '1 day ago', status: 'success' },
    { id: 4, type: 'startup', title: 'HealthTech Platform', score: 78, time: '2 days ago', status: 'success' },
    { id: 5, type: 'analyzer', title: 'Q4 Financial Report Analysis', score: 88, time: '3 days ago', status: 'success' },
  ]);
  const [isLoadingStats, setIsLoadingStats] = useState(false);

  // Load real stats from API on component mount
  useEffect(() => {
    loadStats();
  }, []);

  const loadStats = async () => {
    try {
      setIsLoadingStats(true);
      const statsData = await getPlatformStats();
      
      if (statsData.status === 'success' && statsData.data) {
        const data = statsData.data;
        
        // Update stats
        setStats([
          { 
            name: 'Total Analyses', 
            value: data.total_analyses.toString(), 
            icon: BarChart3, 
            color: 'from-blue-500 to-blue-600', 
            change: '+12%' 
          },
          { 
            name: 'Success Rate', 
            value: `${data.success_rate}%`, 
            icon: Target, 
            color: 'from-green-500 to-green-600', 
            change: '+5%' 
          },
          { 
            name: 'API Calls', 
            value: data.api_calls.toString(), 
            icon: Activity, 
            color: 'from-purple-500 to-purple-600', 
            change: '+18%' 
          },
          { 
            name: 'Avg. Score', 
            value: data.avg_score.toString(), 
            icon: TrendingUp, 
            color: 'from-orange-500 to-orange-600', 
            change: '+8%' 
          },
        ]);
        
        // Update recent activity
        if (data.recent_activity && data.recent_activity.length > 0) {
          setRecentActivity(data.recent_activity.map((activity: any, index: number) => ({
            id: index + 1,
            ...activity
          })));
        }
      }
    } catch (error) {
      console.error('Failed to load stats:', error);
      // Keep using default stats if API fails
    } finally {
      setIsLoadingStats(false);
    }
  };

  const navigation = [
    { name: 'Overview', icon: Home, id: 'overview' },
    { name: 'Startup Validator', icon: Lightbulb, id: 'startup' },
    { name: 'Market Intelligence', icon: LineChart, id: 'market' },
    { name: 'Financial Forecasting', icon: Brain, id: 'forecasting' },
    { name: 'Financial Analyzer', icon: Calculator, id: 'analyzer' },
    { name: 'Reports', icon: FileText, id: 'reports' },
  ];

  const renderContent = () => {
    switch (activeTab) {
      case 'overview':
        return (
          <div className="space-y-6">
            {/* Stats Grid */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
              {stats.map((stat) => (
                <div key={stat.name} className="bg-white/10 backdrop-blur-lg rounded-2xl p-6 border border-white/20">
                  <div className="flex items-center justify-between mb-4">
                    <div className={`p-3 bg-gradient-to-r ${stat.color} rounded-xl`}>
                      <stat.icon className="w-6 h-6 text-white" />
                    </div>
                    <span className="text-green-400 text-sm font-medium">{stat.change}</span>
                  </div>
                  <h3 className="text-2xl font-bold text-white mb-1">{stat.value}</h3>
                  <p className="text-gray-300 text-sm">{stat.name}</p>
                </div>
              ))}
            </div>

            {/* Recent Activity */}
            <div className="bg-white/10 backdrop-blur-lg rounded-2xl p-6 border border-white/20">
              <h2 className="text-xl font-bold text-white mb-6">Recent Activity</h2>
              <div className="space-y-4">
                {recentActivity.map((activity) => (
                  <div key={activity.id} className="flex items-center justify-between p-4 bg-white/5 rounded-xl hover:bg-white/10 transition-colors">
                    <div className="flex items-center space-x-4">
                      <div className={`p-2 rounded-lg ${
                        activity.type === 'startup' ? 'bg-purple-500/20' :
                        activity.type === 'market' ? 'bg-blue-500/20' :
                        activity.type === 'forecasting' ? 'bg-green-500/20' :
                        activity.type === 'analyzer' ? 'bg-orange-500/20' :
                        'bg-gray-500/20'
                      }`}>
                        {activity.type === 'startup' ? <Lightbulb className="w-5 h-5 text-purple-400" /> :
                         activity.type === 'market' ? <LineChart className="w-5 h-5 text-blue-400" /> :
                         activity.type === 'forecasting' ? <Brain className="w-5 h-5 text-green-400" /> :
                         activity.type === 'analyzer' ? <Calculator className="w-5 h-5 text-orange-400" /> :
                         <FileText className="w-5 h-5 text-gray-400" />}
                      </div>
                      <div>
                        <h4 className="text-white font-medium">{activity.title}</h4>
                        <p className="text-gray-400 text-sm">{activity.time}</p>
                      </div>
                    </div>
                    <div className="flex items-center space-x-3">
                      {activity.score && (
                        <span className="text-white font-medium">{activity.score}</span>
                      )}
                      <div className={`w-2 h-2 rounded-full ${
                        activity.status === 'success' ? 'bg-green-400' :
                        activity.status === 'completed' ? 'bg-blue-400' :
                        'bg-yellow-400'
                      }`} />
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        );
      
      case 'startup':
        return <StartupValidator />;
      
      case 'market':
        return <MarketIntelligence />;
      
      case 'forecasting':
        return <FinancialForecasting />;
      
      case 'analyzer':
        return <FinancialReportAnalyzer />;
      
      default:
        return <Reports />;
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900">
      {/* Background Effects */}
      <div className="fixed inset-0 overflow-hidden pointer-events-none">
        <div className="absolute -top-40 -right-40 w-80 h-80 bg-purple-500 rounded-full mix-blend-multiply filter blur-xl opacity-10"></div>
        <div className="absolute -bottom-40 -left-40 w-80 h-80 bg-blue-500 rounded-full mix-blend-multiply filter blur-xl opacity-10"></div>
      </div>

      <div className="flex h-screen relative z-10">
        {/* Sidebar */}
        <div className={`${sidebarOpen ? 'w-64' : 'w-20'} bg-white/10 backdrop-blur-lg border-r border-white/20 transition-all duration-300`}>
          <div className="flex flex-col h-full">
            {/* Logo */}
            <div className="flex items-center justify-between p-4 border-b border-white/10">
              <div className={`flex items-center space-x-3 ${!sidebarOpen && 'justify-center'}`}>
                <div className="flex items-center justify-center w-10 h-10 bg-gradient-to-br from-purple-600 to-blue-600 rounded-xl">
                  <Brain className="w-6 h-6 text-white" />
                </div>
                {sidebarOpen && (
                  <span className="text-white font-bold">AI BI Platform</span>
                )}
              </div>
              <button
                onClick={() => setSidebarOpen(!sidebarOpen)}
                className="text-gray-400 hover:text-white transition-colors"
              >
                {sidebarOpen ? <X className="w-5 h-5" /> : <Menu className="w-5 h-5" />}
              </button>
            </div>

            {/* Navigation */}
            <nav className="flex-1 p-4 space-y-2">
              {navigation.map((item) => (
                <button
                  key={item.id}
                  onClick={() => setActiveTab(item.id)}
                  className={`w-full flex items-center ${sidebarOpen ? 'space-x-3' : 'justify-center'} px-3 py-2 rounded-xl transition-colors ${
                    activeTab === item.id
                      ? 'bg-gradient-to-r from-purple-600 to-blue-600 text-white'
                      : 'text-gray-300 hover:bg-white/10 hover:text-white'
                  }`}
                >
                  <item.icon className="w-5 h-5 flex-shrink-0" />
                  {sidebarOpen && <span className="font-medium">{item.name}</span>}
                </button>
              ))}
            </nav>

            {/* User Profile */}
            <div className="p-4 border-t border-white/10">
              <div className={`flex items-center ${sidebarOpen ? 'space-x-3' : 'justify-center'}`}>
                <img
                  src={user?.avatar || 'https://ui-avatars.com/api/?name=User&background=4f46e5&color=fff'}
                  alt="User"
                  className="w-10 h-10 rounded-full"
                />
                {sidebarOpen && (
                  <div className="flex-1 min-w-0">
                    <p className="text-white font-medium truncate">{user?.name}</p>
                    <p className="text-gray-400 text-sm truncate">{user?.email}</p>
                  </div>
                )}
              </div>
              {sidebarOpen && (
                <button
                  onClick={logout}
                  className="mt-3 w-full flex items-center justify-center space-x-2 px-3 py-2 text-gray-300 hover:bg-white/10 hover:text-white rounded-xl transition-colors"
                >
                  <LogOut className="w-4 h-4" />
                  <span className="text-sm">Logout</span>
                </button>
              )}
            </div>
          </div>
        </div>

        {/* Main Content */}
        <div className="flex-1 overflow-auto">
          <div className="p-8">
            {/* Header */}
            <div className="mb-8">
              <h1 className="text-3xl font-bold text-white mb-2">
                Welcome back, {user?.name}!
              </h1>
              <p className="text-gray-300">
                Here's what's happening with your business intelligence today.
              </p>
            </div>

            {/* Dynamic Content */}
            {renderContent()}
          </div>
        </div>
      </div>
    </div>
  );
}
