import { NextResponse } from 'next/server';
import { readFile } from 'fs/promises';
import { join } from 'path';

const OPENCLAW_DIR = process.env.HOME
  ? join(process.env.HOME, '.openclaw')
  : '/Users/clawdine/.openclaw';
const CRON_FILE = join(OPENCLAW_DIR, 'cron', 'jobs.json');
const CONFIG_FILE = join(OPENCLAW_DIR, 'openclaw.json');

interface CronJob {
  id: string;
  name: string;
  schedule: string;
  nextRun: string | null;
  lastRun: string | null;
  lastStatus?: string | null;
  enabled: boolean;
  command?: string;
}

function parseSchedule(schedule: string): { description: string; nextRun: Date | null } {
  const parts = schedule.split(' ');
  if (parts.length < 5) return { description: schedule, nextRun: null };

  const [minute, hour, , , dayOfWeek] = parts;

  let description = '';

  if (minute === '*' && hour === '*') {
    description = 'Every minute';
  } else if (minute !== '*' && hour === '*') {
    description = `Every hour at :${minute}`;
  } else if (minute !== '*' && hour !== '*') {
    const hourNum = parseInt(hour);
    const period = hourNum >= 12 ? 'PM' : 'AM';
    const displayHour = hourNum > 12 ? hourNum - 12 : hourNum || 12;
    description = `Daily at ${displayHour}:${minute.padStart(2, '0')} ${period}`;
  }

  if (dayOfWeek !== '*') {
    const days = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];
    description += ` on ${days[parseInt(dayOfWeek)] || dayOfWeek}`;
  }

  const now = new Date();
  const nextRun = new Date();

  if (minute !== '*') nextRun.setMinutes(parseInt(minute));
  if (hour !== '*') nextRun.setHours(parseInt(hour));
  nextRun.setSeconds(0);
  nextRun.setMilliseconds(0);

  if (nextRun <= now) {
    nextRun.setDate(nextRun.getDate() + 1);
  }

  return { description: description || schedule, nextRun };
}

async function fetchGatewayJobs(token: string | undefined) {
  try {
    const response = await fetch('http://127.0.0.1:18789/api/cron/jobs', {
      headers: token ? { Authorization: `Bearer ${token}` } : undefined,
    });
    const contentType = response.headers.get('content-type') || '';
    if (!response.ok || !contentType.includes('application/json')) {
      return null;
    }
    return await response.json();
  } catch {
    return null;
  }
}

export async function GET() {
  try {
    const jobs: CronJob[] = [];
    let config: any = null;

    try {
      const configContent = await readFile(CONFIG_FILE, 'utf-8');
      config = JSON.parse(configContent);
    } catch {
      config = null;
    }

    await fetchGatewayJobs(config?.gateway?.auth?.token);

    try {
      const cronContent = await readFile(CRON_FILE, 'utf-8');
      const cronData = JSON.parse(cronContent);

      if (cronData.jobs && Array.isArray(cronData.jobs)) {
        for (const job of cronData.jobs) {
          const scheduleExpr = job.schedule?.expr || job.schedule || job.cron || '';
          const { description, nextRun } = parseSchedule(scheduleExpr);
          jobs.push({
            id: job.id || job.name || String(Math.random()),
            name: job.name || job.label || 'Unnamed Job',
            schedule: description,
            nextRun: job.state?.nextRunAtMs
              ? new Date(job.state.nextRunAtMs).toISOString()
              : job.nextRunAt || nextRun?.toISOString() || null,
            lastRun: job.state?.lastRunAtMs
              ? new Date(job.state.lastRunAtMs).toISOString()
              : job.lastRunAt || null,
            lastStatus: job.state?.lastStatus || null,
            enabled: job.enabled !== false,
            command: job.command || job.prompt,
          });
        }
      }
    } catch {
      // Cron file might not exist or be empty
    }

    if (config?.agents?.defaults?.heartbeat) {
      const hb = config.agents.defaults.heartbeat;
      const everyMs = parseInterval(hb.every || '30m');
      const nextRun = new Date(Date.now() + everyMs);

      jobs.push({
        id: 'heartbeat',
        name: 'Heartbeat Check',
        schedule: `Every ${hb.every || '30m'}`,
        nextRun: nextRun.toISOString(),
        lastRun: null,
        lastStatus: null,
        enabled: true,
        command: 'Heartbeat poll',
      });
    }

    return NextResponse.json({ jobs });
  } catch (error) {
    return NextResponse.json({ error: String(error), jobs: [] }, { status: 500 });
  }
}

function parseInterval(interval: string): number {
  const match = interval.match(/^(\d+)(s|m|h|d)$/);
  if (!match) return 1800000;

  const value = parseInt(match[1]);
  const unit = match[2];

  switch (unit) {
    case 's':
      return value * 1000;
    case 'm':
      return value * 60 * 1000;
    case 'h':
      return value * 60 * 60 * 1000;
    case 'd':
      return value * 24 * 60 * 60 * 1000;
    default:
      return 1800000;
  }
}
