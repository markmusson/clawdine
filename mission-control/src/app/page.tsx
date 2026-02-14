import AgentOverview from '@/components/AgentOverview';
import ClawdSureStatus from '@/components/ClawdSureStatus';
import CronJobs from '@/components/CronJobs';
import MemoryStatus from '@/components/MemoryStatus';
import QuickActions from '@/components/QuickActions';

export default function Home() {
  return (
    <div className="min-h-screen bg-zinc-950 text-white">
      <header className="border-b border-zinc-900 bg-zinc-950/80 backdrop-blur">
        <div className="mx-auto flex max-w-6xl items-center justify-between px-6 py-5">
          <div className="flex items-center gap-3">
            <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-zinc-900">
              <span className="text-xl">🐾</span>
            </div>
            <div>
              <h1 className="text-xl font-semibold">Mission Control</h1>
              <p className="text-xs text-zinc-400">OpenClaw Local Dashboard</p>
            </div>
          </div>
          <time className="text-xs text-zinc-400">
            {new Date().toLocaleString('en-GB', {
              weekday: 'short',
              month: 'short',
              day: 'numeric',
              hour: '2-digit',
              minute: '2-digit',
            })}
          </time>
        </div>
      </header>

      <main className="mx-auto grid max-w-6xl grid-cols-1 gap-6 px-6 py-8 lg:grid-cols-2">
        <div className="space-y-6">
          <AgentOverview />
          <CronJobs />
          <ClawdSureStatus />
        </div>
        <div className="space-y-6">
          <MemoryStatus />
          <QuickActions />
        </div>
      </main>
    </div>
  );
}
