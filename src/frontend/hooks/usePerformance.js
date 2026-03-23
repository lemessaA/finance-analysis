/**
 * Performance monitoring hooks for the frontend
 */

import { useEffect, useState, useCallback } from 'react';
import { getCLS, getFID, getFCP, getLCP, getTTFB } from 'web-vitals';

// Performance metrics state
let performanceMetrics = {
  cls: 0,
  fid: 0,
  fcp: 0,
  lcp: 0,
  ttfb: 0,
};

// Performance observers
const observers = [];

/**
 * Hook to monitor Core Web Vitals
 */
export function useWebVitals() {
  const [metrics, setMetrics] = useState(performanceMetrics);

  useEffect(() => {
    const handleMetric = (metric) => {
      performanceMetrics[metric.name.toLowerCase()] = metric.value;
      setMetrics({ ...performanceMetrics });
      
      // Send metrics to analytics (optional)
      if (typeof window !== 'undefined' && window.gtag) {
        window.gtag('event', metric.name, {
          event_category: 'Web Vitals',
          event_label: metric.id,
          value: Math.round(metric.name === 'CLS' ? metric.value * 1000 : metric.value),
          non_interaction: true,
        });
      }
    };

    // Measure all Core Web Vitals
    getCLS(handleMetric);
    getFID(handleMetric);
    getFCP(handleMetric);
    getLCP(handleMetric);
    getTTFB(handleMetric);
  }, []);

  return metrics;
}

/**
 * Hook to monitor long tasks that block the main thread
 */
export function useLongTasks() {
  const [longTasks, setLongTasks] = useState([]);

  useEffect(() => {
    if (typeof window !== 'undefined' && 'PerformanceObserver' in window) {
      try {
        const observer = new PerformanceObserver((list) => {
          const entries = list.getEntries();
          const tasks = entries.map(entry => ({
            duration: entry.duration,
            startTime: entry.startTime,
            name: entry.name,
          }));
          setLongTasks(prev => [...prev, ...tasks]);
        });
        
        observer.observe({ entryTypes: ['longtask'] });
        observers.push(observer);
      } catch (e) {
        console.warn('Long task monitoring not supported');
      }
    }

    return () => {
      observers.forEach(observer => observer.disconnect());
    };
  }, []);

  return longTasks;
}

/**
 * Hook to monitor resource loading performance
 */
export function useResourceTiming() {
  const [resources, setResources] = useState([]);

  useEffect(() => {
    if (typeof window !== 'undefined' && 'PerformanceObserver' in window) {
      try {
        const observer = new PerformanceObserver((list) => {
          const entries = list.getEntries();
          const resourceEntries = entries.map(entry => ({
            name: entry.name,
            duration: entry.duration,
            size: entry.transferSize || 0,
            type: entry.initiatorType,
          }));
          setResources(prev => [...prev, ...resourceEntries]);
        });
        
        observer.observe({ entryTypes: ['resource'] });
        observers.push(observer);
      } catch (e) {
        console.warn('Resource timing monitoring not supported');
      }
    }

    return () => {
      observers.forEach(observer => observer.disconnect());
    };
  }, []);

  return resources;
}

/**
 * Hook to measure component render performance
 */
export function useRenderTime(componentName) {
  const [renderTime, setRenderTime] = useState(0);

  useEffect(() => {
    const startTime = performance.now();
    
    return () => {
      const endTime = performance.now();
      const duration = endTime - startTime;
      setRenderTime(duration);
      
      if (duration > 100) { // Log slow renders
        console.warn(`Slow render detected: ${componentName} took ${duration.toFixed(2)}ms`);
      }
    };
  }, [componentName]);

  return renderTime;
}

/**
 * Hook for debounced values to prevent excessive re-renders
 */
export function useDebounce(value, delay) {
  const [debouncedValue, setDebouncedValue] = useState(value);

  useEffect(() => {
    const handler = setTimeout(() => {
      setDebouncedValue(value);
    }, delay);

    return () => {
      clearTimeout(handler);
    };
  }, [value, delay]);

  return debouncedValue;
}

/**
 * Hook for throttled functions
 */
export function useThrottle(func, delay) {
  const [lastRun, setLastRun] = useState(Date.now());

  return useCallback((...args) => {
    if (Date.now() - lastRun >= delay) {
      func(...args);
      setLastRun(Date.now());
    }
  }, [func, delay, lastRun]);
}

/**
 * Hook to monitor memory usage
 */
export function useMemoryUsage() {
  const [memoryUsage, setMemoryUsage] = useState({});

  useEffect(() => {
    const updateMemoryUsage = () => {
      if (performance.memory) {
        setMemoryUsage({
          used: Math.round(performance.memory.usedJSHeapSize / 1048576), // MB
          total: Math.round(performance.memory.totalJSHeapSize / 1048576), // MB
          limit: Math.round(performance.memory.jsHeapSizeLimit / 1048576), // MB
        });
      }
    };

    updateMemoryUsage();
    const interval = setInterval(updateMemoryUsage, 5000);

    return () => clearInterval(interval);
  }, []);

  return memoryUsage;
}

/**
 * Hook to detect if user is on slow connection
 */
export function useSlowConnection() {
  const [isSlow, setIsSlow] = useState(false);

  useEffect(() => {
    if (typeof navigator !== 'undefined' && 'connection' in navigator) {
      const connection = navigator.connection;
      
      const checkConnection = () => {
        const effectiveType = connection.effectiveType;
        const downlink = connection.downlink;
        
        // Consider slow if: slow-2g, 2g, or 3g with low downlink
        setIsSlow(
          effectiveType === 'slow-2g' || 
          effectiveType === '2g' || 
          (effectiveType === '3g' && downlink < 1.5)
        );
      };

      checkConnection();
      connection.addEventListener('change', checkConnection);
      
      return () => {
        connection.removeEventListener('change', checkConnection);
      };
    }
  }, []);

  return isSlow;
}

/**
 * Performance monitoring utility functions
 */
export const performanceUtils = {
  // Mark performance checkpoints
  mark: (name) => {
    if (typeof performance !== 'undefined') {
      performance.mark(name);
    }
  },

  // Measure time between marks
  measure: (name, startMark, endMark) => {
    if (typeof performance !== 'undefined') {
      performance.measure(name, startMark, endMark);
      const entries = performance.getEntriesByName(name, 'measure');
      return entries[entries.length - 1]?.duration || 0;
    }
    return 0;
  },

  // Get navigation timing
  getNavigationTiming: () => {
    if (typeof performance !== 'undefined' && performance.timing) {
      const timing = performance.timing;
      return {
        dns: timing.domainLookupEnd - timing.domainLookupStart,
        tcp: timing.connectEnd - timing.connectStart,
        ssl: timing.secureConnectionStart > 0 ? timing.connectEnd - timing.secureConnectionStart : 0,
        ttfb: timing.responseStart - timing.requestStart,
        download: timing.responseEnd - timing.responseStart,
        domParse: timing.domContentLoadedEventStart - timing.responseEnd,
        domReady: timing.domContentLoadedEventEnd - timing.domContentLoadedEventStart,
        loadComplete: timing.loadEventEnd - timing.loadEventStart,
      };
    }
    return {};
  },

  // Log performance metrics
  logMetrics: () => {
    const metrics = {
      webVitals: performanceMetrics,
      navigation: performanceUtils.getNavigationTiming(),
      memory: typeof performance !== 'undefined' && performance.memory ? {
        used: Math.round(performance.memory.usedJSHeapSize / 1048576),
        total: Math.round(performance.memory.totalJSHeapSize / 1048576),
      } : {},
    };
    
    console.table(metrics);
    return metrics;
  },
};
