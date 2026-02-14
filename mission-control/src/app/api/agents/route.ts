import { NextResponse } from 'next/server';
import { homedir } from 'os';
import { join } from 'path';
import { stat } from 'fs/promises';

const AGENTS = [
  {
    id: 'main',
    name: 'Clawdine',
    model: 'Opus',
  },
  {
    id: 'clawdsure',
    name: 'ClawdSure',
    model: 'Sonnet',
  },
];

async function exists(path: string) {
  try {
    await stat(path);
    return true;
  } catch {
    return false;
  }
}

export async function GET() {
  const agents = await Promise.all(
    AGENTS.map(async (agent) => {
      const agentDir = join(homedir(), '.openclaw', 'agents', agent.id, 'agent');
      const memoryDb = join(homedir(), '.openclaw', 'memory', `${agent.id}.sqlite`);
      const hasAgentDir = await exists(agentDir);
      const hasMemory = await exists(memoryDb);

      let status: 'ready' | 'missing' | 'unknown' = 'unknown';
      let detail = '';

      if (hasAgentDir || hasMemory) {
        status = 'ready';
        detail = hasMemory ? 'Memory DB available' : 'Config found';
      } else {
        status = 'missing';
        detail = 'Agent config missing';
      }

      return {
        id: agent.id,
        name: agent.name,
        model: agent.model,
        status,
        detail,
      };
    }),
  );

  return NextResponse.json({ agents });
}
