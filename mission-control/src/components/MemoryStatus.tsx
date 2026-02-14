'use client';

import { useCallback, useEffect, useState } from 'react';

interface MemoryAgentStatus {
  id: string;
  label: string;
  available: boolean;
  files: number;
  chunks: number;
  error?: string;
}

export default function MemoryStatus() {
  const [agents, setAgents] = useState<MemoryAgentStatus[]>([]);
  const [loading, setLoading] = useState(true);

  const fetchStatus = useCallback(async () => {
    try {
      const res = await fetch('/api/memory');
      const data = await res.json();
      setAgents(data.agents || []);
    } catch {
      setAgents([]);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchStatus();
    const interval = setInterval(fetchStatus, 60000);
    return () => clearInterval(interval);
  }, [fetchStatus]);

  return (
    <div className="bg-zinc-900/60 rounded-xl border border-zinc-800 p-6">
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-lg font-semibold text-white flex items-center gap-2">
          <span>🧠</span>
          Memory Status
        </h2>
        <span className="text-xs text-zinc-400">sqlite snapshot</span>
      </div>

      {loading ? (
        <div className="text-sm text-zinc-400">Loading memory stats…</div>
      ) : agents.length === 0 ? (
        <div className="text-sm text-zinc-400">No memory databases found.</div>
      ) : (
        <div className="space-y-3">
          {agents.map((agent) => (
            <div
              key={agent.id}
              className="rounded-lg border border-zinc-800 bg-zinc-950/40 p-3"
            >
              <div className="flex items-center justify-between">
                <div className="text-sm font-medium text-white">{agent.label}</div>
                <span
                  className={`text-[10px] px-2 py-0.5 rounded-full font-semibold ${
                    agent.available
                      ? 'bg-emerald-500/20 text-emerald-300'
                      : 'bg-rose-500/20 text-rose-300'
                  }`}
                >
                  {agent.available ? 'Available' : 'Missing'}
                </span>
              </div>
              {agent.available ? (
                <div className="mt-2 grid grid-cols-2 gap-2 text-xs text-zinc-400">
                  <div>
                    <span className="text-zinc-500">Files:</span>{' '}
                    <span className="text-zinc-200">{agent.files.toLocaleString()}</span>
                  </div>
                  <div>
                    <span className="text-zinc-500">Chunks:</span>{' '}
                    <span className="text-zinc-200">{agent.chunks.toLocaleString()}</span>
                  </div>
                </div>
              ) : (
                <div className="mt-2 text-xs text-rose-300/80">
                  {agent.error || 'Memory DB not available.'}
                </div>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
