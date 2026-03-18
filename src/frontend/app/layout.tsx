import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import Sidebar from "@/components/layout/Sidebar";

const inter = Inter({ subsets: ["latin"], variable: "--font-inter" });

export const metadata: Metadata = {
  title: "Your Business Intelligence Platform",
  description:
    "Startup validation, financial analysis, and forecasting powered by multi-agent AI",
  keywords: ["AI", "Business Intelligence", "Startup Validator", "Financial Analysis"],
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className="dark">
      <body className={`${inter.variable} font-sans bg-surface text-white antialiased`}>
        <div className="flex min-h-screen">
          <Sidebar />
          <main className="flex-1 ml-64 min-h-screen p-8 overflow-auto">
            {children}
          </main>
        </div>
      </body>
    </html>
  );
}
