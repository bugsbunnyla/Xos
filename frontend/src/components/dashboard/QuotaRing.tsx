"use client";

interface QuotaRingProps {
  used: number;
  total: number;
  label: string;
}

export function QuotaRing({ used, total, label }: QuotaRingProps) {
  const pct = Math.round((used / total) * 100);
  return (
    <div className="glass-panel p-6 flex flex-col items-center">
      <div className="relative w-24 h-24">
        <svg className="w-full h-full -rotate-90" viewBox="0 0 36 36">
          <path className="text-slate-800" d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831" fill="none" stroke="currentColor" strokeWidth="3" />
          <path className="text-violet-500" strokeDasharray={`${pct}, 100`} d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831" fill="none" stroke="currentColor" strokeWidth="3" />
        </svg>
        <div className="absolute inset-0 flex items-center justify-center">
          <span className="text-lg font-bold">{pct}%</span>
        </div>
      </div>
      <p className="text-sm text-slate-400 mt-3">{label}</p>
      <p className="text-xs text-slate-500">{used} / {total}</p>
    </div>
  );
}
