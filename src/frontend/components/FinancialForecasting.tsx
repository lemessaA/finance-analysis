"use client";

import { useState } from 'react';
import { generateForecast } from '@/services/api';
import { ForecastResponse } from '@/types';
import { 
  Brain, 
  TrendingUp, 
  BarChart3, 
  Target,
  DollarSign,
  Activity,
  Calendar,
  Send,
  Loader2,
  LineChart as LineChartIcon,
  Zap
} from 'lucide-react';

type LoadingState = "idle" | "loading" | "success" | "error";

export default function FinancialForecasting() {
  const [form, setForm] = useState({
    metric: "Revenue",
    historical_data: [
      { period: "2023-01", value: 100 },
      { period: "2023-04", value: 120 },
      { period: "2023-07", value: 135 },
      { period: "2023-10", value: 160 },
      { period: "2024-01", value: 190 },
      { period: "2024-04", value: 230 },
    ],
    forecast_periods: 4,
    model_type: "auto",
  });
  
  const [state, setState] = useState<LoadingState>("idle");
  const [result, setResult] = useState<ForecastResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setState("loading");
    setError(null);
    setResult(null);

    try {
      const requestData = {
        metric: form.metric,
        historical_data: form.historical_data,
        forecast_periods: form.forecast_periods,
        model_type: "auto"
      };
      const data = await generateForecast(requestData);
      setResult(data);
      setState("success");
    } catch (err: any) {
      setError(
        err?.response?.data?.detail || "Forecasting failed. Please try again."
      );
      setState("error");
    }
  };

  const addDataPoint = () => {
    const newPoint = {
      period: `2024-${String(form.historical_data.length + 1).padStart(2, '0')}`,
      value: Math.floor(Math.random() * 100) + 200
    };
    setForm({ ...form, historical_data: [...form.historical_data, newPoint] });
  };

  const removeDataPoint = (index: number) => {
    if (form.historical_data.length > 3) {
      setForm({ 
        ...form, 
        historical_data: form.historical_data.filter((_, i) => i !== index) 
      });
    }
  };

  const updateDataPoint = (index: number, field: 'period' | 'value', value: string | number) => {
    const updatedData = [...form.historical_data];
    if (field === 'period') {
      updatedData[index].period = value as string;
    } else {
      updatedData[index].value = Number(value);
    }
    setForm({ ...form, historical_data: updatedData });
  };

  const getConfidenceColor = (confidence: string) => {
    switch (confidence.toLowerCase()) {
      case 'high': return 'text-green-400 bg-green-500/20';
      case 'medium': return 'text-yellow-400 bg-yellow-500/20';
      default: return 'text-red-400 bg-red-500/20';
    }
  };

  const ForecastChart = ({ data }: { data: ForecastResponse }) => {
    const maxValue = Math.max(...data.data_points.map(d => d.value));
    const minValue = Math.min(...data.data_points.map(d => d.value));
    const range = maxValue - minValue;

    return (
      <div className="bg-white/5 rounded-xl p-6 border border-white/10">
        <h4 className="text-lg font-semibold text-white mb-4">Forecast Visualization</h4>
        <div className="relative h-64">
          {/* Y-axis labels */}
          <div className="absolute left-0 top-0 h-full flex flex-col justify-between text-xs text-gray-400">
            <span>{maxValue.toFixed(0)}</span>
            <span>{((maxValue + minValue) / 2).toFixed(0)}</span>
            <span>{minValue.toFixed(0)}</span>
          </div>
          
          {/* Chart area */}
          <div className="ml-8 h-full relative">
            {/* Grid lines */}
            <div className="absolute inset-0 flex flex-col justify-between">
              <div className="border-b border-white/10"></div>
              <div className="border-b border-white/10"></div>
              <div className="border-b border-white/10"></div>
            </div>
            
            {/* Data points and lines */}
            <svg className="absolute inset-0 w-full h-full">
              {data.data_points.map((point, i) => {
                const x = (i / (data.data_points.length - 1)) * 100;
                const y = 100 - ((point.value - minValue) / range) * 100;
                
                return (
                  <g key={i}>
                    {i > 0 && (
                      <line
                        x1={`${((i - 1) / (data.data_points.length - 1)) * 100}%`}
                        y1={`${100 - ((data.data_points[i - 1].value - minValue) / range) * 100}%`}
                        x2={`${x}%`}
                        y2={`${y}%`}
                        stroke={point.is_forecast ? "#8b5cf6" : "#3b82f6"}
                        strokeWidth="2"
                      />
                    )}
                    <circle
                      cx={`${x}%`}
                      cy={`${y}%`}
                      r="4"
                      fill={point.is_forecast ? "#8b5cf6" : "#3b82f6"}
                    />
                  </g>
                );
              })}
            </svg>
            
            {/* Forecast divider */}
            {data.data_points.some(p => p.is_forecast) && (
              <div 
                className="absolute top-0 bottom-0 border-l-2 border-dashed border-purple-500"
                style={{
                  left: `${(data.data_points.findIndex(p => p.is_forecast) / (data.data_points.length - 1)) * 100}%`
                }}
              >
                <span className="absolute -top-6 left-2 text-xs text-purple-400">Forecast</span>
              </div>
            )}
            
            {/* X-axis labels */}
            <div className="absolute bottom-0 left-0 right-0 flex justify-between text-xs text-gray-400">
              {data.data_points.map((point, i) => (
                <span key={i} className="transform -rotate-45 origin-left">
                  {point.period}
                </span>
              ))}
            </div>
          </div>
        </div>
      </div>
    );
  };

  return (
    <div className="space-y-8">
      {/* Input Form */}
      <div className="bg-white/10 backdrop-blur-lg rounded-2xl p-8 border border-white/20">
        <div className="flex items-center space-x-3 mb-6">
          <div className="p-3 bg-green-500/20 rounded-xl">
            <Brain className="w-6 h-6 text-green-400" />
          </div>
          <div>
            <h2 className="text-2xl font-bold text-white">Financial Forecasting</h2>
            <p className="text-gray-300">AI-powered financial forecasting and predictions</p>
          </div>
        </div>

        <form onSubmit={handleSubmit} className="space-y-6">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div>
              <label className="block text-sm font-medium text-gray-200 mb-2">
                Metric
              </label>
              <input
                type="text"
                value={form.metric}
                onChange={(e) => setForm({ ...form, metric: e.target.value })}
                className="w-full px-4 py-3 bg-white/5 border border-white/20 rounded-xl text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-transparent transition-all"
                placeholder="e.g., Revenue, Users, Sales"
              />
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-200 mb-2">
                Forecast Periods
              </label>
              <input
                type="number"
                value={form.forecast_periods}
                onChange={(e) => setForm({ ...form, forecast_periods: parseInt(e.target.value) || 1 })}
                className="w-full px-4 py-3 bg-white/5 border border-white/20 rounded-xl text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-transparent transition-all"
                min="1"
                max="12"
              />
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-200 mb-2">
                Model Type
              </label>
              <select
                value={form.model_type}
                onChange={(e) => setForm({ ...form, model_type: e.target.value })}
                className="w-full px-4 py-3 bg-white/5 border border-white/20 rounded-xl text-white focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-transparent transition-all"
              >
                <option value="auto">Auto</option>
                <option value="linear">Linear</option>
                <option value="polynomial">Polynomial</option>
                <option value="exponential">Exponential</option>
              </select>
            </div>
          </div>

          {/* Historical Data */}
          <div>
            <div className="flex items-center justify-between mb-4">
              <label className="block text-sm font-medium text-gray-200">
                Historical Data (Minimum 3 points)
              </label>
              <button
                type="button"
                onClick={addDataPoint}
                className="px-3 py-1 bg-green-500/20 text-green-400 rounded-lg hover:bg-green-500/30 transition-colors text-sm"
              >
                Add Point
              </button>
            </div>
            
            <div className="space-y-2 max-h-64 overflow-y-auto">
              {form.historical_data.map((point, index) => (
                <div key={index} className="flex items-center space-x-2">
                  <input
                    type="text"
                    value={point.period}
                    onChange={(e) => updateDataPoint(index, 'period', e.target.value)}
                    className="flex-1 px-3 py-2 bg-white/5 border border-white/20 rounded-lg text-white text-sm focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-transparent"
                    placeholder="Period"
                  />
                  <input
                    type="number"
                    value={point.value}
                    onChange={(e) => updateDataPoint(index, 'value', e.target.value)}
                    className="flex-1 px-3 py-2 bg-white/5 border border-white/20 rounded-lg text-white text-sm focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-transparent"
                    placeholder="Value"
                  />
                  <button
                    type="button"
                    onClick={() => removeDataPoint(index)}
                    disabled={form.historical_data.length <= 3}
                    className="p-2 text-red-400 hover:bg-red-500/20 rounded-lg transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                  >
                    <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                    </svg>
                  </button>
                </div>
              ))}
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
            className="w-full bg-gradient-to-r from-green-600 to-blue-600 text-white font-semibold py-3 px-6 rounded-xl hover:from-green-700 hover:to-blue-700 focus:outline-none focus:ring-2 focus:ring-green-500 focus:ring-offset-2 focus:ring-offset-transparent transition-all disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center space-x-2"
          >
            {state === "loading" ? (
              <>
                <Loader2 className="w-5 h-5 animate-spin" />
                <span>Generating Forecast...</span>
              </>
            ) : (
              <>
                <Zap className="w-5 h-5" />
                <span>Generate Forecast</span>
              </>
            )}
          </button>
        </form>
      </div>

      {/* Results */}
      {result && state === "success" && (
        <div className="space-y-6 animate-fade-in">
          {/* Forecast Summary */}
          <div className="bg-white/10 backdrop-blur-lg rounded-2xl p-8 border border-white/20">
            <div className="flex items-center space-x-3 mb-6">
              <Target className="w-6 h-6 text-green-400" />
              <h3 className="text-xl font-bold text-white">Forecast Summary</h3>
            </div>
            
            <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-6">
              <div className="text-center">
                <div className="inline-flex items-center justify-center w-12 h-12 bg-blue-500/20 rounded-xl mb-3">
                  <DollarSign className="w-6 h-6 text-blue-400" />
                </div>
                <h4 className="text-lg font-bold text-white mb-1">Metric</h4>
                <p className="text-gray-300">{result.metric}</p>
              </div>
              
              <div className="text-center">
                <div className="inline-flex items-center justify-center w-12 h-12 bg-purple-500/20 rounded-xl mb-3">
                  <Brain className="w-6 h-6 text-purple-400" />
                </div>
                <h4 className="text-lg font-bold text-white mb-1">Model</h4>
                <p className="text-gray-300">{result.model_used}</p>
              </div>
              
              <div className="text-center">
                <div className="inline-flex items-center justify-center w-12 h-12 bg-green-500/20 rounded-xl mb-3">
                  <Activity className="w-6 h-6 text-green-400" />
                </div>
                <h4 className="text-lg font-bold text-white mb-1">R² Score</h4>
                <p className="text-gray-300">{result.r_squared.toFixed(3)}</p>
              </div>
              
              <div className="text-center">
                <div className={`inline-flex items-center justify-center w-12 h-12 rounded-xl mb-3 ${getConfidenceColor(result.confidence)}`}>
                  <TrendingUp className="w-6 h-6" />
                </div>
                <h4 className="text-lg font-bold text-white mb-1">Confidence</h4>
                <p className="text-gray-300">{result.confidence}</p>
              </div>
            </div>
            
            <div className="bg-white/5 rounded-xl p-4 border border-white/10">
              <h4 className="text-sm font-medium text-gray-200 mb-2">Growth Rate</h4>
              <div className="flex items-center space-x-2">
                <TrendingUp className="w-5 h-5 text-green-400" />
                <span className="text-2xl font-bold text-white">
                  {(result.avg_growth_rate * 100).toFixed(1)}%
                </span>
                <span className="text-gray-400">average growth</span>
              </div>
            </div>
          </div>

          {/* Forecast Chart */}
          <ForecastChart data={result} />

          {/* Forecast Values */}
          <div className="bg-white/10 backdrop-blur-lg rounded-2xl p-8 border border-white/20">
            <div className="flex items-center space-x-3 mb-6">
              <Calendar className="w-6 h-6 text-blue-400" />
              <h3 className="text-xl font-bold text-white">Forecast Values</h3>
            </div>
            
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {result.data_points.filter(point => point.is_forecast).map((point, i) => (
                <div key={i} className="bg-white/5 rounded-xl p-4 border border-purple-500/20">
                  <div className="flex items-center justify-between mb-2">
                    <span className="text-sm text-gray-400">{point.period}</span>
                    <span className="text-xs px-2 py-1 bg-purple-500/20 text-purple-400 rounded-full">
                      Forecast
                    </span>
                  </div>
                  <div className="text-2xl font-bold text-white mb-2">
                    {point.value.toFixed(1)}
                  </div>
                  {point.lower_bound && point.upper_bound && (
                    <div className="text-xs text-gray-400">
                      Range: {point.lower_bound.toFixed(1)} - {point.upper_bound.toFixed(1)}
                    </div>
                  )}
                </div>
              ))}
            </div>
          </div>

          {/* Interpretation */}
          <div className="bg-white/10 backdrop-blur-lg rounded-2xl p-8 border border-white/20">
            <div className="flex items-center space-x-3 mb-6">
              <LineChartIcon className="w-6 h-6 text-purple-400" />
              <h3 className="text-xl font-bold text-white">AI Interpretation</h3>
            </div>
            <div className="prose prose-invert max-w-none">
              <p className="text-gray-300 leading-relaxed">{result.interpretation}</p>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
