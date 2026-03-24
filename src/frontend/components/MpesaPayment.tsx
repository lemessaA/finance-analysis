/**
 * M-Pesa Payment Component
 * 
 * React component for M-Pesa payment integration with STK Push,
 * transaction status, and payment history functionality.
 */

"use client";

import { useState, useEffect } from "react";
import { 
  Smartphone, 
  CheckCircle, 
  AlertCircle, 
  Clock, 
  History,
  RefreshCw,
  User,
  CreditCard,
  Shield,
  TrendingUp
} from "lucide-react";
import { apiClient } from "@/services/enhancedApi";

interface PaymentRequest {
  phone_number: string;
  amount: number;
  account_reference: string;
  transaction_desc: string;
}

interface Transaction {
  id: string;
  phone_number: string;
  amount: number;
  account_reference: string;
  transaction_desc: string;
  status: "pending" | "completed" | "failed";
  created_at: string;
  checkout_request_id?: string;
  mpesa_transaction_id?: string;
  completed_at?: string;
}

interface PaymentHistoryResponse {
  payments: Transaction[];
  total_count: number;
  page: number;
  per_page: number;
}

export default function MpesaPayment() {
  const [activeTab, setActiveTab] = useState<"payment" | "history" | "status">("payment");
  const [paymentForm, setPaymentForm] = useState<PaymentRequest>({
    phone_number: "",
    amount: 0,
    account_reference: "",
    transaction_desc: ""
  });
  const [isLoading, setIsLoading] = useState(false);
  const [message, setMessage] = useState<{ type: "success" | "error" | "info"; text: string } | null>(null);
  const [transactions, setTransactions] = useState<Transaction[]>([]);
  const [transactionId, setTransactionId] = useState("");
  const [statusResult, setStatusResult] = useState<any>(null);
  const [currentPage, setCurrentPage] = useState(1);
  const [balance, setBalance] = useState<any>(null);

  // Load payment history
  useEffect(() => {
    if (activeTab === "history") {
      loadPaymentHistory();
    }
  }, [activeTab, currentPage]);

  // Load account balance
  useEffect(() => {
    loadAccountBalance();
  }, []);

  const loadPaymentHistory = async () => {
    try {
      const response = await apiClient.get(`/api/v1/mpesa/payment-history?page=${currentPage}&per_page=10`);
      setTransactions(response.data.payments);
    } catch (error: any) {
      setMessage({
        type: "error",
        text: error?.response?.data?.detail || "Failed to load payment history"
      });
    }
  };

  const loadAccountBalance = async () => {
    try {
      const response = await apiClient.get("/api/v1/mpesa/balance");
      setBalance(response.data);
    } catch (error: any) {
      console.error("Failed to load balance:", error);
    }
  };

  const handlePaymentSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    // Validation
    if (!paymentForm.phone_number || !paymentForm.amount || !paymentForm.account_reference) {
      setMessage({
        type: "error",
        text: "Please fill in all required fields"
      });
      return;
    }

    if (!paymentForm.phone_number.startsWith("251") || paymentForm.phone_number.length !== 12) {
      setMessage({
        type: "error",
        text: "Please enter a valid Ethiopian phone number (251XXXXXXXXX)"
      });
      return;
    }

    if (paymentForm.amount < 1 || paymentForm.amount > 150000) {
      setMessage({
        type: "error",
        text: "Amount must be between ETB 1 and ETB 150,000"
      });
      return;
    }

    setIsLoading(true);
    setMessage(null);

    try {
      const response = await apiClient.post("/api/v1/mpesa/stk-push", paymentForm);
      
      setMessage({
        type: "success",
        text: response.data.customer_message || "Payment request sent successfully! Please check your phone."
      });
      
      // Reset form
      setPaymentForm({
        phone_number: "",
        amount: 0,
        account_reference: "",
        transaction_desc: ""
      });
      
      // Load updated history
      if (activeTab === "history") {
        loadPaymentHistory();
      }
      
    } catch (error: any) {
      setMessage({
        type: "error",
        text: error?.response?.data?.detail || "Payment failed. Please try again."
      });
    } finally {
      setIsLoading(false);
    }
  };

  const handleStatusCheck = async () => {
    if (!transactionId.trim()) {
      setMessage({
        type: "error",
        text: "Please enter a transaction ID"
      });
      return;
    }

    setIsLoading(true);
    setStatusResult(null);

    try {
      const response = await apiClient.post("/api/v1/mpesa/transaction-status", {
        checkout_request_id: transactionId
      });
      
      setStatusResult(response.data);
      setMessage({
        type: "info",
        text: response.data.message || "Status retrieved successfully"
      });
      
    } catch (error: any) {
      setMessage({
        type: "error",
        text: error?.response?.data?.detail || "Failed to check transaction status"
      });
    } finally {
      setIsLoading(false);
    }
  };

  const formatAmount = (amount: number) => {
    return new Intl.NumberFormat("en-ET", {
      style: "currency",
      currency: "ETB"
    }).format(amount);
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleString();
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case "completed":
        return "text-green-500 bg-green-500/10 border-green-500/20";
      case "failed":
        return "text-red-500 bg-red-500/10 border-red-500/20";
      default:
        return "text-yellow-500 bg-yellow-500/10 border-yellow-500/20";
    }
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case "completed":
        return <CheckCircle className="w-4 h-4" />;
      case "failed":
        return <AlertCircle className="w-4 h-4" />;
      default:
        return <Clock className="w-4 h-4" />;
    }
  };

  return (
    <div className="max-w-6xl mx-auto animate-fade-in">
      {/* Header */}
      <div className="mb-8">
        <div className="flex items-center gap-3 mb-3">
          <div className="w-12 h-12 rounded-2xl bg-gradient-to-br from-green-500 to-emerald-600 flex items-center justify-center shadow-lg shadow-green-500/20">
            <Smartphone className="w-6 h-6 text-white" />
          </div>
          <h1 className="text-3xl font-bold text-white tracking-tight">
            M-Pesa Payment Integration
          </h1>
        </div>
        <p className="text-slate-400 max-w-2xl text-lg">
          Accept M-Pesa payments directly through your application using Safaricom's Daraja API.
        </p>
      </div>

      {/* Balance Card */}
      {balance && (
        <div className="glass rounded-2xl p-6 mb-8 border border-emerald-500/20 bg-emerald-500/5">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="p-2 bg-emerald-500/20 rounded-lg">
                <TrendingUp className="w-5 h-5 text-emerald-500" />
              </div>
              <div>
                <p className="text-sm text-gray-400">Available Balance</p>
                <p className="text-2xl font-bold text-white">
                  {formatAmount(balance.available_balance)}
                </p>
              </div>
            </div>
            <button
              onClick={loadAccountBalance}
              className="p-2 text-emerald-400 hover:text-emerald-300 transition-colors"
            >
              <RefreshCw className="w-5 h-5" />
            </button>
          </div>
        </div>
      )}

      {/* Navigation Tabs */}
      <div className="flex items-center gap-2 bg-white/10 rounded-xl p-1 mb-8">
        <button
          onClick={() => setActiveTab("payment")}
          className={`px-4 py-2 rounded-lg transition-all flex items-center gap-2 ${
            activeTab === "payment"
              ? "bg-green-600 text-white"
              : "text-gray-300 hover:text-white"
          }`}
        >
          <CreditCard className="w-4 h-4" />
          Make Payment
        </button>
        <button
          onClick={() => setActiveTab("status")}
          className={`px-4 py-2 rounded-lg transition-all flex items-center gap-2 ${
            activeTab === "status"
              ? "bg-blue-600 text-white"
              : "text-gray-300 hover:text-white"
          }`}
        >
          <Clock className="w-4 h-4" />
          Check Status
        </button>
        <button
          onClick={() => setActiveTab("history")}
          className={`px-4 py-2 rounded-lg transition-all flex items-center gap-2 ${
            activeTab === "history"
              ? "bg-purple-600 text-white"
              : "text-gray-300 hover:text-white"
          }`}
        >
          <History className="w-4 h-4" />
          History
        </button>
      </div>

      {/* Messages */}
      {message && (
        <div className={`glass rounded-2xl p-4 mb-6 border ${
          message.type === "success" ? "border-green-500/30 bg-green-500/10" :
          message.type === "error" ? "border-red-500/30 bg-red-500/10" :
          "border-blue-500/30 bg-blue-500/10"
        }`}>
          <div className="flex items-center gap-3">
            {message.type === "success" && <CheckCircle className="w-5 h-5 text-green-500" />}
            {message.type === "error" && <AlertCircle className="w-5 h-5 text-red-500" />}
            {message.type === "info" && <Clock className="w-5 h-5 text-blue-500" />}
            <p className={`${
              message.type === "success" ? "text-green-400" :
              message.type === "error" ? "text-red-400" :
              "text-blue-400"
            }`}>{message.text}</p>
          </div>
        </div>
      )}

      {/* Payment Form Tab */}
      {activeTab === "payment" && (
        <div className="glass rounded-3xl p-8 mb-10 border border-white/5 shadow-2xl">
          <form onSubmit={handlePaymentSubmit} className="space-y-6">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <label className="block text-sm font-medium text-slate-300 mb-2">
                  Phone Number <span className="text-green-400">*</span>
                </label>
                <div className="relative">
                  <input
                    type="tel"
                    placeholder="251XXXXXXXXX"
                    value={paymentForm.phone_number}
                    onChange={(e) => setPaymentForm({...paymentForm, phone_number: e.target.value})}
                    className="w-full px-4 py-3 bg-white/10 border border-white/10 rounded-xl text-white placeholder-gray-400 focus:border-green-500/50 focus:outline-none transition-all"
                    required
                  />
                  <Smartphone className="absolute right-3 top-3.5 w-5 h-5 text-gray-400" />
                </div>
              </div>

              <div>
                <label className="block text-sm font-medium text-slate-300 mb-2">
                  Amount (ETB) <span className="text-green-400">*</span>
                </label>
                <div className="relative">
                  <input
                    type="number"
                    placeholder="100"
                    min="1"
                    max="150000"
                    value={paymentForm.amount || ""}
                    onChange={(e) => setPaymentForm({...paymentForm, amount: parseInt(e.target.value) || 0})}
                    className="w-full px-4 py-3 bg-white/10 border border-white/10 rounded-xl text-white placeholder-gray-400 focus:border-green-500/50 focus:outline-none transition-all"
                    required
                  />
                  <CreditCard className="absolute right-3 top-3.5 w-5 h-5 text-gray-400" />
                </div>
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium text-slate-300 mb-2">
                Account Reference <span className="text-green-400">*</span>
              </label>
              <input
                type="text"
                placeholder="Invoice #12345"
                value={paymentForm.account_reference}
                onChange={(e) => setPaymentForm({...paymentForm, account_reference: e.target.value})}
                className="w-full px-4 py-3 bg-white/10 border border-white/10 rounded-xl text-white placeholder-gray-400 focus:border-green-500/50 focus:outline-none transition-all"
                required
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-slate-300 mb-2">
                Transaction Description <span className="text-green-400">*</span>
              </label>
              <input
                type="text"
                placeholder="Payment for goods/services"
                value={paymentForm.transaction_desc}
                onChange={(e) => setPaymentForm({...paymentForm, transaction_desc: e.target.value})}
                className="w-full px-4 py-3 bg-white/10 border border-white/10 rounded-xl text-white placeholder-gray-400 focus:border-green-500/50 focus:outline-none transition-all"
                required
              />
            </div>

            <button
              type="submit"
              disabled={isLoading}
              className="w-full h-14 px-8 bg-gradient-to-r from-green-600 to-emerald-600 text-white font-semibold rounded-2xl hover:from-green-500 hover:to-emerald-500 transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed shadow-xl shadow-green-500/25 flex items-center justify-center gap-2 whitespace-nowrap text-lg"
            >
              {isLoading ? (
                <div className="flex items-center gap-2">
                  <div className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin"></div>
                  <span>Processing...</span>
                </div>
              ) : (
                <div className="flex items-center gap-2">
                  <Smartphone className="w-5 h-5" />
                  <span>Send Payment Request</span>
                </div>
              )}
            </button>
          </form>
        </div>
      )}

      {/* Status Check Tab */}
      {activeTab === "status" && (
        <div className="glass rounded-3xl p-8 mb-10 border border-white/5 shadow-2xl">
          <div className="space-y-6">
            <div>
              <label className="block text-sm font-medium text-slate-300 mb-2">
                Transaction ID / Checkout Request ID
              </label>
              <div className="flex gap-3">
                <input
                  type="text"
                  placeholder="ws_CO_123456789"
                  value={transactionId}
                  onChange={(e) => setTransactionId(e.target.value)}
                  className="flex-1 px-4 py-3 bg-white/10 border border-white/10 rounded-xl text-white placeholder-gray-400 focus:border-blue-500/50 focus:outline-none transition-all"
                />
                <button
                  onClick={handleStatusCheck}
                  disabled={isLoading}
                  className="h-14 px-6 bg-gradient-to-r from-blue-600 to-indigo-600 text-white font-semibold rounded-2xl hover:from-blue-500 hover:to-indigo-500 transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed shadow-xl shadow-blue-500/25 flex items-center justify-center gap-2 whitespace-nowrap"
                >
                  {isLoading ? (
                    <div className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin"></div>
                  ) : (
                    <RefreshCw className="w-5 h-5" />
                  )}
                </button>
              </div>
            </div>

            {statusResult && (
              <div className={`glass rounded-2xl p-6 border ${
                statusResult.success ? "border-green-500/30 bg-green-500/10" : "border-red-500/30 bg-red-500/10"
              }`}>
                <div className="flex items-center gap-3 mb-4">
                  {statusResult.success ? (
                    <CheckCircle className="w-6 h-6 text-green-500" />
                  ) : (
                    <AlertCircle className="w-6 h-6 text-red-500" />
                  )}
                  <div>
                    <h3 className="text-lg font-semibold text-white">
                      {statusResult.success ? "Transaction Successful" : "Transaction Failed"}
                    </h3>
                    <p className="text-sm text-gray-400">{statusResult.message}</p>
                  </div>
                </div>
                
                {statusResult.checkout_request_id && (
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
                    <div>
                      <span className="text-gray-400">Checkout Request ID:</span>
                      <p className="text-white font-mono">{statusResult.checkout_request_id}</p>
                    </div>
                    {statusResult.response_code && (
                      <div>
                        <span className="text-gray-400">Response Code:</span>
                        <p className="text-white font-mono">{statusResult.response_code}</p>
                      </div>
                    )}
                  </div>
                )}
              </div>
            )}
          </div>
        </div>
      )}

      {/* Payment History Tab */}
      {activeTab === "history" && (
        <div className="glass rounded-3xl p-8 border border-white/5 shadow-2xl">
          <h3 className="text-xl font-semibold text-white mb-6 flex items-center gap-3">
            <History className="w-6 h-6 text-purple-500" />
            Payment History
          </h3>
          
          {transactions.length === 0 ? (
            <div className="text-center py-12">
              <History className="w-12 h-12 text-gray-400 mx-auto mb-4" />
              <p className="text-gray-400">No payment transactions found</p>
            </div>
          ) : (
            <div className="space-y-4">
              {transactions.map((transaction) => (
                <div key={transaction.id} className="bg-white/5 rounded-xl p-4 border border-white/10">
                  <div className="flex items-center justify-between">
                    <div className="flex-1">
                      <div className="flex items-center gap-3 mb-2">
                        {getStatusIcon(transaction.status)}
                        <span className={`font-medium ${getStatusColor(transaction.status).split(" ")[0]}`}>
                          {transaction.status.charAt(0).toUpperCase() + transaction.status.slice(1)}
                        </span>
                        <span className="text-gray-400 text-sm ml-2">
                          {formatAmount(transaction.amount)}
                        </span>
                      </div>
                      <div className="text-sm text-gray-400">
                        <p>Phone: {transaction.phone_number}</p>
                        <p>Ref: {transaction.account_reference}</p>
                        <p>Date: {formatDate(transaction.created_at)}</p>
                        {transaction.mpesa_transaction_id && (
                          <p>M-Pesa ID: {transaction.mpesa_transaction_id}</p>
                        )}
                      </div>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
          
          {/* Pagination */}
          {transactions.length > 0 && (
            <div className="flex justify-center items-center gap-4 mt-6">
              <button
                onClick={() => setCurrentPage(Math.max(1, currentPage - 1))}
                disabled={currentPage <= 1}
                className="px-4 py-2 bg-white/10 rounded-lg hover:bg-white/20 disabled:opacity-50 disabled:cursor-not-allowed transition-all"
              >
                Previous
              </button>
              <span className="text-gray-400">
                Page {currentPage}
              </span>
              <button
                onClick={() => setCurrentPage(currentPage + 1)}
                className="px-4 py-2 bg-white/10 rounded-lg hover:bg-white/20 transition-all"
              >
                Next
              </button>
            </div>
          )}
        </div>
      )}

      {/* Security Notice */}
      <div className="glass rounded-2xl p-6 border border-blue-500/20 bg-blue-500/5">
        <div className="flex items-center gap-3">
          <Shield className="w-6 h-6 text-blue-500" />
          <div>
            <h3 className="text-lg font-semibold text-white mb-2">Security Notice</h3>
            <p className="text-sm text-gray-300 leading-relaxed">
              This payment system is secured by Safaricom's M-Pesa API. All transactions are encrypted and processed through official channels. 
              Never share your M-Pesa PIN with anyone.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
