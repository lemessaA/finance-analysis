import axios, { AxiosInstance, AxiosError, AxiosRequestConfig, AxiosResponse, InternalAxiosRequestConfig } from 'axios';
import type { ApiError } from '@/types';

// Enhanced error types
export interface EnhancedApiError extends ApiError {
  message: string;
  isNetworkError?: boolean;
  isTimeout?: boolean;
  isServerError?: boolean;
  isClientError?: boolean;
  retryCount?: number;
}

// Retry configuration
interface RetryConfig {
  maxRetries: number;
  retryDelay: number;
  retryCondition?: (error: AxiosError) => boolean;
}

// Extended request config with metadata
interface ExtendedAxiosRequestConfig extends InternalAxiosRequestConfig {
  metadata?: {
    startTime?: Date;
  };
  __retryCount?: number;
}

class ApiClient {
  private client: AxiosInstance;
  private retryConfig: RetryConfig;

  constructor() {
    this.retryConfig = {
      maxRetries: 3,
      retryDelay: 1000,
      retryCondition: (error: AxiosError) => {
        // Retry on network errors, 5xx server errors, and 429 rate limiting
        return !error.response ||
          error.response.status >= 500 ||
          error.response.status === 429 ||
          error.code === 'NETWORK_ERROR' ||
          error.code === 'TIMEOUT';
      }
    };

    this.client = axios.create({
      baseURL: process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000",
      timeout: 120000, // 2 min — agents take time
      headers: { "Content-Type": "application/json" },
    });

    this.setupInterceptors();
  }

  private setupInterceptors() {
    // Request interceptor
    this.client.interceptors.request.use(
      (config: ExtendedAxiosRequestConfig) => {
        // Add request timestamp for debugging
        config.metadata = { startTime: new Date() };
        return config;
      },
      (error) => {
        return Promise.reject(this.enhanceError(error));
      }
    );

    // Response interceptor
    this.client.interceptors.response.use(
      (response) => {
        // Log successful requests in development
        if (process.env.NODE_ENV === 'development') {
          const config = response.config as ExtendedAxiosRequestConfig;
          const duration = config.metadata?.startTime ?
            new Date().getTime() - config.metadata.startTime.getTime() : 0;
          console.log(`✅ API Request: ${response.config.method?.toUpperCase()} ${response.config.url} (${duration}ms)`);
        }
        return response;
      },
      (error) => {
        const enhancedError = this.enhanceError(error);

        // Log failed requests in development
        if (process.env.NODE_ENV === 'development') {
          const config = error.config as ExtendedAxiosRequestConfig;
          const duration = config.metadata?.startTime ?
            new Date().getTime() - config.metadata.startTime.getTime() : 0;
          console.error(`❌ API Request: ${error.config?.method?.toUpperCase()} ${error.config?.url} (${duration}ms)`, enhancedError);
        }

        // Attempt retry if conditions are met
        if (this.shouldRetry(enhancedError)) {
          return this.retryRequest(error.config as ExtendedAxiosRequestConfig);
        }

        return Promise.reject(enhancedError);
      }
    );
  }

  private enhanceError(error: AxiosError | Error): EnhancedApiError {
    const enhanced: EnhancedApiError = {
      message: 'An unexpected error occurred',
      detail: 'An unexpected error occurred',
      status: 0,
      isNetworkError: false,
      isTimeout: false,
      isServerError: false,
      isClientError: false,
      retryCount: 0
    };

    if (axios.isAxiosError(error)) {
      if (error.response) {
        // Server responded with error status
        const responseData = error.response.data as any;
        enhanced.message = responseData?.error?.message || responseData?.detail || 'Server error';
        enhanced.detail = responseData?.error?.message || responseData?.detail || 'Server error';
        enhanced.status = error.response.status;
        enhanced.isServerError = error.response.status >= 500;
        enhanced.isClientError = error.response.status >= 400 && error.response.status < 500;

        // Special handling for rate limit errors
        if (error.response.status === 429 ||
          (responseData?.error?.message && responseData.error.message.includes('rate limit'))) {
          enhanced.message = 'API rate limit reached. Please wait a moment and try again.';
          enhanced.detail = 'The AI service is temporarily rate limited. This usually resolves within a minute.';
        }
      } else if (error.request) {
        // Network error
        enhanced.message = 'Network error. Please check your connection.';
        enhanced.detail = 'Network error. Please check your connection.';
        enhanced.isNetworkError = true;
        enhanced.status = 0;
      } else {
        // Request setup error
        enhanced.message = error.message || 'Request configuration error';
        enhanced.detail = error.message || 'Request configuration error';
      }

      if (error.code === 'ECONNABORTED') {
        enhanced.isTimeout = true;
        enhanced.message = 'Request timed out. Please try again.';
        enhanced.detail = 'Request timed out. Please try again.';
      }
    } else {
      // Non-Axios error
      enhanced.message = error.message || 'Unexpected error';
      enhanced.detail = error.message || 'Unexpected error';
    }

    return enhanced;
  }

  private shouldRetry(error: EnhancedApiError): boolean {
    return this.retryConfig.retryCondition?.(error as any) || false;
  }

  private async retryRequest(config: ExtendedAxiosRequestConfig): Promise<AxiosResponse> {
    const retryCount = config.__retryCount || 0;

    if (retryCount >= this.retryConfig.maxRetries) {
      throw this.enhanceError(new Error('Maximum retry attempts exceeded'));
    }

    // Add retry count to config
    config.__retryCount = retryCount + 1;

    // Wait before retrying
    await new Promise(resolve =>
      setTimeout(resolve, this.retryConfig.retryDelay * Math.pow(2, retryCount))
    );

    console.log(`🔄 Retrying request (${retryCount + 1}/${this.retryConfig.maxRetries}): ${config.method?.toUpperCase()} ${config.url}`);

    return this.client.request(config);
  }

  // Public methods
  async get<T>(url: string, config?: AxiosRequestConfig): Promise<T> {
    const response = await this.client.get<T>(url, config);
    return response.data;
  }

  async post<T>(url: string, data?: any, config?: AxiosRequestConfig): Promise<T> {
    const response = await this.client.post<T>(url, data, config);
    return response.data;
  }

  async put<T>(url: string, data?: any, config?: AxiosRequestConfig): Promise<T> {
    const response = await this.client.put<T>(url, data, config);
    return response.data;
  }

  async delete<T>(url: string, config?: AxiosRequestConfig): Promise<T> {
    const response = await this.client.delete<T>(url, config);
    return response.data;
  }

  // Health check method
  async healthCheck(): Promise<boolean> {
    try {
      await this.get('/api/v1/health/');
      return true;
    } catch {
      return false;
    }
  }
}

// Create singleton instance
export const apiClient = new ApiClient();

// Export convenience functions
export const api = {
  get: <T>(url: string, config?: AxiosRequestConfig) => apiClient.get<T>(url, config),
  post: <T>(url: string, data?: any, config?: AxiosRequestConfig) => apiClient.post<T>(url, data, config),
  put: <T>(url: string, data?: any, config?: AxiosRequestConfig) => apiClient.put<T>(url, data, config),
  delete: <T>(url: string, config?: AxiosRequestConfig) => apiClient.delete<T>(url, config),
  healthCheck: () => apiClient.healthCheck()
};

// Export error handling utilities
export const isNetworkError = (error: EnhancedApiError): boolean => error.isNetworkError || false;
export const isTimeoutError = (error: EnhancedApiError): boolean => error.isTimeout || false;
export const isServerError = (error: EnhancedApiError): boolean => error.isServerError || false;
export const isClientError = (error: EnhancedApiError): boolean => error.isClientError || false;
