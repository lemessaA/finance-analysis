/**
 * Optimized lazy loading image component with intersection observer
 */

import { useState, useRef, useEffect } from 'react';
import { useIntersectionObserver } from 'react-intersection-observer';

export default function LazyImage({
  src,
  alt,
  className = '',
  placeholder = 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNDAiIGhlaWdodD0iNDAiIHZpZXdCb3g9IjAgMCA0MCA0MCIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPHJlY3Qgd2lkdGg9IjQwIiBoZWlnaHQ9IjQwIiBmaWxsPSIjRjNGNEY2Ii8+CjxwYXRoIGQ9Ik0yMCAyNkMxOC4yMDcgMjYgMTYuNzMwNyAyNC43MzA3IDE1LjczMDcgMjMuNzMwN0MxNC43MzA3IDIyLjczMDcgMTQgMjEuMjY5MyAxNCAyMEMxNCAxOC43MzA3IDE0LjczMDcgMTcuMjY5MyAxNS43MzA3IDE2LjI2OTNDMTYuNzMwNyAxNS4yNjkzIDE4LjIwNyAxNCAyMCAxNEMyMS43OTMgMTQgMjMuMjY5MyAxNS4yNjkzIDI0LjI2OTMgMTYuMjY5M0MyNS4yNjkzIDE3LjI2OTMgMjYgMTguNzMwNyAyNiAyMEMyNiAyMS4yNjkzIDI1LjI2OTMgMjIuNzMwNyAyNC4yNjkzIDIzLjczMDdDMjMuMjY5MyAyNC43MzA3IDIxLjY5MyAyNiAyMCAyNloiIGZpbGw9IiM5Q0EzQUYiLz4KPC9zdmc+',
  width,
  height,
  priority = false,
  onLoad,
  onError,
  ...props
}) {
  const [isLoaded, setIsLoaded] = useState(false);
  const [hasError, setHasError] = useState(false);
  const [currentSrc, setCurrentSrc] = useState(priority ? src : placeholder);
  const imgRef = useRef();

  const { ref, inView } = useIntersectionObserver({
    threshold: 0.1,
    triggerOnce: true,
    rootMargin: '50px',
  });

  // Set the ref for both intersection observer and image element
  const setRefs = (node) => {
    ref(node);
    imgRef.current = node;
  };

  useEffect(() => {
    if (priority || (inView && !isLoaded && !hasError)) {
      setCurrentSrc(src);
    }
  }, [inView, priority, src, isLoaded, hasError]);

  const handleLoad = (e) => {
    setIsLoaded(true);
    if (onLoad) {
      onLoad(e);
    }
  };

  const handleError = (e) => {
    setHasError(true);
    if (onError) {
      onError(e);
    }
  };

  // Generate responsive srcset if multiple sizes are provided
  const generateSrcSet = (src) => {
    if (typeof src === 'object' && src.srcSet) {
      return src.srcSet;
    }
    return null;
  };

  return (
    <div className={`relative overflow-hidden ${className}`} {...props}>
      <img
        ref={setRefs}
        src={currentSrc}
        alt={alt}
        width={width}
        height={height}
        srcSet={generateSrcSet(src)}
        sizes="(max-width: 768px) 100vw, (max-width: 1200px) 50vw, 33vw"
        loading={priority ? 'eager' : 'lazy'}
        decoding="async"
        onLoad={handleLoad}
        onError={handleError}
        className={`
          transition-opacity duration-300 ease-in-out
          ${isLoaded ? 'opacity-100' : 'opacity-0'}
          ${hasError ? 'hidden' : ''}
        `}
      />
      
      {/* Loading placeholder */}
      {!isLoaded && !hasError && (
        <div 
          className="absolute inset-0 bg-gray-200 animate-pulse flex items-center justify-center"
          style={{ aspectRatio: width && height ? `${width}/${height}` : 'auto' }}
        >
          <svg 
            className="w-8 h-8 text-gray-400" 
            fill="none" 
            stroke="currentColor" 
            viewBox="0 0 24 24"
          >
            <path 
              strokeLinecap="round" 
              strokeLinejoin="round" 
              strokeWidth={2} 
              d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" 
            />
          </svg>
        </div>
      )}
      
      {/* Error state */}
      {hasError && (
        <div 
          className="absolute inset-0 bg-gray-200 flex items-center justify-center text-gray-500"
          style={{ aspectRatio: width && height ? `${width}/${height}` : 'auto' }}
        >
          <svg 
            className="w-8 h-8" 
            fill="none" 
            stroke="currentColor" 
            viewBox="0 0 24 24"
          >
            <path 
              strokeLinecap="round" 
              strokeLinejoin="round" 
              strokeWidth={2} 
              d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" 
            />
          </svg>
        </div>
      )}
    </div>
  );
}

// Progressive image component for better UX
export function ProgressiveImage({ src, placeholder, alt, className, ...props }) {
  const [imgSrc, setImgSrc] = useState(placeholder);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const img = new Image();
    img.src = src;
    img.onload = () => {
      setImgSrc(src);
      setLoading(false);
    };
  }, [src]);

  return (
    <div className={`relative ${className}`} {...props}>
      <img
        src={imgSrc}
        alt={alt}
        className={`
          transition-all duration-500 ease-in-out
          ${loading ? 'filter blur-sm scale-110' : 'filter blur-0 scale-100'}
        `}
      />
    </div>
  );
}
