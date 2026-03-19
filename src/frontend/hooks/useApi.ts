"use client";

import { useState, useCallback, useEffect } from 'react';
import { EnhancedApiError, apiClient } from '@/services/enhancedApi';

interface UseApiOptions<T> {
  immediate?: boolean;
  onSuccess?: (data: T) => void;
  onError?: (error: EnhancedApiError) => void;
  retryCount?: number;
}

interface UseApiResult<T> {
  data: T | null;
  loading: boolean;
  error: EnhancedApiError | null;
  execute: (...args: any[]) => Promise<T | null>;
  reset: () => void;
  retry: () => void;
}

export function useApi<T>(
  apiFunction: (...args: any[]) => Promise<T>,
  options: UseApiOptions<T> = {}
): UseApiResult<T> {
  const [data, setData] = useState<T | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<EnhancedApiError | null>(null);
  const [retryCount, setRetryCount] = useState(0);

  const {
    immediate = false,
    onSuccess,
    onError,
    retryCount: maxRetries = 3
  } = options;

  const execute = useCallback(async (...args: any[]): Promise<T | null> => {
    try {
      setLoading(true);
      setError(null);
      
      const result = await apiFunction(...args);
      setData(result);
      setRetryCount(0);
      
      onSuccess?.(result);
      return result;
      
    } catch (err) {
      const apiError = err as EnhancedApiError;
      setError(apiError);
      onError?.(apiError);
      
      return null;
    } finally {
      setLoading(false);
    }
  }, [apiFunction, onSuccess, onError]);

  const retry = useCallback(() => {
    if (retryCount < maxRetries) {
      setRetryCount(prev => prev + 1);
      execute();
    }
  }, [execute, retryCount, maxRetries]);

  const reset = useCallback(() => {
    setData(null);
    setLoading(false);
    setError(null);
    setRetryCount(0);
  }, []);

  // Execute immediately if requested
  useEffect(() => {
    if (immediate) {
      execute();
    }
  }, [immediate, execute]);

  return {
    data,
    loading,
    error,
    execute,
    reset,
    retry
  };
}

// Hook for health checking
export function useHealthCheck(interval: number = 30000) {
  const [isOnline, setIsOnline] = useState(true);
  const [lastChecked, setLastChecked] = useState<Date | null>(null);

  useEffect(() => {
    const checkHealth = async () => {
      const isHealthy = await apiClient.healthCheck();
      setIsOnline(isHealthy);
      setLastChecked(new Date());
    };

    checkHealth();
    const intervalId = setInterval(checkHealth, interval);

    return () => clearInterval(intervalId);
  }, [interval]);

  return { isOnline, lastChecked };
}

// Hook for network status
export function useNetworkStatus() {
  const [isOnline, setIsOnline] = useState(
    typeof navigator !== 'undefined' ? navigator.onLine : true
  );

  useEffect(() => {
    if (typeof navigator === 'undefined') return;

    const handleOnline = () => setIsOnline(true);
    const handleOffline = () => setIsOnline(false);

    window.addEventListener('online', handleOnline);
    window.addEventListener('offline', handleOffline);

    return () => {
      window.removeEventListener('online', handleOnline);
      window.removeEventListener('offline', handleOffline);
    };
  }, []);

  return isOnline;
}

// Hook for error reporting
export function useErrorReporting() {
  const reportError = useCallback((error: EnhancedApiError, context?: string) => {
    // Log to console in development
    if (process.env.NODE_ENV === 'development') {
      console.error('API Error:', error, context);
    }

    // Send to monitoring service in production
    if (process.env.NODE_ENV === 'production' && typeof window !== 'undefined') {
      // Example: Send to analytics service
      if (window.gtag) {
        window.gtag('event', 'api_error', {
          error_message: error.message,
          error_status: error.status,
          error_context: context,
          is_network_error: error.isNetworkError,
          is_timeout: error.isTimeout
        });
      }

      // Example: Send to error tracking service
      // Sentry.captureException(error, { extra: { context } });
    }
  }, []);

  return { reportError };
}
