import { NextResponse } from 'next/server';
import { readdir, readFile } from 'fs/promises';
import { join } from 'path';

const LOG_DIR = '/tmp/openclaw';

interface LogEntry {
  id: string;
  timestamp: string;
  level: string;
  subsystem: string;
  message: string;
  type: 'info' | 'warn' | 'error' | 'debug';
}

function parseLogLine(line: string, index: number): LogEntry | null {
  try {
    const data = JSON.parse(line);
    const meta = data._meta || {};
    const time = data.time || meta.date || new Date().toISOString();
    const level = meta.logLevelName || 'INFO';
    
    // Extract subsystem from the "0" field or name
    let subsystem = 'system';
    const nameField = data['0'] || meta.name || '';
    if (typeof nameField === 'string') {
      try {
        const parsed = JSON.parse(nameField);
        subsystem = parsed.subsystem || parsed.module || 'system';
      } catch {
        subsystem = nameField.slice(0, 50);
      }
    }
    
    // Extract message from "1" or "2" field
    let message = data['1'] || data['2'] || '';
    if (typeof message === 'object') {
      message = JSON.stringify(message);
    }
    
    // Skip very verbose debug logs
    if (level === 'DEBUG' && !message.includes('tool') && !message.includes('session')) {
      return null;
    }
    
    return {
      id: `${time}-${index}`,
      timestamp: time,
      level,
      subsystem,
      message: String(message).slice(0, 500),
      type: level === 'ERROR' ? 'error' : level === 'WARN' ? 'warn' : level === 'DEBUG' ? 'debug' : 'info',
    };
  } catch {
    return null;
  }
}

export async function GET(request: Request) {
  try {
    const { searchParams } = new URL(request.url);
    const limit = parseInt(searchParams.get('limit') || '100');
    const date = searchParams.get('date') || new Date().toISOString().split('T')[0];
    
    const logFile = join(LOG_DIR, `openclaw-${date}.log`);
    
    let content: string;
    try {
      content = await readFile(logFile, 'utf-8');
    } catch {
      // Try to list available log files
      try {
        const files = await readdir(LOG_DIR);
        const logFiles = files.filter(f => f.startsWith('openclaw-') && f.endsWith('.log'));
        if (logFiles.length > 0) {
          const latestLog = logFiles.sort().reverse()[0];
          content = await readFile(join(LOG_DIR, latestLog), 'utf-8');
        } else {
          return NextResponse.json({ entries: [], message: 'No log files found' });
        }
      } catch {
        return NextResponse.json({ entries: [], message: 'Log directory not accessible' });
      }
    }
    
    const lines = content.trim().split('\n');
    const entries: LogEntry[] = [];
    
    // Parse from the end (most recent)
    for (let i = lines.length - 1; i >= 0 && entries.length < limit; i--) {
      const entry = parseLogLine(lines[i], i);
      if (entry) {
        entries.push(entry);
      }
    }
    
    return NextResponse.json({ entries });
  } catch (error) {
    return NextResponse.json({ error: String(error), entries: [] }, { status: 500 });
  }
}
