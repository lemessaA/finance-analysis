import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import ErrorBoundary from "@/components/ErrorBoundary";

const inter = Inter({ subsets: ["latin"], variable: "--font-inter" });

export const metadata: Metadata = {
  title: "Financial Analysis Platform - AI-Powered Report Analyzer",
  description:
    "AI-powered financial report analysis platform. Upload PDF statements and extract key metrics instantly.",
  keywords: ["AI", "Financial Analysis", "PDF Reports", "Financial Metrics", "Report Analyzer"],
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className="dark">
      <body className={`${inter.variable} font-sans bg-slate-900 text-white antialiased`}>
        <ErrorBoundary>
          {children}
        </ErrorBoundary>
      </body>
    </html>
  );
}
