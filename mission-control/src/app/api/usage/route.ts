import { NextResponse } from 'next/server';
import { readFile } from 'fs/promises';
import { join } from 'path';

function getLogPath() {
  const today = new Date();
  const yyyy = today.getFullYear();
  const mm = String(today.getMonth() + 1).padStart(2, '0');
  const dd = String(today.getDate()).padStart(2, '0');
  return join('/tmp', 'openclaw', `openclaw-${yyyy}-${mm}-${dd}.log`);
}

export async function GET() {
  try {
    const logPath = getLogPath();
    const content = await readFile(logPath, 'utf-8');
    const lines = content.split('\n').filter(Boolean);

    let inputTokens = 0;
    let outputTokens = 0;
    let totalCostUsd = 0;
    let found = false;

    for (const line of lines) {
      if (!line.trim().startsWith('{')) continue;
      try {
        const payload = JSON.parse(line);
        if (payload.usage) {
          found = true;
          inputTokens += payload.usage.inputTokens || 0;
          outputTokens += payload.usage.outputTokens || 0;
          totalCostUsd += payload.usage.totalCostUsd || 0;
        }
      } catch {
        // ignore
      }
    }

    return NextResponse.json({
      available: found,
      inputTokens,
      outputTokens,
      totalCostUsd,
    });
  } catch (error) {
    return NextResponse.json({
      available: false,
      inputTokens: 0,
      outputTokens: 0,
      totalCostUsd: 0,
      error: String(error),
    });
  }
}
