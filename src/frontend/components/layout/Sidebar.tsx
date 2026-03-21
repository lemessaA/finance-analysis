"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import {
  Lightbulb,
  FileText,
  TrendingUp,
  Brain,
  LineChart,
} from "lucide-react";
import clsx from "clsx";

const navItems = [
  { href: "/startup",     label: "Startup Validator", icon: Lightbulb  },
  { href: "/market",      label: "Market Intel",      icon: LineChart  },
  { href: "/reports",     label: "Financial Reports", icon: FileText   },
  { href: "/forecasting", label: "ML Forecasting",    icon: Brain       },
];

export default function Sidebar() {
  const pathname = usePathname();

  return (
    <aside className="fixed left-0 top-0 h-full w-64 bg-surface-card border-r border-surface-border flex flex-col z-50">
      {/* Logo */}
      <div className="p-6 border-b border-surface-border">
        <div className="flex items-center gap-3">
          <div className="w-9 h-9 rounded-xl bg-gradient-to-br from-brand-500 to-purple-600 flex items-center justify-center shadow-glow-brand">
            <Brain className="w-5 h-5 text-white" />
          </div>
          <div> 
            <p className="text-sm font-bold text-white leading-tight">Your Business Intelligence</p>
            <p className="text-xs text-slate-400">Platform v1.0</p>
          </div>
        </div>
      </div>

      {/* Navigation */}
      <nav className="flex-1 p-4 space-y-1">
        {navItems.map(({ href, label, icon: Icon }) => {
          const active = pathname === href;
          return (
            <Link
              key={href}
              href={href}
              className={clsx(
                "flex items-center gap-3 px-4 py-3 rounded-xl text-sm font-medium transition-all duration-200",
                active
                  ? "bg-brand-600/20 text-brand-300 border border-brand-500/30 shadow-glow-brand"
                  : "text-slate-400 hover:bg-surface-hover hover:text-white"
              )}
            >
              <Icon className="w-4 h-4 flex-shrink-0" />
              {label}
            </Link>
          );
        })}
      </nav>

      {/* Footer */}
      <div className="p-4 border-t border-surface-border">
        <p className="text-xs text-slate-500 text-center">
          Powered by GPT-4o + LangGraph
        </p>
      </div>
    </aside>
  );
}
