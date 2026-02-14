import { NextResponse } from 'next/server';
import { readFile } from 'fs/promises';
import { join } from 'path';

const WORKSPACE_DIR = process.env.HOME
  ? join(process.env.HOME, '.openclaw', 'workspace')
  : '/Users/clawdine/.openclaw/workspace';
const PRICE_LOG = join(WORKSPACE_DIR, 'trading', 'backtest', 'price_log.jsonl');

interface PriceLogEntry {
  timestamp: string;
  target_date: string;
  forecast_source?: string;
  forecast_high_f: number;
  market_implied: string;
  market_confidence: number;
  days_until: number;
}

function safeParse(line: string): PriceLogEntry | null {
  try {
    const parsed = JSON.parse(line);
    if (!parsed.timestamp || !parsed.target_date) return null;
    return parsed as PriceLogEntry;
  } catch {
    return null;
  }
}

export async function GET() {
  try {
    const content = await readFile(PRICE_LOG, 'utf-8');
    const entries = content
      .split('\n')
      .map((line) => line.trim())
      .filter(Boolean)
      .map(safeParse)
      .filter((entry): entry is PriceLogEntry => Boolean(entry));

    if (entries.length === 0) {
      return NextResponse.json({ entries: [], latestTimestamp: null });
    }

    const latestTimestamp = entries
      .map((e) => e.timestamp)
      .sort()
      .slice(-1)[0];

    const latestEntries = entries
      .filter((e) => e.timestamp === latestTimestamp)
      .sort((a, b) => a.target_date.localeCompare(b.target_date));

    const fallback = entries
      .slice(-5)
      .sort((a, b) => a.target_date.localeCompare(b.target_date));

    return NextResponse.json({
      latestTimestamp,
      entries: latestEntries.length > 0 ? latestEntries : fallback,
    });
  } catch (error) {
    return NextResponse.json(
      { error: String(error), entries: [], latestTimestamp: null },
      { status: 500 },
    );
  }
}
