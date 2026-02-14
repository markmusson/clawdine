'use client';

import { useEffect, useState, useCallback } from 'react';

interface AttestationStatus {
  healthy: boolean;
  chainLength: number;
  gaps: number[];
  lastAttestationAt: string | null;
  lastStatus: string | null;
  lastSequence?: number;
}

export default function ClawdSureStatus() {
  const [status, setStatus] = useState<AttestationStatus | null>(null);
  const [loading, setLoading] = useState(true);

  const fetchStatus = useCallback(async () => {
    try {
      const res = await fetch('/api/clawdsure');
      const data = await res.json();
      setStatus(data);
    } catch {
      setStatus(null);
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
          <span className="text-xl">🛡️</span>
          ClawdSure Attestation
        </h2>
        {status && (
          <span
            className={`px-2 py-0.5 text-xs font-semibold rounded-full ${
              status.healthy
                ? 'bg-emerald-500/20 text-emerald-300'
                : 'bg-rose-500/20 text-rose-300'
            }`}
          >
            {status.healthy ? 'Healthy' : 'Attention'}
          </span>
        )}
      </div>

      {loading ? (
        <div className="text-sm text-zinc-400">Loading status…</div>
      ) : !status ? (
        <div className="text-sm text-rose-300">Unable to read attestation log.</div>
      ) : (
        <div className="space-y-3 text-sm">
          <div className="flex items-center justify-between">
            <span className="text-zinc-500">Last attestation</span>
            <span className="font-mono text-zinc-100">
              {status.lastAttestationAt
                ? new Date(status.lastAttestationAt).toLocaleString()
                : '—'}
            </span>
          </div>
          <div className="flex items-center justify-between">
            <span className="text-zinc-500">Chain length</span>
            <span className="font-semibold text-zinc-100">#{status.chainLength}</span>
          </div>
          <div className="flex items-center justify-between">
            <span className="text-zinc-500">Last status</span>
            <span className="font-semibold text-zinc-100">
              {status.lastStatus || 'UNKNOWN'}
            </span>
          </div>
          {status.gaps?.length > 0 && (
            <div className="rounded-lg border border-rose-500/30 bg-rose-500/10 p-2 text-xs text-rose-200">
              Missing attestations: {status.gaps.join(', ')}
            </div>
          )}
        </div>
      )}
    </div>
  );
}
