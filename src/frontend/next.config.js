/** @type {import('next').NextConfig} */

const nextConfig = {
  reactStrictMode: false, // Disabled for faster development
  swcMinify: true,
  compress: true,
  poweredByHeader: false,
  
  env: {
    NEXT_PUBLIC_API_URL: process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000",
  },

  // Simplified performance optimizations for development
  images: {
    formats: ['image/webp', 'image/avif'],
    deviceSizes: [640, 750, 828, 1080, 1200, 1920, 2048, 3840],
    imageSizes: [16, 32, 48, 64, 96, 128, 256, 384],
    minimumCacheTTL: 60,
  },

  // Compression
  compress: true,

  // Static optimization
  trailingSlash: false,
  
  // Headers for caching
  async headers() {
    return [
      {
        source: '/_next/static/(.*)',
        headers: [
          {
            key: 'Cache-Control',
            value: 'public, max-age=31536000, immutable',
          },
        ],
      },
      {
        source: '/api/(.*)',
        headers: [
          {
            key: 'Cache-Control',
            value: 'public, max-age=60, s-maxage=60',
          },
        ],
      },
    ];
  },

  // Redirects for API proxy
  async rewrites() {
    return [
      {
        source: "/api/:path*",
        destination: "http://localhost:8000/api/:path*",
      },
    ];
  },

  // Simplified webpack config for faster builds
  webpack: (config, { dev, isServer }) => {
    if (dev) {
      // Faster development builds
      config.optimization.minimize = false;
    }
    
    return config;
  },
};

module.exports = nextConfig;
