"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { FileText, BarChart2, Brain } from "lucide-react";
import clsx from "clsx";

const navItems = [
  { href: "/reports",           label: "Financial Reports",   icon: FileText  },
  { href: "/reports?mode=advanced", label: "Advanced AI Analysis", icon: Brain },
];

export default function Sidebar() {
  const pathname = usePathname();

  return (
    <aside className="fixed left-0 top-0 h-full w-64 bg-slate-900 border-r border-white/10 flex flex-col z-50">
      {/* Logo */}
      <div className="p-6 border-b border-white/10">
        <div className="flex items-center gap-3">
          <div className="w-9 h-9 rounded-xl bg-gradient-to-br from-emerald-500 to-teal-600 flex items-center justify-center shadow-lg shadow-emerald-500/20">
            <BarChart2 className="w-5 h-5 text-white" />
          </div>
          <div>
            <p className="text-sm font-bold text-white leading-tight">Financial Analysis</p>
            <p className="text-xs text-slate-400">AI Platform v1.0</p>
          </div>
        </div>
      </div>

      {/* Navigation */}
      <nav className="flex-1 p-4 space-y-1">
        {navItems.map(({ href, label, icon: Icon }) => {
          const active = pathname === href.split("?")[0];
          return (
            <Link
              key={href}
              href={href}
              className={clsx(
                "flex items-center gap-3 px-4 py-3 rounded-xl text-sm font-medium transition-all duration-200",
                active
                  ? "bg-emerald-600/20 text-emerald-300 border border-emerald-500/30"
                  : "text-slate-400 hover:bg-white/5 hover:text-white"
              )}
            >
              <Icon className="w-4 h-4 flex-shrink-0" />
              {label}
            </Link>
          );
        })}
      </nav>

      {/* Footer */}
      <div className="p-4 border-t border-white/10">
        <p className="text-xs text-slate-500 text-center">
          Powered by AI · Financial Insights
        </p>
      </div>
    </aside>
  );
}
