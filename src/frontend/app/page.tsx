"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";

export default function HomePage() {
  const router = useRouter();

  useEffect(() => {
    // Redirect to the main dashboard
    router.replace("/dashboard");
  }, [router]);

  return (
    <div className="min-h-full flex items-center justify-center">
      <div className="text-center">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-brand-500 mx-auto mb-4"></div>
        <p className="text-slate-400">Redirecting to dashboard...</p>
      </div>
    </div>
  );
}
