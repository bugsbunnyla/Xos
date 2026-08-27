"use client";
import { useState } from "react";
import { motion } from "framer-motion";
import { Zap, Send, Loader2, User } from "lucide-react";
import { useSkills, useInvokeSkill } from "@/hooks/useSkills";

const CATEGORIES = ["All", "legal", "security", "finance", "healthcare", "sales", "operations", "academia", "executive"];

export function SkillSelector({ user }: { user: any }) {
  const [category, setCategory] = useState("All");
  const [selectedSkill, setSelectedSkill] = useState<string | null>(null);
  const [query, setQuery] = useState("");
  const { data: skills } = useSkills(category === "All" ? undefined : category);
  const invoke = useInvokeSkill();

  return (
    <div className="space-y-6">
      <div className="glass-panel p-6">
        <div className="flex items-center gap-3 mb-6">
          <Zap className="w-6 h-6 text-amber-400" />
          <h2 className="text-xl font-bold">AI Skill Agents</h2>
        </div>
        <div className="flex flex-wrap gap-2 mb-6">
          {CATEGORIES.map((cat) => (
            <button key={cat} onClick={() => setCategory(cat)}
              className={`px-3 py-1.5 rounded-lg text-sm font-medium transition-colors ${
                category === cat ? "bg-violet-500/20 text-violet-300 border border-violet-500/30" : "text-slate-400 hover:text-slate-200 hover:bg-slate-800/50"
              }`}>{cat}</button>
          ))}
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-3 mb-6">
          {skills?.map((skill: any) => (
            <button key={skill.id} onClick={() => setSelectedSkill(skill.id)}
              className={`p-4 rounded-xl border text-left transition-all ${
                selectedSkill === skill.id ? "border-violet-500/50 bg-violet-500/10" : "border-slate-800/50 bg-slate-800/30 hover:bg-slate-800/50"
              }`}>
              <h4 className="font-medium text-slate-200">{skill.name}</h4>
              <p className="text-sm text-slate-500 mt-1">{skill.description}</p>
              <span className="text-xs text-slate-600 mt-2 inline-block">{skill.category}</span>
            </button>
          ))}
        </div>
        {selectedSkill && (
          <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} className="space-y-3">
            <div className="flex items-center gap-2 text-sm text-violet-400 mb-2">
              <User className="w-4 h-4" />
              <span>Running as {user?.role} &bull; {user?.department || "General"}</span>
            </div>
            <textarea value={query} onChange={(e) => setQuery(e.target.value)} placeholder={`Ask the ${selectedSkill} agent...`}
              className="w-full h-32 p-4 bg-slate-800/50 border border-slate-700 rounded-xl focus:outline-none focus:border-violet-500 resize-none" />
            <button onClick={() => invoke.mutate({ skill_id: selectedSkill, query })}
              disabled={invoke.isPending || !query}
              className="w-full h-12 bg-violet-600 hover:bg-violet-500 rounded-xl font-medium transition-colors disabled:opacity-50 flex items-center justify-center gap-2">
              {invoke.isPending ? <Loader2 className="w-4 h-4 animate-spin" /> : <Send className="w-4 h-4" />}
              Invoke Agent
            </button>
          </motion.div>
        )}
        {invoke.data && (
          <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="mt-4 p-4 bg-slate-800/50 rounded-xl border border-violet-500/20">
            <h4 className="font-medium text-violet-300 mb-2">Agent Response</h4>
            <p className="text-slate-300 text-sm whitespace-pre-wrap">{invoke.data.response}</p>
          </motion.div>
        )}
      </div>
    </div>
  );
}
