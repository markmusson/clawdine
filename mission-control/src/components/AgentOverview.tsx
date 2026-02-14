'use client';

import { useCallback, useEffect, useState } from 'react';

interface AgentStatus {
  id: string;
  name: string;
  model: string;
  status: 'ready' | 'missing' | 'unknown';
  detail?: string;
}

export default function AgentOverview() {
  const [agents, setAgents] = useState<AgentStatus[]>([]);
  const [loading, setLoading] = useState(true);

  const fetchAgents = useCallback(async () => {
    try {
      const res = await fetch('/api/agents');
      const data = await res.json();
      setAgents(data.agents || []);
    } catch {
      setAgents([]);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchAgents();
    const interval = setInterval(fetchAgents, 60000);
    return () => clearInterval(interval);
  }, [fetchAgents]);

  const statusLabel = (status: AgentStatus['status']) => {
    switch (status) {
      case 'ready':
        return 'Ready';
      case 'missing':
        return 'Missing';
      default:
        return 'Unknown';
    }
  };

  const statusClasses = (status: AgentStatus['status']) => {
    switch (status) {
      case 'ready':
        return 'bg-emerald-500/20 text-emerald-300';
      case 'missing':
        return 'bg-rose-500/20 text-rose-300';
      default:
        return 'bg-zinc-500/20 text-zinc-300';
    }
  };

  return (
    <div className="bg-zinc-900/60 rounded-xl border border-zinc-800 p-6">
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-lg font-semibold text-white flex items-center gap-2">
          <span>🤖</span>
          Agents
        </h2>
        <span className="text-xs text-zinc-400">Local config</span>
      </div>

      {loading ? (
        <div className="text-sm text-zinc-400">Loading agents…</div>
      ) : agents.length === 0 ? (
        <div className="text-sm text-zinc-400">No agents found.</div>
      ) : (
        <div className="space-y-3">
          {agents.map((agent) => (
            <div
              key={agent.id}
              className="flex flex-col gap-2 rounded-lg border border-zinc-800 bg-zinc-950/40 p-3 sm:flex-row sm:items-center sm:justify-between"
            >
              <div>
                <div className="text-sm font-medium text-white">
                  {agent.name}
                  <span className="text-xs text-zinc-400"> · {agent.model}</span>
                </div>
                <div className="text-xs text-zinc-500">{agent.detail || agent.id}</div>
              </div>
              <span
                className={`self-start rounded-full px-2 py-0.5 text-[10px] font-semibold sm:self-auto ${statusClasses(
                  agent.status,
                )}`}
              >
                {statusLabel(agent.status)}
              </span>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
