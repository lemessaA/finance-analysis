/** @type {import('next').NextConfig} */

const nextConfig = {
  reactStrictMode: false,
  swcMinify: true,
  compress: true,
  poweredByHeader: false,
  
  env: {
    NEXT_PUBLIC_API_URL: process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000",
  },

  // API proxy rewrites
  async rewrites() {
    return [
      {
        source: "/api/:path*",
        destination: "http://localhost:8000/api/:path*",
      },
    ];
  },

  // Simplified webpack config
  webpack: (config, { dev, isServer }) => {
    // Fix runtime issues
    config.resolve.fallback = {
      ...config.resolve.fallback,
      fs: false,
      net: false,
      tls: false,
    };
    
    return config;
  },
};

module.exports = nextConfig;
