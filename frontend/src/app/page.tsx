"use client";
import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Search, Shield, Brain, Zap, User, Building2, LogOut, BarChart3, Globe, Lock } from "lucide-react";
import { useAuth } from "@/components/providers/AuthProvider";
import { SearchResults } from "@/components/search/SearchResults";
import { OSINTPanel } from "@/components/osint/OSINTPanel";
import { SkillSelector } from "@/components/skills/SkillSelector";
import { useSearch } from "@/hooks/useSearch";

export default function Home() {
  const { user, logout } = useAuth();
  const [query, setQuery] = useState("");
  const [activeTab, setActiveTab] = useState<"search" | "osint" | "skills" | "dashboard">("search");
  const search = useSearch();

  const handleSearch = () => {
    if (!query.trim()) return;
    search.mutate({ query, search_type: "hybrid" });
  };

  if (!user) return <LoginScreen />;

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-950 via-slate-900 to-violet-950/20">
      <header className="border-b border-slate-800/50 glass-panel rounded-none sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-6 h-16 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-violet-500 to-fuchsia-500 flex items-center justify-center">
              <Brain className="w-5 h-5 text-white" />
            </div>
            <span className="font-bold text-lg tracking-tight">PhD Xpert Solver</span>
          </div>
          <div className="flex items-center gap-4">
            <div className="hidden md:flex items-center gap-2 text-sm text-slate-400">
              <Building2 className="w-4 h-4" />
              <span>{user.department || "General"}</span>
            </div>
            <div className="hidden md:flex items-center gap-2 text-sm text-slate-400">
              <User className="w-4 h-4" />
              <span>{user.first_name || user.email}</span>
            </div>
            <div className="flex items-center gap-2 text-xs px-2 py-1 rounded-full bg-violet-500/20 text-violet-300 border border-violet-500/30">
              <Lock className="w-3 h-3" />
              {user.role}
            </div>
            <button onClick={logout} className="p-2 hover:bg-slate-800 rounded-lg transition-colors">
              <LogOut className="w-4 h-4 text-slate-400" />
            </button>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-6 py-8">
        <div className="flex flex-wrap gap-2 mb-8">
          {[
            { id: "search", label: "AI Search", icon: Search },
            { id: "osint", label: "OSINT Intel", icon: Shield },
            { id: "skills", label: "Skill Agents", icon: Zap },
            { id: "dashboard", label: "Dashboard", icon: BarChart3 },
          ].map((tab) => (
            <button key={tab.id} onClick={() => setActiveTab(tab.id as any)}
              className={`flex items-center gap-2 px-4 py-2 rounded-xl text-sm font-medium transition-all ${
                activeTab === tab.id
                  ? "bg-violet-500/20 text-violet-300 border border-violet-500/30"
                  : "text-slate-400 hover:text-slate-200 hover:bg-slate-800/50"
              }`}>
              <tab.icon className="w-4 h-4" />{tab.label}
            </button>
          ))}
        </div>

        {activeTab === "search" && (
          <div className="space-y-6">
            <div className="relative max-w-3xl mx-auto">
              <input type="text" value={query} onChange={(e) => setQuery(e.target.value)}
                onKeyDown={(e) => e.key === "Enter" && handleSearch()}
                placeholder="Ask anything... powered by your profile context"
                className="w-full h-14 pl-14 pr-6 bg-slate-900/80 border border-slate-700/50 rounded-2xl text-lg placeholder:text-slate-500 focus:outline-none focus:border-violet-500/50 focus:ring-2 focus:ring-violet-500/20 transition-all search-glow" />
              <Search className="absolute left-5 top-1/2 -translate-y-1/2 w-5 h-5 text-slate-500" />
              <button onClick={handleSearch} disabled={search.isPending}
                className="absolute right-3 top-1/2 -translate-y-1/2 px-4 py-2 bg-violet-600 hover:bg-violet-500 rounded-xl text-sm font-medium transition-colors disabled:opacity-50">
                {search.isPending ? "..." : "Solve"}
              </button>
            </div>
            <AnimatePresence>
              {search.data && <SearchResults data={search.data} user={user} />}
            </AnimatePresence>
          </div>
        )}
        {activeTab === "osint" && <OSINTPanel />}
        {activeTab === "skills" && <SkillSelector user={user} />}
        {activeTab === "dashboard" && <Dashboard user={user} />}
      </main>
    </div>
  );
}

function Dashboard({ user }: { user: any }) {
  return (
    <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
      <div className="glass-panel p-6">
        <h3 className="font-semibold mb-4 flex items-center gap-2"><BarChart3 className="w-4 h-4 text-violet-400" /> Usage</h3>
        <div className="space-y-3">
          <div className="flex justify-between"><span className="text-sm text-slate-400">Subscription</span><span className="text-sm font-medium text-violet-300">{user.subscription_tier}</span></div>
          <div className="flex justify-between"><span className="text-sm text-slate-400">API Quota</span><span className="text-sm font-medium">{user.api_quota_remaining} / {user.api_quota_total}</span></div>
          <div className="flex justify-between"><span className="text-sm text-slate-400">Role</span><span className="text-sm font-medium">{user.role}</span></div>
        </div>
      </div>
      <div className="glass-panel p-6">
        <h3 className="font-semibold mb-4 flex items-center gap-2"><Globe className="w-4 h-4 text-emerald-400" /> Profile Context</h3>
        <div className="space-y-3">
          <div className="flex justify-between"><span className="text-sm text-slate-400">Department</span><span className="text-sm font-medium">{user.department || "N/A"}</span></div>
          <div className="flex justify-between"><span className="text-sm text-slate-400">Job Title</span><span className="text-sm font-medium">{user.job_title || "N/A"}</span></div>
          <div className="flex justify-between"><span className="text-sm text-slate-400">Company ID</span><span className="text-sm font-medium">{user.company_id || "N/A"}</span></div>
        </div>
      </div>
      <div className="glass-panel p-6">
        <h3 className="font-semibold mb-4 flex items-center gap-2"><Shield className="w-4 h-4 text-red-400" /> Security</h3>
        <div className="space-y-3">
          <div className="flex justify-between"><span className="text-sm text-slate-400">Email Verified</span><span className="text-sm font-medium">{user.email_verified ? "Yes" : "No"}</span></div>
          <div className="flex justify-between"><span className="text-sm text-slate-400">MFA Enabled</span><span className="text-sm font-medium">{user.mfa_enabled ? "Yes" : "No"}</span></div>
          <div className="flex justify-between"><span className="text-sm text-slate-400">Status</span><span className="text-sm font-medium text-emerald-400">{user.status}</span></div>
        </div>
      </div>
    </div>
  );
}

function LoginScreen() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const { login } = useAuth();

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-slate-950 via-slate-900 to-violet-950/20">
      <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} className="w-full max-w-md p-8 glass-panel">
        <div className="flex items-center justify-center gap-3 mb-8">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-violet-500 to-fuchsia-500 flex items-center justify-center">
            <Brain className="w-6 h-6 text-white" />
          </div>
          <h1 className="text-2xl font-bold">PhD Xpert Solver</h1>
        </div>
        <div className="space-y-4">
          <input type="email" placeholder="Email" value={email} onChange={(e) => setEmail(e.target.value)}
            className="w-full h-12 px-4 bg-slate-800/50 border border-slate-700 rounded-xl focus:outline-none focus:border-violet-500" />
          <input type="password" placeholder="Password" value={password} onChange={(e) => setPassword(e.target.value)}
            className="w-full h-12 px-4 bg-slate-800/50 border border-slate-700 rounded-xl focus:outline-none focus:border-violet-500" />
          <button onClick={() => login(email, password)}
            className="w-full h-12 bg-violet-600 hover:bg-violet-500 rounded-xl font-medium transition-colors">
            Sign In
          </button>
        </div>
        <div className="mt-6 text-center text-xs text-slate-500">
          Enterprise AI + OSINT + Search Browser
        </div>
      </motion.div>
    </div>
  );
}
