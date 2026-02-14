import { NextResponse } from 'next/server';
import { readdir, readFile, stat } from 'fs/promises';
import { join, relative } from 'path';

const WORKSPACE_DIR = process.env.HOME 
  ? join(process.env.HOME, '.openclaw', 'workspace')
  : '/Users/clawdine/.openclaw/workspace';

interface SearchResult {
  id: string;
  file: string;
  relativePath: string;
  matches: {
    line: number;
    content: string;
    highlight: { start: number; end: number }[];
  }[];
  score: number;
}

async function* walkDir(dir: string): AsyncGenerator<string> {
  try {
    const entries = await readdir(dir, { withFileTypes: true });
    for (const entry of entries) {
      const fullPath = join(dir, entry.name);
      
      // Skip node_modules, .git, and mission-control itself
      if (entry.name === 'node_modules' || entry.name === '.git' || entry.name === 'mission-control') {
        continue;
      }
      
      if (entry.isDirectory()) {
        yield* walkDir(fullPath);
      } else if (entry.name.endsWith('.md') || entry.name.endsWith('.txt') || entry.name.endsWith('.json')) {
        yield fullPath;
      }
    }
  } catch {
    // Directory not accessible
  }
}

function findMatches(content: string, query: string): { line: number; content: string; highlight: { start: number; end: number }[] }[] {
  const lines = content.split('\n');
  const matches: { line: number; content: string; highlight: { start: number; end: number }[] }[] = [];
  const queryLower = query.toLowerCase();
  
  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];
    const lineLower = line.toLowerCase();
    
    if (lineLower.includes(queryLower)) {
      const highlights: { start: number; end: number }[] = [];
      let pos = 0;
      
      while (true) {
        const idx = lineLower.indexOf(queryLower, pos);
        if (idx === -1) break;
        highlights.push({ start: idx, end: idx + query.length });
        pos = idx + 1;
      }
      
      matches.push({
        line: i + 1,
        content: line.slice(0, 200),
        highlight: highlights,
      });
    }
  }
  
  return matches.slice(0, 5); // Limit matches per file
}

export async function GET(request: Request) {
  try {
    const { searchParams } = new URL(request.url);
    const query = searchParams.get('q') || '';
    const limit = parseInt(searchParams.get('limit') || '20');
    
    if (!query || query.length < 2) {
      return NextResponse.json({ results: [], message: 'Query too short' });
    }
    
    const results: SearchResult[] = [];
    
    for await (const filePath of walkDir(WORKSPACE_DIR)) {
      if (results.length >= limit) break;
      
      try {
        const fileStat = await stat(filePath);
        if (fileStat.size > 1024 * 1024) continue; // Skip files > 1MB
        
        const content = await readFile(filePath, 'utf-8');
        const matches = findMatches(content, query);
        
        if (matches.length > 0) {
          results.push({
            id: filePath,
            file: filePath,
            relativePath: relative(WORKSPACE_DIR, filePath),
            matches,
            score: matches.length,
          });
        }
      } catch {
        // File not readable
      }
    }
    
    // Sort by score
    results.sort((a, b) => b.score - a.score);
    
    return NextResponse.json({ results: results.slice(0, limit) });
  } catch (error) {
    return NextResponse.json({ error: String(error), results: [] }, { status: 500 });
  }
}
