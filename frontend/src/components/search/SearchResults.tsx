"use client";
import { motion } from "framer-motion";
import { Globe, Shield, Brain, BarChart3 } from "lucide-react";
import ReactMarkdown from "react-markdown";

interface SearchResultsProps {
  data: any;
  user: any;
}

export function SearchResults({ data, user }: SearchResultsProps) {
  return (
    <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} className="space-y-6">
      {data.ai_summary && (
        <div className="glass-panel p-6 border-l-4 border-violet-500">
          <div className="flex items-center gap-2 mb-3">
            <Brain className="w-5 h-5 text-violet-400" />
            <h3 className="font-semibold text-violet-300">AI Summary (Tailored for {user?.role})</h3>
          </div>
          <div className="text-slate-300 leading-relaxed prose prose-invert max-w-none">
            <ReactMarkdown>{data.ai_summary}</ReactMarkdown>
          </div>
        </div>
      )}
      <div className="flex gap-4">
        <div className="glass-panel px-4 py-2 flex items-center gap-2">
          <BarChart3 className="w-4 h-4 text-emerald-400" />
          <span className="text-sm text-slate-400">{data.total} results</span>
        </div>
        <div className="glass-panel px-4 py-2 flex items-center gap-2">
          <Shield className="w-4 h-4 text-blue-400" />
          <span className="text-sm text-slate-400">Profile-matched: {data.profile_matched ? "Yes" : "No"}</span>
        </div>
      </div>
      <div className="space-y-3">
        {data.results?.map((result: any, i: number) => (
          <motion.a key={result.id || i} href={result.url} target="_blank" rel="noopener noreferrer"
            initial={{ opacity: 0, x: -10 }} animate={{ opacity: 1, x: 0 }} transition={{ delay: i * 0.05 }}
            className="block glass-panel p-4 hover:bg-slate-800/80 transition-colors group">
            <div className="flex items-start gap-3">
              <Globe className="w-4 h-4 text-slate-500 mt-1 group-hover:text-violet-400 transition-colors" />
              <div className="flex-1">
                <h4 className="font-medium text-slate-200 group-hover:text-violet-300 transition-colors">{result.title || "Untitled"}</h4>
                <p className="text-sm text-slate-400 mt-1 line-clamp-2">{result.snippet}</p>
                <div className="flex items-center gap-3 mt-2">
                  <span className="text-xs text-slate-500">{result.domain}</span>
                  <span className="text-xs px-2 py-0.5 rounded-full bg-slate-800 text-slate-400">{result.source}</span>
                  <span className="text-xs text-emerald-400">Score: {result.score?.toFixed(2)}</span>
                </div>
              </div>
            </div>
          </motion.a>
        ))}
      </div>
    </motion.div>
  );
}
