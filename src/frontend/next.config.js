/** @type {import('next').NextConfig} */

const BACKEND_URL = process.env.NEXT_PUBLIC_API_URL || "https://finance-app.fastapicloud.dev";

const nextConfig = {
  reactStrictMode: false,
  swcMinify: true,
  compress: true,
  poweredByHeader: false,

  env: {
    NEXT_PUBLIC_API_URL: BACKEND_URL,
  },

  // Proxy all /api/v1/ requests to the deployed backend
  // This fixes relative-URL fetch calls in frontend components
  async rewrites() {
    return [
      {
        source: "/api/v1/:path*",
        destination: `${BACKEND_URL}/api/v1/:path*`,
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
