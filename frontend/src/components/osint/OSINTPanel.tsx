"use client";
import { useState } from "react";
import { motion } from "framer-motion";
import { Shield, Search, Loader2, FileText, AlertTriangle } from "lucide-react";
import { useOSINTInvestigate, useOSINTReports } from "@/hooks/useOSINT";

const TARGET_TYPES = [
  { value: "domain", label: "Domain" },
  { value: "ip", label: "IP Address" },
  { value: "email", label: "Email" },
  { value: "phone", label: "Phone" },
  { value: "person", label: "Person" },
  { value: "company", label: "Company" },
];

export function OSINTPanel() {
  const [target, setTarget] = useState("");
  const [targetType, setTargetType] = useState("domain");
  const investigate = useOSINTInvestigate();
  const { data: reports } = useOSINTReports();

  return (
    <div className="space-y-6">
      <div className="glass-panel p-6">
        <div className="flex items-center gap-3 mb-6">
          <Shield className="w-6 h-6 text-red-400" />
          <h2 className="text-xl font-bold">OSINT Intelligence Engine</h2>
        </div>
        <div className="flex gap-3 mb-4">
          <select value={targetType} onChange={(e) => setTargetType(e.target.value)}
            className="h-12 px-4 bg-slate-800/50 border border-slate-700 rounded-xl text-sm focus:outline-none focus:border-violet-500">
            {TARGET_TYPES.map((t) => <option key={t.value} value={t.value}>{t.label}</option>)}
          </select>
          <input type="text" value={target} onChange={(e) => setTarget(e.target.value)} placeholder="Enter target..."
            className="flex-1 h-12 px-4 bg-slate-800/50 border border-slate-700 rounded-xl focus:outline-none focus:border-violet-500" />
          <button onClick={() => investigate.mutate({ target, target_type: targetType })}
            disabled={investigate.isPending || !target}
            className="h-12 px-6 bg-red-600 hover:bg-red-500 rounded-xl font-medium transition-colors disabled:opacity-50 flex items-center gap-2">
            {investigate.isPending ? <Loader2 className="w-4 h-4 animate-spin" /> : <Search className="w-4 h-4" />}
            Investigate
          </button>
        </div>
        {investigate.data && (
          <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="mt-4 p-4 bg-slate-800/50 rounded-xl">
            <div className="flex items-center gap-2 mb-2">
              <AlertTriangle className="w-5 h-5 text-amber-400" />
              <span className="font-semibold">Risk Level: {investigate.data.risk_level?.toUpperCase()}</span>
              <span className="text-slate-400">({investigate.data.risk_score}/100)</span>
            </div>
            <p className="text-sm text-slate-400">Report ID: {investigate.data.report_id}</p>
          </motion.div>
        )}
      </div>
      <div className="glass-panel p-6">
        <h3 className="font-semibold mb-4 flex items-center gap-2"><FileText className="w-4 h-4" /> Previous Reports</h3>
        <div className="space-y-2">
          {reports?.map((report: any) => (
            <div key={report.id} className="flex items-center justify-between p-3 bg-slate-800/30 rounded-lg">
              <div>
                <p className="font-medium text-sm">{report.target}</p>
                <p className="text-xs text-slate-500">{report.target_type} &bull; {report.status}</p>
              </div>
              <span className={`text-xs px-2 py-1 rounded-full ${
                report.status === 'completed' ? 'bg-emerald-500/20 text-emerald-400' :
                report.status === 'running' ? 'bg-amber-500/20 text-amber-400' :
                'bg-slate-700 text-slate-400'
              }`}>{report.status}</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
