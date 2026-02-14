import { NextResponse } from 'next/server';
import { exec } from 'child_process';
import { promisify } from 'util';

const execAsync = promisify(exec);

const ACTIONS: Record<string, string> = {
  'gap-alert': 'bash /Users/clawdine/.openclaw/workspace/trading/backtest/gap_alert_silent.sh',
  attest: 'bash /Users/clawdine/.openclaw/workspace/skills/clawdsure/scripts/attest.sh',
  'gateway-status': 'openclaw gateway status',
};

export async function POST(request: Request) {
  try {
    const body = await request.json();
    const action = body.action as string;
    const command = ACTIONS[action];

    if (!command) {
      return NextResponse.json({ error: 'Unknown action' }, { status: 400 });
    }

    const { stdout, stderr } = await execAsync(command, {
      timeout: 120000,
      env: process.env,
    });

    return NextResponse.json({
      action,
      ok: true,
      stdout: stdout?.trim() || '',
      stderr: stderr?.trim() || '',
    });
  } catch (error) {
    return NextResponse.json(
      { ok: false, error: String(error) },
      { status: 500 },
    );
  }
}
