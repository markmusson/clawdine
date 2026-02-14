'use client';

import { useCallback, useEffect, useState } from 'react';

interface CronJob {
  id: string;
  name: string;
  schedule: string;
  nextRun: string | null;
  lastRun: string | null;
  lastStatus?: string | null;
  enabled: boolean;
}

export default function CronJobs() {
  const [jobs, setJobs] = useState<CronJob[]>([]);
  const [loading, setLoading] = useState(true);

  const fetchJobs = useCallback(async () => {
    try {
      const res = await fetch('/api/cron');
      const data = await res.json();
      setJobs(data.jobs || []);
    } catch {
      setJobs([]);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchJobs();
    const interval = setInterval(fetchJobs, 60000);
    return () => clearInterval(interval);
  }, [fetchJobs]);

  const formatTimestamp = (value: string | null) => {
    if (!value) return '—';
    const date = new Date(value);
    return date.toLocaleString();
  };

  return (
    <div className="bg-zinc-900/60 rounded-xl border border-zinc-800 p-6">
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-lg font-semibold text-white flex items-center gap-2">
          <span>⏱️</span>
          Cron Jobs
        </h2>
        <span className="text-xs text-zinc-400">Auto-refresh 60s</span>
      </div>

      {loading ? (
        <div className="text-sm text-zinc-400">Loading cron jobs…</div>
      ) : jobs.length === 0 ? (
        <div className="text-sm text-zinc-400">No cron jobs found.</div>
      ) : (
        <div className="space-y-3">
          {jobs.map((job) => (
            <div
              key={job.id}
              className="rounded-lg border border-zinc-800 bg-zinc-950/40 p-3"
            >
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <span
                    className={`h-2.5 w-2.5 rounded-full ${
                      job.enabled ? 'bg-emerald-400' : 'bg-zinc-500'
                    }`}
                  />
                  <span className="text-sm font-medium text-white">{job.name}</span>
                  {job.lastStatus && (
                    <span
                      className={`text-[10px] px-2 py-0.5 rounded-full ${
                        job.lastStatus === 'ok'
                          ? 'bg-emerald-500/20 text-emerald-300'
                          : 'bg-rose-500/20 text-rose-300'
                      }`}
                    >
                      {job.lastStatus.toUpperCase()}
                    </span>
                  )}
                </div>
                <span className="text-xs text-zinc-400">{job.schedule}</span>
              </div>
              <div className="mt-2 grid grid-cols-1 gap-2 text-xs text-zinc-400 sm:grid-cols-2">
                <div>
                  <span className="text-zinc-500">Last run:</span>{' '}
                  <span className="text-zinc-200">{formatTimestamp(job.lastRun)}</span>
                </div>
                <div>
                  <span className="text-zinc-500">Next run:</span>{' '}
                  <span className="text-zinc-200">{formatTimestamp(job.nextRun)}</span>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
