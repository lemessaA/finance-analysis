import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import { AuthProvider } from "@/contexts/AuthContext";
import ErrorBoundary from "@/components/ErrorBoundary";
import { I18nProvider } from "@/contexts/I18nContext";

const inter = Inter({ subsets: ["latin"], variable: "--font-inter" });

export const metadata: Metadata = {
  title: "Business Insights - AI Intelligence Platform",
  description:
    "AI-powered platform for business analytics, database queries, and data insights",
  keywords: ["AI", "Business Intelligence", "Data Analytics", "Business Insights", "Database Queries"],
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
          <I18nProvider>
            <AuthProvider>
              {children}
            </AuthProvider>
          </I18nProvider>
        </ErrorBoundary>
      </body>
    </html>
  );
}
