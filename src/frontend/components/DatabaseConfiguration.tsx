"use client";

import { useState, useEffect } from "react";
import {
  Database,
  Plus,
  TestTube,
  Settings,
  CheckCircle2,
  XCircle,
  X,
  AlertTriangle,
  Eye,
  EyeOff,
  Loader2,
  RefreshCw,
  Trash2,
  Edit,
  Play,
  BarChart3,
  Shield,
  Globe,
  Server,
  Key,
  Lock,
  Wifi,
  WifiOff,
  Copy,
  Download
} from "lucide-react";

interface DatabaseConfig {
  id: string;
  name: string;
  type: string;
  host?: string;
  port?: number;
  database: string;
  username?: string;
  password?: string;
  ssl_mode?: string;
  connection_string?: string;
  is_active: boolean;
  created_at?: string;
  last_tested?: string;
  status: string;
}

interface ConnectionTestResult {
  success: boolean;
  message: string;
  response_time_ms?: number;
  error_details?: string;
  schema_info?: Array<{
    table_name: string;
    columns: Array<{
      name: string;
      type: string;
      nullable: boolean;
      default: string;
    }>;
    row_count?: number;
    indexes?: any[];
    foreign_keys?: any[];
    primary_keys?: string[];
  }>;
  table_count?: number;
}

export default function DatabaseConfiguration() {
  const [configs, setConfigs] = useState<DatabaseConfig[]>([]);
  const [showAddForm, setShowAddForm] = useState(false);
  const [editingConfig, setEditingConfig] = useState<DatabaseConfig | null>(null);
  const [testingConnection, setTestingConnection] = useState<string | null>(null);
  const [connectionResults, setConnectionResults] = useState<{ [key: string]: ConnectionTestResult }>({});
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [selectedDatabase, setSelectedDatabase] = useState<string | null>(null);
  const [showPassword, setShowPassword] = useState<{ [key: string]: boolean }>({});

  // Form state
  const [formData, setFormData] = useState({
    name: "",
    type: "postgresql",
    host: "",
    port: "",
    database: "",
    username: "",
    password: "",
    ssl_mode: "prefer",
    connection_string: "",
    is_active: true
  });

  const databaseTypes = [
    { value: "postgresql", label: "PostgreSQL", icon: "🐘", defaultPort: 5432 },
    { value: "mysql", label: "MySQL", icon: "🐬", defaultPort: 3306 },
    { value: "sqlite", label: "SQLite", icon: "📁", defaultPort: null },
    { value: "mongodb", label: "MongoDB", icon: "🍃", defaultPort: 27017 },
    { value: "oracle", label: "Oracle", icon: "🏛️", defaultPort: 1521 },
    { value: "sqlserver", label: "SQL Server", icon: "🗄️", defaultPort: 1433 }
  ];

  const sslModes = [
    { value: "disable", label: "Disable SSL" },
    { value: "allow", label: "Allow SSL" },
    { value: "prefer", label: "Prefer SSL" },
    { value: "require", label: "Require SSL" },
    { value: "verify-ca", label: "Verify CA" },
    { value: "verify-full", label: "Verify Full" }
  ];

  useEffect(() => {
    loadConfigurations();
  }, []);

  const loadConfigurations = async () => {
    try {
      setLoading(true);
      const response = await fetch("/api/v1/database-config/configurations");
      const data = await response.json();
      
      if (data.success) {
        setConfigs(data.configurations);
      } else {
        setError("Failed to load configurations");
      }
    } catch (err) {
      setError("Error loading configurations");
    } finally {
      setLoading(false);
    }
  };

  const testConnection = async (configData?: any, configId?: string) => {
    const testData = configId 
      ? { config_id: configId }
      : configData;

    try {
      setTestingConnection(configId || "test");
      
      const endpoint = configId 
        ? `/api/v1/database-config/test-connection/${configId}`
        : "/api/v1/database-config/test-connection";
      
      const response = await fetch(endpoint, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(testData)
      });
      
      const result = await response.json();
      
      if (configId) {
        setConnectionResults(prev => ({ ...prev, [configId]: result }));
        // Reload configurations to update status
        await loadConfigurations();
      } else {
        setConnectionResults(prev => ({ ...prev, test: result }));
      }
      
    } catch (err) {
      const errorResult = {
        success: false,
        message: "Connection test failed",
        error_details: "Network error"
      };
      
      if (configId) {
        setConnectionResults(prev => ({ ...prev, [configId]: errorResult }));
      } else {
        setConnectionResults(prev => ({ ...prev, test: errorResult }));
      }
    } finally {
      setTestingConnection(null);
    }
  };

  const saveConfiguration = async () => {
    try {
      setLoading(true);
      setError(null);

      const endpoint = editingConfig 
        ? `/api/v1/database-config/configurations/${editingConfig.id}`
        : "/api/v1/database-config/configurations";
      
      const method = editingConfig ? "PUT" : "POST";
      
      const response = await fetch(endpoint, {
        method,
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(formData)
      });
      
      const data = await response.json();
      
      if (data.success) {
        setShowAddForm(false);
        setEditingConfig(null);
        resetForm();
        await loadConfigurations();
      } else {
        setError(data.detail || "Failed to save configuration");
      }
    } catch (err) {
      setError("Error saving configuration");
    } finally {
      setLoading(false);
    }
  };

  const deleteConfiguration = async (configId: string) => {
    if (!confirm("Are you sure you want to delete this database configuration?")) {
      return;
    }

    try {
      const response = await fetch(`/api/v1/database-config/configurations/${configId}`, {
        method: "DELETE"
      });
      
      const data = await response.json();
      
      if (data.success) {
        await loadConfigurations();
      } else {
        setError("Failed to delete configuration");
      }
    } catch (err) {
      setError("Error deleting configuration");
    }
  };

  const switchDatabase = async (configId: string) => {
    try {
      const response = await fetch(`/api/v1/database-config/switch/${configId}`, {
        method: "POST"
      });
      
      const data = await response.json();
      
      if (data.success) {
        setSelectedDatabase(configId);
      } else {
        setError("Failed to switch database");
      }
    } catch (err) {
      setError("Error switching database");
    }
  };

  const resetForm = () => {
    setFormData({
      name: "",
      type: "postgresql",
      host: "",
      port: "",
      database: "",
      username: "",
      password: "",
      ssl_mode: "prefer",
      connection_string: "",
      is_active: true
    });
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case "connected":
        return <CheckCircle2 className="w-4 h-4 text-green-500" />;
      case "error":
        return <XCircle className="w-4 h-4 text-red-500" />;
      case "testing":
        return <Loader2 className="w-4 h-4 text-blue-500 animate-spin" />;
      default:
        return <WifiOff className="w-4 h-4 text-gray-500" />;
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case "connected":
        return "text-green-500 bg-green-500/10 border-green-500/30";
      case "error":
        return "text-red-500 bg-red-500/10 border-red-500/30";
      case "testing":
        return "text-blue-500 bg-blue-500/10 border-blue-500/30";
      default:
        return "text-gray-500 bg-gray-500/10 border-gray-500/30";
    }
  };

  const selectedDb = databaseTypes.find(db => db.value === formData.type);

  return (
    <div className="max-w-7xl mx-auto animate-fade-in">
      <div className="mb-8">
        <div className="flex items-center justify-between mb-3">
          <div className="flex items-center gap-3">
            <div className="w-12 h-12 rounded-2xl bg-gradient-to-br from-blue-500 to-cyan-600 flex items-center justify-center shadow-lg shadow-blue-500/20">
              <Database className="w-6 h-6 text-white" />
            </div>
            <div>
              <h1 className="text-3xl font-bold text-white tracking-tight">
                Database Configuration
              </h1>
              <p className="text-slate-400">
                Manage and connect to multiple company databases
              </p>
            </div>
          </div>
          
          <button
            onClick={() => setShowAddForm(true)}
            className="px-6 py-3 bg-gradient-to-r from-blue-600 to-cyan-600 text-white font-semibold rounded-xl hover:from-blue-500 hover:to-cyan-500 transition-all duration-300 flex items-center gap-2 shadow-xl shadow-blue-500/25"
          >
            <Plus className="w-5 h-5" />
            Add Database
          </button>
        </div>
      </div>

      {/* Error Display */}
      {error && (
        <div className="glass rounded-2xl p-6 border border-red-500/30 bg-red-500/10 mb-8">
          <div className="flex items-center gap-3 text-red-400">
            <AlertTriangle className="w-6 h-6" />
            <p className="text-lg font-medium">{error}</p>
            <button onClick={() => setError(null)} className="ml-auto">
              <X className="w-5 h-5" />
            </button>
          </div>
        </div>
      )}

      {/* Database Configurations List */}
      <div className="space-y-6">
        {configs.map((config) => (
          <div key={config.id} className="glass rounded-2xl p-6 border border-white/10">
            <div className="flex items-start justify-between mb-4">
              <div className="flex items-center gap-4">
                <div className="w-12 h-12 rounded-xl bg-white/10 flex items-center justify-center text-2xl">
                  {databaseTypes.find(db => db.value === config.type)?.icon || "🗄️"}
                </div>
                <div>
                  <h3 className="text-xl font-semibold text-white flex items-center gap-2">
                    {config.name}
                    {selectedDatabase === config.id && (
                      <span className="px-2 py-1 bg-blue-500/20 text-blue-400 text-xs rounded-full">
                        Active
                      </span>
                    )}
                  </h3>
                  <div className="flex items-center gap-4 text-sm text-gray-400 mt-1">
                    <span className="capitalize">{config.type}</span>
                    {config.host && <span>• {config.host}:{config.port}</span>}
                    <span>• {config.database}</span>
                  </div>
                </div>
              </div>
              
              <div className="flex items-center gap-2">
                <span className={`px-3 py-1 rounded-full text-xs font-medium flex items-center gap-1 border ${getStatusColor(config.status)}`}>
                  {getStatusIcon(config.status)}
                  {config.status}
                </span>
              </div>
            </div>

            {/* Connection Test Result */}
            {connectionResults[config.id] && (
              <div className={`mb-4 p-4 rounded-xl border ${
                connectionResults[config.id].success 
                  ? "bg-green-500/10 border-green-500/30" 
                  : "bg-red-500/10 border-red-500/30"
              }`}>
                <div className="flex items-start gap-3">
                  {connectionResults[config.id].success ? (
                    <CheckCircle2 className="w-5 h-5 text-green-500 mt-0.5" />
                  ) : (
                    <XCircle className="w-5 h-5 text-red-500 mt-0.5" />
                  )}
                  <div className="flex-1">
                    <p className={`font-medium ${
                      connectionResults[config.id].success ? "text-green-400" : "text-red-400"
                    }`}>
                      {connectionResults[config.id].message}
                    </p>
                    {connectionResults[config.id]?.response_time_ms && (
                      <p className="text-sm text-gray-400 mt-1">
                        Response time: {connectionResults[config.id]!.response_time_ms.toFixed(2)}ms
                      </p>
                    )}
                    {connectionResults[config.id].schema_info && (
                      <p className="text-sm text-gray-400 mt-1">
                        Discovered {connectionResults[config.id].schema_info.length} tables
                      </p>
                    )}
                    {connectionResults[config.id].error_details && (
                      <p className="text-sm text-red-300 mt-2">
                        {connectionResults[config.id].error_details}
                      </p>
                    )}
                  </div>
                </div>
              </div>
            )}

            {/* Actions */}
            <div className="flex items-center gap-3">
              <button
                onClick={() => testConnection(null, config.id)}
                disabled={testingConnection === config.id}
                className="px-4 py-2 bg-white/10 text-white rounded-lg hover:bg-white/20 transition-all flex items-center gap-2 disabled:opacity-50"
              >
                {testingConnection === config.id ? (
                  <Loader2 className="w-4 h-4 animate-spin" />
                ) : (
                  <TestTube className="w-4 h-4" />
                )}
                Test Connection
              </button>
              
              <button
                onClick={() => switchDatabase(config.id)}
                className="px-4 py-2 bg-white/10 text-white rounded-lg hover:bg-white/20 transition-all flex items-center gap-2"
              >
                <Play className="w-4 h-4" />
                Switch
              </button>
              
              <button
                onClick={() => {
                  setEditingConfig(config);
                  setFormData({
                    name: config.name,
                    type: config.type,
                    host: config.host || "",
                    port: config.port?.toString() || "",
                    database: config.database,
                    username: config.username || "",
                    password: "",
                    ssl_mode: config.ssl_mode || "prefer",
                    connection_string: config.connection_string || "",
                    is_active: config.is_active
                  });
                  setShowAddForm(true);
                }}
                className="px-4 py-2 bg-white/10 text-white rounded-lg hover:bg-white/20 transition-all flex items-center gap-2"
              >
                <Edit className="w-4 h-4" />
                Edit
              </button>
              
              <button
                onClick={() => deleteConfiguration(config.id)}
                className="px-4 py-2 bg-red-500/20 text-red-400 rounded-lg hover:bg-red-500/30 transition-all flex items-center gap-2"
              >
                <Trash2 className="w-4 h-4" />
                Delete
              </button>
            </div>
          </div>
        ))}
        
        {configs.length === 0 && !loading && (
          <div className="glass rounded-2xl p-12 border border-white/10 text-center">
            <Database className="w-16 h-16 text-gray-500 mx-auto mb-4" />
            <h3 className="text-xl font-semibold text-white mb-2">No Database Configurations</h3>
            <p className="text-gray-400 mb-6">
              Add your first database configuration to get started with data analysis.
            </p>
            <button
              onClick={() => setShowAddForm(true)}
              className="px-6 py-3 bg-gradient-to-r from-blue-600 to-cyan-600 text-white font-semibold rounded-xl hover:from-blue-500 hover:to-cyan-500 transition-all duration-300 flex items-center gap-2 mx-auto"
            >
              <Plus className="w-5 h-5" />
              Add Your First Database
            </button>
          </div>
        )}
      </div>

      {/* Add/Edit Database Form */}
      {(showAddForm || editingConfig) && (
        <div className="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center z-50 p-4">
          <div className="glass rounded-3xl p-8 border border-white/10 max-w-2xl w-full max-h-[90vh] overflow-y-auto">
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-2xl font-bold text-white">
                {editingConfig ? "Edit Database" : "Add Database Configuration"}
              </h2>
              <button
                onClick={() => {
                  setShowAddForm(false);
                  setEditingConfig(null);
                  resetForm();
                }}
                className="text-gray-400 hover:text-white"
              >
                <X className="w-6 h-6" />
              </button>
            </div>

            {/* Connection Test Result for New Config */}
            {connectionResults.test && (
              <div className={`mb-6 p-4 rounded-xl border ${
                connectionResults.test.success 
                  ? "bg-green-500/10 border-green-500/30" 
                  : "bg-red-500/10 border-red-500/30"
              }`}>
                <div className="flex items-start gap-3">
                  {connectionResults.test.success ? (
                    <CheckCircle2 className="w-5 h-5 text-green-500 mt-0.5" />
                  ) : (
                    <XCircle className="w-5 h-5 text-red-500 mt-0.5" />
                  )}
                  <div className="flex-1">
                    <p className={`font-medium ${
                      connectionResults.test.success ? "text-green-400" : "text-red-400"
                    }`}>
                      {connectionResults.test.message}
                    </p>
                    {connectionResults.test.response_time_ms && (
                      <p className="text-sm text-gray-400 mt-1">
                        Response time: {connectionResults.test.response_time_ms.toFixed(2)}ms
                      </p>
                    )}
                    {connectionResults.test.schema_info && (
                      <p className="text-sm text-gray-400 mt-1">
                        Discovered {connectionResults.test.schema_info.length} tables
                      </p>
                    )}
                    {connectionResults.test.error_details && (
                      <p className="text-sm text-red-300 mt-2">
                        {connectionResults.test.error_details}
                      </p>
                    )}
                  </div>
                </div>
              </div>
            )}

            <div className="space-y-6">
              {/* Basic Information */}
              <div>
                <label className="block text-sm font-medium text-gray-300 mb-2">
                  Configuration Name *
                </label>
                <input
                  type="text"
                  value={formData.name}
                  onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                  className="w-full px-4 py-3 bg-white/5 border border-white/20 rounded-xl text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  placeholder="e.g., Production Database"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-300 mb-2">
                  Database Type *
                </label>
                <div className="grid grid-cols-3 gap-3">
                  {databaseTypes.map((db) => (
                    <button
                      key={db.value}
                      type="button"
                      onClick={() => {
                        setFormData({ 
                          ...formData, 
                          type: db.value,
                          port: db.defaultPort?.toString() || ""
                        });
                      }}
                      className={`p-3 rounded-xl border transition-all flex items-center gap-2 ${
                        formData.type === db.value
                          ? "bg-blue-500/20 border-blue-500 text-white"
                          : "bg-white/5 border-white/20 text-gray-300 hover:bg-white/10"
                      }`}
                    >
                      <span className="text-xl">{db.icon}</span>
                      <span className="text-sm">{db.label}</span>
                    </button>
                  ))}
                </div>
              </div>

              {/* Connection String Option */}
              <div>
                <label className="flex items-center gap-2 text-sm font-medium text-gray-300 mb-2">
                  <input
                    type="checkbox"
                    checked={!!formData.connection_string}
                    onChange={(e) => {
                      if (e.target.checked) {
                        setFormData({ ...formData, connection_string: "postgresql://username:password@host:port/database" });
                      } else {
                        setFormData({ ...formData, connection_string: "" });
                      }
                    }}
                    className="rounded"
                  />
                  Use Connection String
                </label>
              </div>

              {formData.connection_string ? (
                <div>
                  <label className="block text-sm font-medium text-gray-300 mb-2">
                    Connection String *
                  </label>
                  <input
                    type="text"
                    value={formData.connection_string}
                    onChange={(e) => setFormData({ ...formData, connection_string: e.target.value })}
                    className="w-full px-4 py-3 bg-white/5 border border-white/20 rounded-xl text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent font-mono text-sm"
                    placeholder="postgresql://username:password@host:port/database"
                  />
                </div>
              ) : (
                <>
                  {/* Individual Connection Parameters */}
                  {selectedDb?.value !== "sqlite" && (
                    <>
                      <div className="grid grid-cols-2 gap-4">
                        <div>
                          <label className="block text-sm font-medium text-gray-300 mb-2">
                            Host *
                          </label>
                          <input
                            type="text"
                            value={formData.host}
                            onChange={(e) => setFormData({ ...formData, host: e.target.value })}
                            className="w-full px-4 py-3 bg-white/5 border border-white/20 rounded-xl text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                            placeholder="localhost"
                          />
                        </div>
                        <div>
                          <label className="block text-sm font-medium text-gray-300 mb-2">
                            Port
                          </label>
                          <input
                            type="number"
                            value={formData.port}
                            onChange={(e) => setFormData({ ...formData, port: e.target.value })}
                            className="w-full px-4 py-3 bg-white/5 border border-white/20 rounded-xl text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                            placeholder={selectedDb?.defaultPort?.toString()}
                          />
                        </div>
                      </div>

                      <div>
                        <label className="block text-sm font-medium text-gray-300 mb-2">
                          Username *
                        </label>
                        <input
                          type="text"
                          value={formData.username}
                          onChange={(e) => setFormData({ ...formData, username: e.target.value })}
                          className="w-full px-4 py-3 bg-white/5 border border-white/20 rounded-xl text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                          placeholder="database_user"
                        />
                      </div>

                      <div>
                        <label className="block text-sm font-medium text-gray-300 mb-2">
                          Password
                        </label>
                        <div className="relative">
                          <input
                            type={showPassword.password ? "text" : "password"}
                            value={formData.password}
                            onChange={(e) => setFormData({ ...formData, password: e.target.value })}
                            className="w-full px-4 py-3 bg-white/5 border border-white/20 rounded-xl text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent pr-12"
                            placeholder="••••••••"
                          />
                          <button
                            type="button"
                            onClick={() => setShowPassword({ ...showPassword, password: !showPassword.password })}
                            className="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-400 hover:text-white"
                          >
                            {showPassword.password ? <EyeOff className="w-5 h-5" /> : <Eye className="w-5 h-5" />}
                          </button>
                        </div>
                      </div>

                      <div>
                        <label className="block text-sm font-medium text-gray-300 mb-2">
                          SSL Mode
                        </label>
                        <select
                          value={formData.ssl_mode}
                          onChange={(e) => setFormData({ ...formData, ssl_mode: e.target.value })}
                          className="w-full px-4 py-3 bg-white/5 border border-white/20 rounded-xl text-white focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                        >
                          {sslModes.map((mode) => (
                            <option key={mode.value} value={mode.value}>
                              {mode.label}
                            </option>
                          ))}
                        </select>
                      </div>
                    </>
                  )}

                  <div>
                    <label className="block text-sm font-medium text-gray-300 mb-2">
                      {selectedDb?.value === "sqlite" ? "Database File Path *" : "Database Name *"}
                    </label>
                    <input
                      type="text"
                      value={formData.database}
                      onChange={(e) => setFormData({ ...formData, database: e.target.value })}
                      className="w-full px-4 py-3 bg-white/5 border border-white/20 rounded-xl text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                      placeholder={selectedDb?.value === "sqlite" ? "/path/to/database.db" : "database_name"}
                    />
                  </div>
                </>
              )}

              {/* Actions */}
              <div className="flex items-center gap-4 pt-6 border-t border-white/10">
                <button
                  onClick={() => testConnection(formData)}
                  disabled={testingConnection === "test" || !formData.name || !formData.database}
                  className="px-6 py-3 bg-white/10 text-white rounded-xl hover:bg-white/20 transition-all flex items-center gap-2 disabled:opacity-50"
                >
                  {testingConnection === "test" ? (
                    <Loader2 className="w-5 h-5 animate-spin" />
                  ) : (
                    <TestTube className="w-5 h-5" />
                  )}
                  Test Connection
                </button>

                <button
                  onClick={saveConfiguration}
                  disabled={loading || !formData.name || !formData.database}
                  className="px-6 py-3 bg-gradient-to-r from-blue-600 to-cyan-600 text-white font-semibold rounded-xl hover:from-blue-500 hover:to-cyan-500 transition-all disabled:opacity-50"
                >
                  {loading ? (
                    <Loader2 className="w-5 h-5 animate-spin" />
                  ) : (
                    <>{editingConfig ? "Update" : "Save"} Configuration</>
                  )}
                </button>

                <button
                  onClick={() => {
                    setShowAddForm(false);
                    setEditingConfig(null);
                    resetForm();
                  }}
                  className="px-6 py-3 bg-white/10 text-white rounded-xl hover:bg-white/20 transition-all"
                >
                  Cancel
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
