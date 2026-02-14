import { NextResponse } from 'next/server';
import { readFile } from 'fs/promises';
import { join } from 'path';

const WORKSPACE_DIR = process.env.HOME
  ? join(process.env.HOME, '.openclaw', 'workspace')
  : '/Users/clawdine/.openclaw/workspace';
const CLAWDSURE_LOG = join(WORKSPACE_DIR, '.clawdsure', 'attestation.log');

interface AttestationEntry {
  timestamp: string;
  sequence: number;
  status: string;
  raw: string;
}

function parseLine(line: string): AttestationEntry | null {
  const parts = line.split('|').map((p) => p.trim());
  if (parts.length < 3) return null;
  const timestamp = parts[0];
  const seqMatch = parts[1]?.match(/#(\d+)/);
  const sequence = seqMatch ? Number(seqMatch[1]) : NaN;
  const status = parts[2] || 'UNKNOWN';
  if (!timestamp || Number.isNaN(sequence)) return null;
  return { timestamp, sequence, status, raw: line };
}

export async function GET() {
  try {
    const content = await readFile(CLAWDSURE_LOG, 'utf-8');
    const entries = content
      .split('\n')
      .map((line) => line.trim())
      .filter(Boolean)
      .map(parseLine)
      .filter((entry): entry is AttestationEntry => Boolean(entry));

    if (entries.length === 0) {
      return NextResponse.json({
        healthy: false,
        chainLength: 0,
        gaps: [],
        lastAttestationAt: null,
        lastStatus: 'UNKNOWN',
      });
    }

    const sequences = entries.map((e) => e.sequence);
    const maxSeq = Math.max(...sequences);
    const minSeq = Math.min(...sequences);
    const sequenceSet = new Set(sequences);
    const gaps: number[] = [];

    for (let i = minSeq; i <= maxSeq; i += 1) {
      if (!sequenceSet.has(i)) gaps.push(i);
    }

    const sortedByTime = [...entries].sort(
      (a, b) => new Date(a.timestamp).getTime() - new Date(b.timestamp).getTime(),
    );
    const last = sortedByTime[sortedByTime.length - 1];

    const healthy = gaps.length === 0 && last.status.toUpperCase() === 'PASS';

    return NextResponse.json({
      healthy,
      chainLength: maxSeq,
      gaps,
      lastAttestationAt: last.timestamp,
      lastStatus: last.status,
      lastSequence: last.sequence,
    });
  } catch (error) {
    return NextResponse.json(
      { error: String(error), healthy: false, chainLength: 0, gaps: [] },
      { status: 500 },
    );
  }
}
