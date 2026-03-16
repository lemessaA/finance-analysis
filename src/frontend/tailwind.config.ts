import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
    "./hooks/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      fontFamily: {
        sans: ["Inter", "system-ui", "sans-serif"],
      },
      colors: {
        brand: {
          50: "#f0f4ff",
          100: "#dde6ff",
          200: "#c3d0ff",
          300: "#9db1ff",
          400: "#7088ff",
          500: "#4f62ff",
          600: "#3940f5",
          700: "#2e33d8",
          800: "#282dae",
          900: "#262c89",
        },
        surface: {
          DEFAULT: "#0f1117",
          card: "#1a1d2e",
          border: "#2a2d3e",
          hover: "#252840",
        },
      },
      boxShadow: {
        "glow-brand": "0 0 20px rgba(79, 98, 255, 0.3)",
        "glow-green": "0 0 20px rgba(52, 211, 153, 0.3)",
        "card": "0 4px 24px rgba(0, 0, 0, 0.4)",
      },
      animation: {
        "fade-in": "fadeIn 0.4s ease-in-out",
        "slide-up": "slideUp 0.4s ease-out",
        "pulse-slow": "pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite",
        "spin-slow": "spin 3s linear infinite",
      },
      keyframes: {
        fadeIn: {
          "0%": { opacity: "0" },
          "100%": { opacity: "1" },
        },
        slideUp: {
          "0%": { opacity: "0", transform: "translateY(16px)" },
          "100%": { opacity: "1", transform: "translateY(0)" },
        },
      },
    },
  },
  plugins: [],
};

export default config;
