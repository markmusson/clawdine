import { NextResponse } from 'next/server';
import { execFile } from 'child_process';
import { promisify } from 'util';
import { homedir } from 'os';
import { join } from 'path';
import { stat } from 'fs/promises';

const execFileAsync = promisify(execFile);

const MEMORY_DBS = [
  {
    id: 'main',
    label: 'Clawdine (Opus)',
    path: join(homedir(), '.openclaw', 'memory', 'main.sqlite'),
  },
  {
    id: 'clawdsure',
    label: 'ClawdSure (Sonnet)',
    path: join(homedir(), '.openclaw', 'memory', 'clawdsure.sqlite'),
  },
];

async function readCounts(dbPath: string) {
  try {
    await stat(dbPath);
  } catch (error) {
    return {
      available: false,
      files: 0,
      chunks: 0,
      error: `Missing database: ${String(error)}`,
    };
  }

  try {
    const { stdout } = await execFileAsync('sqlite3', [
      '-separator',
      ',',
      dbPath,
      'select (select count(*) from files), (select count(*) from chunks);',
    ]);
    const [filesRaw, chunksRaw] = stdout.trim().split(',');
    const files = Number.parseInt(filesRaw || '0', 10);
    const chunks = Number.parseInt(chunksRaw || '0', 10);

    return {
      available: true,
      files: Number.isNaN(files) ? 0 : files,
      chunks: Number.isNaN(chunks) ? 0 : chunks,
    };
  } catch (error) {
    return {
      available: false,
      files: 0,
      chunks: 0,
      error: `SQLite error: ${String(error)}`,
    };
  }
}

export async function GET() {
  const agents = await Promise.all(
    MEMORY_DBS.map(async (agent) => ({
      id: agent.id,
      label: agent.label,
      ...(await readCounts(agent.path)),
    })),
  );

  return NextResponse.json({ agents });
}
