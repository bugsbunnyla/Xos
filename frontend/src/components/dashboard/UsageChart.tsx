"use client";
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer } from "recharts";

const data = [
  { name: "Mon", searches: 120, osint: 15 },
  { name: "Tue", searches: 180, osint: 22 },
  { name: "Wed", searches: 150, osint: 18 },
  { name: "Thu", searches: 220, osint: 30 },
  { name: "Fri", searches: 190, osint: 25 },
  { name: "Sat", searches: 80, osint: 10 },
  { name: "Sun", searches: 60, osint: 8 },
];

export function UsageChart() {
  return (
    <div className="glass-panel p-6">
      <h3 className="font-semibold mb-4">Weekly Activity</h3>
      <ResponsiveContainer width="100%" height={200}>
        <BarChart data={data}>
          <XAxis dataKey="name" stroke="#64748b" fontSize={12} />
          <YAxis stroke="#64748b" fontSize={12} />
          <Tooltip contentStyle={{ backgroundColor: '#1e293b', border: 'none', borderRadius: '8px' }} />
          <Bar dataKey="searches" fill="#8b5cf6" radius={[4, 4, 0, 0]} />
          <Bar dataKey="osint" fill="#ef4444" radius={[4, 4, 0, 0]} />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}
