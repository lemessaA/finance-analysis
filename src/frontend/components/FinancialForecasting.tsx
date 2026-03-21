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
  Zap,
  X
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
      {period: "2024-01", value: 190 },
      { period: "2024-04", value: 230 },
    ],
    forecast_periods: 4,
    model_type: "auto",
  });
  
  const [state, setState] = useState<LoadingState>("idle");
  const [result, setResult] = useState<ForecastResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

  // Sample Ethiopian business datasets
  const sampleDatasets = [
    {
      name: "Ethiopian Coffee Shop Revenue",
      metric: "Revenue (ETB 000s)",
      data: [
        { period: "2023-Q1", value: 450 },
        { period: "2023-Q2", value: 520 },
        { period: "2023-Q3", value: 580 },
        { period: "2023-Q4", value: 650 },
        { period: "2024-Q1", value: 720 },
        { period: "2024-Q2", value: 810 },
      ],
      description: "Quarterly revenue data for Addis Ababa coffee shop chain"
    },
    {
      name: "Mobile Money Transactions Volume",
      metric: "Transactions (Millions)",
      data: [
        { period: "2023-01", value: 12.5 },
        { period: "2023-02", value: 14.2 },
        { period: "2023-03", value: 15.8 },
        { period: "2023-04", value: 17.3 },
        { period: "2023-05", value: 19.1 },
        { period: "2023-06", value: 21.4 },
      ],
      description: "Monthly mobile money transaction volume in Ethiopia"
    },
    {
      name: "Solar Panel Sales",
      metric: "Units Sold",
      data: [
        { period: "2023-Q1", value: 120 },
        { period: "2023-Q2", value: 145 },
        { period: "2023-Q3", value: 178 },
        { period: "2023-Q4", value: 210 },
        { period: "2024-Q1", value: 255 },
        { period: "2024-Q2", value: 298 },
      ],
      description: "Quarterly solar panel sales for Ethiopian renewable energy company"
    },
    {
      name: "E-commerce Monthly Orders",
      metric: "Orders (Thousands)",
      data: [
        { period: "2023-07", value: 8.2 },
        { period: "2023-08", value: 9.1 },
        { period: "2023-09", value: 10.3 },
        { period: "2023-10", value: 11.8 },
        { period: "2023-11", value: 13.2 },
        { period: "2023-12", value: 15.1 },
      ],
      description: "Monthly e-commerce orders for Ethiopian online retail platform"
    }
  ];

  const loadSampleDataset = (dataset: typeof sampleDatasets[0]) => {
    setForm({
      ...form,
      metric: dataset.metric,
      historical_data: dataset.data,
    });
    setError(null);
    setState("idle");
  };

  const addDataPoint = () => {
    const newPoint = {
      period: `2024-Q${form.historical_data.length % 4 + 1}`,
      value: Math.round(form.historical_data[form.historical_data.length - 1]?.value * 1.1 || 100)
    };
    setForm({
      ...form,
      historical_data: [...form.historical_data, newPoint]
    });
  };

  const removeDataPoint = (index: number) => {
    setForm({
      ...form,
      historical_data: form.historical_data.filter((_, i) => i !== index)
    });
  };

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

  const updateDataPoint = (index: number, field: 'period' | 'value', value: string | number) => {
    const updatedData = [...form.historical_data];
    if (field === 'period') {
      updatedData[index].period = value as string;
    } else {
      updatedData[index].value = typeof value === 'string' ? parseFloat(value) || 0 : value;
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
            <p className="text-gray-300">AI-powered Ethiopian business financial forecasting and predictions</p>
          </div>
        </div>

        {/* Sample Datasets */}
        <div className="mb-6 p-4 bg-green-500/10 rounded-xl border border-green-500/30">
          <p className="text-sm font-medium text-green-300 mb-3">📈 Sample Ethiopian Business Datasets:</p>
          <div className="space-y-2">
            {sampleDatasets.map((dataset, index) => (
              <button
                key={index}
                onClick={() => loadSampleDataset(dataset)}
                className="w-full text-left p-3 bg-white/5 rounded-lg hover:bg-white/10 transition-colors text-sm"
              >
                <span className="text-green-400 font-medium">{dataset.name}:</span>
                <span className="text-gray-300 ml-2">{dataset.description}</span>
              </button>
            ))}
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
                placeholder="e.g., Revenue (ETB), Users, Sales Volume"
              />
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-200 mb-2">
                Forecast Periods
              </label>
              <input
                type="number"
                value={form.forecast_periods}
                onChange={(e) => setForm({ ...form, forecast_periods: parseInt(e.target.value) || 4 })}
                className="w-full px-4 py-3 bg-white/5 border border-white/20 rounded-xl text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-transparent transition-all"
                placeholder="Number of periods to forecast"
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
                <option value="auto">Auto Select</option>
                <option value="linear">Linear Regression</option>
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
                <div key={index} className="flex items-center space-x-2 p-2 bg-white/5 rounded-lg">
                  <input
                    type="text"
                    value={point.period}
                    onChange={(e) => {
                      const newData = [...form.historical_data];
                      newData[index].period = e.target.value;
                      setForm({ ...form, historical_data: newData });
                    }}
                    className="flex-1 px-3 py-2 bg-white/10 border border-white/20 rounded text-white text-sm"
                    placeholder="Period (e.g., 2023-Q1)"
                  />
                  <input
                    type="number"
                    value={point.value}
                    onChange={(e) => {
                      const newData = [...form.historical_data];
                      newData[index].value = parseFloat(e.target.value) || 0;
                      setForm({ ...form, historical_data: newData });
                    }}
                    className="flex-1 px-3 py-2 bg-white/10 border border-white/20 rounded text-white text-sm"
                    placeholder="Value"
                  />
                  {form.historical_data.length > 3 && (
                    <button
                      type="button"
                      onClick={() => removeDataPoint(index)}
                      className="p-2 text-red-400 hover:bg-red-500/20 rounded transition-colors"
                    >
                      <X className="w-4 h-4" />
                    </button>
                  )}
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
