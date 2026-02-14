'use client';

import { useState } from 'react';

const ACTIONS = [
  {
    id: 'gap-alert',
    label: 'Run Gap Alert Cron',
    description: 'Trigger the scheduled gap alert job now',
  },
  {
    id: 'attest',
    label: 'Run Attestation',
    description: 'Run ClawdSure attestation on demand',
  },
  {
    id: 'gateway-status',
    label: 'Gateway Status',
    description: 'Check OpenClaw gateway health',
  },
];

export default function QuickActions() {
  const [running, setRunning] = useState<string | null>(null);
  const [result, setResult] = useState<string>('');

  const runAction = async (action: string) => {
    setRunning(action);
    setResult('');
    try {
      const res = await fetch('/api/actions', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ action }),
      });
      const data = await res.json();
      const output = [data.stdout, data.stderr].filter(Boolean).join('\n');
      setResult(output || (data.ok ? 'Done.' : data.error || 'Failed'));
    } catch (error) {
      setResult(String(error));
    } finally {
      setRunning(null);
    }
  };

  return (
    <div className="bg-zinc-900/60 rounded-xl border border-zinc-800 p-6">
      <div className="flex items-center gap-2 mb-4">
        <span className="text-xl">⚡</span>
        <h2 className="text-lg font-semibold text-white">Quick Actions</h2>
      </div>
      <div className="space-y-3">
        {ACTIONS.map((action) => (
          <button
            key={action.id}
            onClick={() => runAction(action.id)}
            disabled={running === action.id}
            className="w-full text-left px-4 py-3 rounded-lg border border-zinc-800 bg-zinc-950/40 hover:bg-zinc-900/80 transition-colors disabled:opacity-60"
          >
            <div className="flex items-center justify-between">
              <span className="font-medium text-white">{action.label}</span>
              {running === action.id && (
                <span className="text-xs text-zinc-400">Running…</span>
              )}
            </div>
            <p className="text-xs text-zinc-400 mt-1">{action.description}</p>
          </button>
        ))}
      </div>
      {result && (
        <pre className="mt-4 max-h-40 overflow-y-auto text-xs bg-zinc-950/40 border border-zinc-800 rounded-lg p-3 whitespace-pre-wrap text-zinc-200">
          {result}
        </pre>
      )}
    </div>
  );
}
