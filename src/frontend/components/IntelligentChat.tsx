"use client";

import { useState, useEffect, useRef, useCallback } from "react";
import {
  MessageCircle,
  Send,
  Database,
  BarChart3,
  TrendingUp,
  Download,
  Settings,
  Loader2,
  CheckCircle2,
  AlertTriangle,
  Lightbulb,
  ArrowRight,
  Copy,
  Trash2,
  Maximize2,
  Minimize2,
  RefreshCw,
  Eye,
  EyeOff,
  Sparkles,
  Brain,
  FileText,
  PieChart,
  LineChart,
  ScatterChart,
  Activity
} from "lucide-react";

interface Message {
  id: string;
  type: "human" | "ai";
  content: string;
  timestamp: string;
  data?: any;
  visualization?: any;
  suggestions?: string[];
  follow_up_questions?: string[];
  confidence_score?: number;
  query_info?: any;
}

interface ChatSession {
  session_id: string;
  database_name: string;
  database_type: string;
  session_name: string;
  created_at: string;
}

interface DatabaseConfig {
  id: string;
  name: string;
  type: string;
  status: string;
}

export default function IntelligentChat() {
  const [sessions, setSessions] = useState<ChatSession[]>([]);
  const [currentSession, setCurrentSession] = useState<ChatSession | null>(null);
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputMessage, setInputMessage] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [isTyping, setIsTyping] = useState(false);
  const [databases, setDatabases] = useState<DatabaseConfig[]>([]);
  const [selectedDatabase, setSelectedDatabase] = useState<string>("");
  const [showDatabaseSelector, setShowDatabaseSelector] = useState(false);
  const [suggestions, setSuggestions] = useState<string[]>([]);
  const [showSuggestions, setShowSuggestions] = useState(false);
  const [expandedMessage, setExpandedMessage] = useState<string | null>(null);
  const [isFullscreen, setIsFullscreen] = useState(false);
  const [showVisualization, setShowVisualization] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  // Load databases on mount
  useEffect(() => {
    loadDatabases();
  }, []);

  // Auto-scroll to bottom
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const loadDatabases = async () => {
    try {
      const response = await fetch("/api/v1/database-config/configurations");
      const data = await response.json();
      
      if (data.success) {
        // Only show connected databases
        const connectedDbs = data.configurations.filter((db: DatabaseConfig) => db.status === "connected");
        setDatabases(connectedDbs);
      }
    } catch (error) {
      console.error("Error loading databases:", error);
    }
  };

  const createChatSession = async (databaseId: string) => {
    try {
      setIsLoading(true);
      
      const response = await fetch("/api/v1/intelligent-chat/sessions", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          database_id: databaseId,
          session_name: `Chat Session ${new Date().toLocaleTimeString()}`
        })
      });
      
      const data = await response.json();
      
      if (data.success) {
        const newSession: ChatSession = {
          session_id: data.session_id,
          database_name: data.database_name,
          database_type: data.database_type,
          session_name: data.session_name,
          created_at: data.created_at
        };
        
        setCurrentSession(newSession);
        setMessages([{
          id: "welcome",
          type: "ai",
          content: `Hello! I'm connected to ${data.database_name}. I can help you explore your data using natural language. Try asking me questions like:\n\n• "Show me recent sales data"\n• "What are our top products?"\n• "How many users do we have?"\n\nWhat would you like to know?`,
          timestamp: new Date().toISOString(),
          suggestions: [
            "Show me recent sales data",
            "What are our top products?",
            "How many users do we have?",
            "What are the total sales by month?"
          ]
        }]);
        
        setShowDatabaseSelector(false);
        loadSuggestions(data.session_id);
      }
    } catch (error) {
      console.error("Error creating chat session:", error);
    } finally {
      setIsLoading(false);
    }
  };

  const loadSuggestions = async (sessionId: string) => {
    try {
      const response = await fetch(`/api/v1/intelligent-chat/sessions/${sessionId}/suggestions`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({})
      });
      
      const data = await response.json();
      
      if (data.success) {
        setSuggestions(data.suggestions);
      }
    } catch (error) {
      console.error("Error loading suggestions:", error);
    }
  };

  const sendMessage = async (message: string) => {
    if (!message.trim() || !currentSession || isLoading) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      type: "human",
      content: message,
      timestamp: new Date().toISOString()
    };

    setMessages(prev => [...prev, userMessage]);
    setInputMessage("");
    setIsLoading(true);
    setIsTyping(true);

    try {
      const response = await fetch("/api/v1/intelligent-chat/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          session_id: currentSession.session_id,
          message: message,
          include_visualization: true
        })
      });

      const data = await response.json();

      if (data.success) {
        const aiMessage: Message = {
          id: (Date.now() + 1).toString(),
          type: "ai",
          content: data.message,
          timestamp: new Date().toISOString(),
          data: data.data,
          visualization: data.visualization,
          suggestions: data.suggestions,
          follow_up_questions: data.follow_up_questions,
          confidence_score: data.confidence_score,
          query_info: data.query_info
        };

        setMessages(prev => [...prev, aiMessage]);
        
        // Update suggestions
        if (data.suggestions) {
          setSuggestions(data.suggestions);
        }
      }
    } catch (error) {
      console.error("Error sending message:", error);
      
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        type: "ai",
        content: "I'm sorry, I encountered an error while processing your request. Please try again.",
        timestamp: new Date().toISOString()
      };
      
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
      setIsTyping(false);
    }
  };

  const handleSuggestionClick = (suggestion: string) => {
    setInputMessage(suggestion);
    inputRef.current?.focus();
  };

  const handleFollowUpClick = (question: string) => {
    sendMessage(question);
  };

  const exportConversation = async (format: string = "json") => {
    if (!currentSession) return;

    try {
      const response = await fetch(`/api/v1/intelligent-chat/sessions/${currentSession.session_id}/export`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ format })
      });

      const data = await response.json();

      if (data.success) {
        // Create and download file
        const blob = new Blob([JSON.stringify(data.export_data, null, 2)], {
          type: format === "csv" ? "text/csv" : "application/json"
        });
        
        const url = URL.createObjectURL(blob);
        const a = document.createElement("a");
        a.href = url;
        a.download = `chat-export-${currentSession.session_id}.${format}`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
      }
    } catch (error) {
      console.error("Error exporting conversation:", error);
    }
  };

  const clearConversation = async () => {
    if (!currentSession) return;

    try {
      const response = await fetch(`/api/v1/intelligent-chat/sessions/${currentSession.session_id}`, {
        method: "DELETE"
      });

      if (response.ok) {
        setMessages([]);
        loadSuggestions(currentSession.session_id);
      }
    } catch (error) {
      console.error("Error clearing conversation:", error);
    }
  };

  const getVisualizationIcon = (chartType: string) => {
    switch (chartType) {
      case "bar": return <BarChart3 className="w-4 h-4" />;
      case "line": return <LineChart className="w-4 h-4" />;
      case "pie": return <PieChart className="w-4 h-4" />;
      case "scatter": return <ScatterChart className="w-4 h-4" />;
      case "area": return <Activity className="w-4 h-4" />;
      default: return <BarChart3 className="w-4 h-4" />;
    }
  };

  const getConfidenceColor = (score: number) => {
    if (score >= 0.8) return "text-green-500";
    if (score >= 0.6) return "text-yellow-500";
    return "text-red-500";
  };

  if (!currentSession) {
    return (
      <div className="max-w-4xl mx-auto animate-fade-in">
        <div className="mb-8">
          <div className="flex items-center gap-3 mb-3">
            <div className="w-12 h-12 rounded-2xl bg-gradient-to-br from-purple-500 to-pink-600 flex items-center justify-center shadow-lg shadow-purple-500/20">
              <MessageCircle className="w-6 h-6 text-white" />
            </div>
            <div>
              <h1 className="text-3xl font-bold text-white tracking-tight">
                Chat with Your Data
              </h1>
              <p className="text-slate-400">
                Ask questions in plain English to retrieve and analyze your company data
              </p>
            </div>
          </div>
        </div>

        {/* Database Selection */}
        <div className="glass rounded-3xl p-8 border border-white/10 shadow-2xl">
          <h2 className="text-xl font-semibold text-white mb-6 flex items-center gap-2">
            <Database className="w-6 h-6 text-blue-500" />
            Select Database to Chat With
          </h2>

          {databases.length === 0 ? (
            <div className="text-center py-12">
              <Database className="w-16 h-16 text-gray-500 mx-auto mb-4" />
              <h3 className="text-lg font-medium text-white mb-2">No Connected Databases</h3>
              <p className="text-gray-400 mb-6">
                Please configure and connect a database first.
              </p>
              <button
                onClick={() => window.location.href = "/database"}
                className="px-6 py-3 bg-gradient-to-r from-blue-600 to-purple-600 text-white font-semibold rounded-xl hover:from-blue-500 hover:to-purple-500 transition-all duration-300"
              >
                Configure Database
              </button>
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {databases.map((db) => (
                <button
                  key={db.id}
                  onClick={() => createChatSession(db.id)}
                  className="p-6 bg-white/5 rounded-xl border border-white/20 hover:bg-white/10 transition-all text-left group"
                >
                  <div className="flex items-center justify-between mb-3">
                    <div className="flex items-center gap-3">
                      <div className="w-10 h-10 rounded-lg bg-blue-500/20 flex items-center justify-center text-xl">
                        🗄️
                      </div>
                      <div>
                        <h3 className="text-white font-medium">{db.name}</h3>
                        <p className="text-sm text-gray-400 capitalize">{db.type}</p>
                      </div>
                    </div>
                    <ArrowRight className="w-5 h-5 text-gray-400 group-hover:text-white transition-colors" />
                  </div>
                  <div className="flex items-center gap-2 text-sm text-gray-400">
                    <CheckCircle2 className="w-4 h-4 text-green-500" />
                    <span>Connected</span>
                  </div>
                </button>
              ))}
            </div>
          )}
        </div>

        {/* Features */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mt-8">
          <div className="glass rounded-2xl p-6 border border-white/10">
            <div className="flex items-center gap-3 mb-3">
              <Brain className="w-6 h-6 text-purple-500" />
              <h3 className="text-lg font-semibold text-white">Natural Language</h3>
            </div>
            <p className="text-gray-300 text-sm">
              Ask questions in plain English - no SQL knowledge required
            </p>
          </div>
          
          <div className="glass rounded-2xl p-6 border border-white/10">
            <div className="flex items-center gap-3 mb-3">
              <BarChart3 className="w-6 h-6 text-green-500" />
              <h3 className="text-lg font-semibold text-white">Data Visualization</h3>
            </div>
            <p className="text-gray-300 text-sm">
              Automatic chart suggestions based on your data
            </p>
          </div>
          
          <div className="glass rounded-2xl p-6 border border-white/10">
            <div className="flex items-center gap-3 mb-3">
              <Sparkles className="w-6 h-6 text-yellow-500" />
              <h3 className="text-lg font-semibold text-white">Smart Insights</h3>
            </div>
            <p className="text-gray-300 text-sm">
              AI-powered analysis and recommendations
            </p>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className={`max-w-6xl mx-auto animate-fade-in ${isFullscreen ? 'fixed inset-0 z-50 bg-slate-900' : ''}`}>
      <div className={`${isFullscreen ? 'h-full flex flex-col' : ''}`}>
        {/* Header */}
        <div className="flex items-center justify-between mb-6">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-purple-500 to-pink-600 flex items-center justify-center">
              <MessageCircle className="w-5 h-5 text-white" />
            </div>
            <div>
              <h2 className={`text-xl font-bold text-white ${isFullscreen ? 'text-2xl' : ''}`}>
                Chat with {currentSession.database_name}
              </h2>
              <p className="text-sm text-gray-400">{currentSession.session_name}</p>
            </div>
          </div>
          
          <div className="flex items-center gap-2">
            <button
              onClick={() => setShowSuggestions(!showSuggestions)}
              className="p-2 bg-white/10 text-white rounded-lg hover:bg-white/20 transition-all"
              title="Show Suggestions"
            >
              <Lightbulb className="w-5 h-5" />
            </button>
            
            <button
              onClick={() => exportConversation("json")}
              className="p-2 bg-white/10 text-white rounded-lg hover:bg-white/20 transition-all"
              title="Export Conversation"
            >
              <Download className="w-5 h-5" />
            </button>
            
            <button
              onClick={clearConversation}
              className="p-2 bg-white/10 text-white rounded-lg hover:bg-white/20 transition-all"
              title="Clear Conversation"
            >
              <Trash2 className="w-5 h-5" />
            </button>
            
            <button
              onClick={() => setIsFullscreen(!isFullscreen)}
              className="p-2 bg-white/10 text-white rounded-lg hover:bg-white/20 transition-all"
              title={isFullscreen ? "Exit Fullscreen" : "Fullscreen"}
            >
              {isFullscreen ? <Minimize2 className="w-5 h-5" /> : <Maximize2 className="w-5 h-5" />}
            </button>
          </div>
        </div>

        <div className={`flex gap-6 ${isFullscreen ? 'flex-1 min-h-0' : ''}`}>
          {/* Suggestions Panel */}
          {showSuggestions && (
            <div className="w-80 glass rounded-2xl p-6 border border-white/10">
              <h3 className="text-lg font-semibold text-white mb-4 flex items-center gap-2">
                <Lightbulb className="w-5 h-5 text-yellow-500" />
                Suggested Questions
              </h3>
              <div className="space-y-2">
                {suggestions.map((suggestion, index) => (
                  <button
                    key={index}
                    onClick={() => handleSuggestionClick(suggestion)}
                    className="w-full text-left p-3 bg-white/5 rounded-lg hover:bg-white/10 transition-all text-sm text-gray-300 hover:text-white group"
                  >
                    <div className="flex items-center justify-between">
                      <span>{suggestion}</span>
                      <ArrowRight className="w-4 h-4 text-gray-400 group-hover:text-white transition-colors" />
                    </div>
                  </button>
                ))}
              </div>
            </div>
          )}

          {/* Chat Area */}
          <div className={`flex-1 glass rounded-2xl border border-white/10 ${isFullscreen ? 'flex flex-col' : ''}`}>
            {/* Messages */}
            <div className={`flex-1 overflow-y-auto p-6 ${isFullscreen ? 'min-h-0' : 'h-96'}`}>
              <div className="space-y-4">
                {messages.map((message) => (
                  <div
                    key={message.id}
                    className={`flex gap-3 ${message.type === "human" ? "justify-end" : "justify-start"}`}
                  >
                    {message.type === "ai" && (
                      <div className="w-8 h-8 rounded-full bg-gradient-to-br from-purple-500 to-pink-600 flex items-center justify-center flex-shrink-0">
                        <Brain className="w-4 h-4 text-white" />
                      </div>
                    )}
                    
                    <div className={`max-w-3xl ${message.type === "human" ? "order-1" : ""}`}>
                      <div
                        className={`p-4 rounded-2xl ${
                          message.type === "human"
                            ? "bg-gradient-to-r from-blue-600 to-purple-600 text-white"
                            : "bg-white/10 text-white"
                        }`}
                      >
                        <p className="whitespace-pre-wrap">{message.content}</p>
                        
                        {/* Query Info */}
                        {message.query_info && (
                          <div className="mt-3 pt-3 border-t border-white/20">
                            <div className="flex items-center gap-2 text-xs opacity-75">
                              <Database className="w-3 h-3" />
                              <span>Query executed in {message.query_info.execution_time?.toFixed(2)}ms</span>
                              {message.confidence_score && (
                                <span className={`flex items-center gap-1 ${getConfidenceColor(message.confidence_score)}`}>
                                  <Activity className="w-3 h-3" />
                                  {Math.round(message.confidence_score * 100)}% confidence
                                </span>
                              )}
                            </div>
                          </div>
                        )}
                        
                        {/* Data Results */}
                        {message.data && message.data.rows && (
                          <div className="mt-4">
                            <div className="flex items-center justify-between mb-2">
                              <span className="text-sm font-medium">
                                {message.data.rows.length} rows returned
                              </span>
                              <button
                                onClick={() => setExpandedMessage(expandedMessage === message.id ? null : message.id)}
                                className="text-xs opacity-75 hover:opacity-100"
                              >
                                {expandedMessage === message.id ? <EyeOff className="w-3 h-3" /> : <Eye className="w-3 h-3" />}
                              </button>
                            </div>
                            
                            {expandedMessage === message.id && (
                              <div className="mt-2 bg-black/20 rounded-lg p-3 max-h-64 overflow-y-auto">
                                <table className="w-full text-xs">
                                  <thead>
                                    <tr className="border-b border-white/20">
                                      {message.data.columns.map((col: string) => (
                                        <th key={col} className="text-left p-1">{col}</th>
                                      ))}
                                    </tr>
                                  </thead>
                                  <tbody>
                                    {message.data.rows.slice(0, 10).map((row: any, index: number) => (
                                      <tr key={index} className="border-b border-white/10">
                                        {message.data.columns.map((col: string) => (
                                          <td key={col} className="p-1">{row[col]}</td>
                                        ))}
                                      </tr>
                                    ))}
                                  </tbody>
                                </table>
                                {message.data.rows.length > 10 && (
                                  <p className="text-xs text-gray-400 mt-2">
                                    ... and {message.data.rows.length - 10} more rows
                                  </p>
                                )}
                              </div>
                            )}
                          </div>
                        )}
                        
                        {/* Visualization */}
                        {message.visualization && (
                          <div className="mt-4">
                            <div className="flex items-center gap-2 mb-2">
                              {getVisualizationIcon(message.visualization.chart_type)}
                              <span className="text-sm font-medium">
                                {message.visualization.title}
                              </span>
                              <button
                                onClick={() => setShowVisualization(!showVisualization)}
                                className="text-xs opacity-75 hover:opacity-100"
                              >
                                {showVisualization ? <EyeOff className="w-3 h-3" /> : <Eye className="w-3 h-3" />}
                              </button>
                            </div>
                            
                            {showVisualization && (
                              <div className="bg-black/20 rounded-lg p-4">
                                <div className="text-center text-gray-400">
                                  <BarChart3 className="w-12 h-12 mx-auto mb-2" />
                                  <p className="text-sm">Chart visualization would be displayed here</p>
                                  <p className="text-xs opacity-75 mt-1">
                                    Chart Type: {message.visualization.chart_type}
                                  </p>
                                </div>
                              </div>
                            )}
                          </div>
                        )}
                        
                        {/* Follow-up Questions */}
                        {message.follow_up_questions && message.follow_up_questions.length > 0 && (
                          <div className="mt-4 pt-3 border-t border-white/20">
                            <p className="text-sm font-medium mb-2">Follow-up Questions:</p>
                            <div className="space-y-1">
                              {message.follow_up_questions.map((question, index) => (
                                <button
                                  key={index}
                                  onClick={() => handleFollowUpClick(question)}
                                  className="w-full text-left p-2 bg-white/10 rounded hover:bg-white/20 transition-all text-xs text-gray-300 hover:text-white group"
                                >
                                  <div className="flex items-center justify-between">
                                    <span>{question}</span>
                                    <ArrowRight className="w-3 h-3 text-gray-400 group-hover:text-white transition-colors" />
                                  </div>
                                </button>
                              ))}
                            </div>
                          </div>
                        )}
                      </div>
                      
                      <div className="text-xs text-gray-400 mt-1">
                        {new Date(message.timestamp).toLocaleTimeString()}
                      </div>
                    </div>
                  </div>
                ))}
                
                {isTyping && (
                  <div className="flex gap-3 justify-start">
                    <div className="w-8 h-8 rounded-full bg-gradient-to-br from-purple-500 to-pink-600 flex items-center justify-center">
                      <Brain className="w-4 h-4 text-white animate-pulse" />
                    </div>
                    <div className="bg-white/10 text-white p-4 rounded-2xl">
                      <div className="flex items-center gap-2">
                        <Loader2 className="w-4 h-4 animate-spin" />
                        <span>Thinking...</span>
                      </div>
                    </div>
                  </div>
                )}
                
                <div ref={messagesEndRef} />
              </div>
            </div>

            {/* Input */}
            <div className="p-6 border-t border-white/10">
              <div className="flex gap-3">
                <input
                  ref={inputRef}
                  type="text"
                  value={inputMessage}
                  onChange={(e) => setInputMessage(e.target.value)}
                  onKeyPress={(e) => e.key === "Enter" && sendMessage(inputMessage)}
                  placeholder="Ask about your data..."
                  className="flex-1 px-4 py-3 bg-white/10 border border-white/20 rounded-xl text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                  disabled={isLoading}
                />
                <button
                  onClick={() => sendMessage(inputMessage)}
                  disabled={!inputMessage.trim() || isLoading}
                  className="px-6 py-3 bg-gradient-to-r from-purple-600 to-pink-600 text-white font-semibold rounded-xl hover:from-purple-500 hover:to-pink-500 transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2"
                >
                  {isLoading ? (
                    <Loader2 className="w-5 h-5 animate-spin" />
                  ) : (
                    <Send className="w-5 h-5" />
                  )}
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
