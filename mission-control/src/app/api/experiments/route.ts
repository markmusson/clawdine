import { NextResponse } from 'next/server';
import { readFile } from 'fs/promises';

const EXPERIMENTS_FILE = '/Users/clawdine/.openclaw/workspace/trading/experiments.md';

interface Trade {
  date: string;
  market: string;
  position: string;
  entry: string;
  forecast: string;
  actual: string;
  result: string;
  pnl: string;
}

interface DataPoint {
  date: string;
  city: string;
  horizon: string;
  forecast: string;
  actual: string;
  error: string;
}

interface Experiment {
  id: string;
  hypothesis: string;
  status: 'active' | 'validated' | 'invalidated' | 'pending';
  result: string;
  fullHypothesis?: string;
  testCriteria?: string;
  timeline?: string;
  trades?: Trade[];
  data?: DataPoint[];
  learnings?: string;
}

function parseStatus(statusText: string): 'active' | 'validated' | 'invalidated' | 'pending' {
  if (statusText.includes('🔬') || statusText.toLowerCase().includes('active')) return 'active';
  if (statusText.includes('✅') || statusText.toLowerCase().includes('validated')) return 'validated';
  if (statusText.includes('❌') || statusText.toLowerCase().includes('invalidated')) return 'invalidated';
  return 'pending';
}

function parseMarkdownTable(tableText: string): Record<string, string>[] {
  const lines = tableText.trim().split('\n').filter(line => line.trim());
  if (lines.length < 2) return [];
  
  // Parse header
  const headers = lines[0]
    .split('|')
    .map(h => h.trim().toLowerCase())
    .filter(h => h && h !== '---' && !h.match(/^-+$/));
  
  // Skip separator line
  const dataLines = lines.slice(2);
  
  return dataLines.map(line => {
    const cells = line.split('|').map(c => c.trim()).filter((_, i, arr) => i > 0 && i < arr.length - 1 || arr.length <= 2);
    // Handle edge case where split creates empty first/last elements
    const cleanCells = line.split('|').slice(1, -1).map(c => c.trim());
    
    const row: Record<string, string> = {};
    headers.forEach((header, i) => {
      row[header] = cleanCells[i] || '';
    });
    return row;
  });
}

function parseExperiments(content: string): Experiment[] {
  const experiments: Experiment[] = [];
  
  // Parse summary table first
  const summaryMatch = content.match(/## Summary\s*\n\n([\s\S]*?)(?=\n---|\n## (?!Summary))/);
  const summaryTable = summaryMatch ? parseMarkdownTable(summaryMatch[1]) : [];
  
  // Create map of summary data
  const summaryMap = new Map<string, { hypothesis: string; status: string; result: string }>();
  summaryTable.forEach(row => {
    const id = row['id'] || '';
    if (id) {
      summaryMap.set(id, {
        hypothesis: row['hypothesis'] || '',
        status: row['status'] || '',
        result: row['result'] || '',
      });
    }
  });
  
  // Parse individual experiment sections
  const expSections = content.split(/\n## (EXP-\d+):/);
  
  for (let i = 1; i < expSections.length; i += 2) {
    const id = expSections[i];
    const sectionContent = expSections[i + 1] || '';
    
    const summary = summaryMap.get(id);
    
    // Extract hypothesis
    const hypothesisMatch = sectionContent.match(/\*\*Hypothesis:\*\*\s*([\s\S]*?)(?=\n\*\*|\n\n##)/);
    const fullHypothesis = hypothesisMatch ? hypothesisMatch[1].trim() : summary?.hypothesis || '';
    
    // Extract status
    const statusMatch = sectionContent.match(/\*\*Status:\*\*\s*(.+)/);
    const statusText = statusMatch ? statusMatch[1].trim() : summary?.status || '';
    
    // Extract success criteria
    const criteriaMatch = sectionContent.match(/\*\*Success Criteria:\*\*\s*([\s\S]*?)(?=\n\*\*|\n\n##)/);
    const testCriteria = criteriaMatch ? criteriaMatch[1].trim().replace(/\n-/g, '; -') : '';
    
    // Extract timeline
    const timelineMatch = sectionContent.match(/\*\*Timeline:\*\*\s*(.+)/);
    const timeline = timelineMatch ? timelineMatch[1].trim() : '';
    
    // Extract trades table
    const tradesMatch = sectionContent.match(/\*\*Trades:\*\*\s*\n([\s\S]*?)(?=\n\*\*|\n\n---|\n\n##|$)/);
    let trades: Trade[] = [];
    if (tradesMatch) {
      const tradeRows = parseMarkdownTable(tradesMatch[1]);
      trades = tradeRows.map(row => ({
        date: row['date'] || '',
        market: row['market'] || '',
        position: row['position'] || '',
        entry: row['entry'] || '',
        forecast: row['forecast'] || '',
        actual: row['actual'] || '',
        result: row['result'] || '',
        pnl: row['p&l'] || row['pnl'] || '',
      }));
    }
    
    // Extract data table (for EXP-002 style experiments)
    const dataMatch = sectionContent.match(/\*\*Data:\*\*\s*\n([\s\S]*?)(?=\n\*\*|\n\n---|\n\n##|$)/);
    let data: DataPoint[] = [];
    if (dataMatch) {
      const dataRows = parseMarkdownTable(dataMatch[1]);
      data = dataRows.map(row => ({
        date: row['date'] || '',
        city: row['city'] || '',
        horizon: row['horizon'] || '',
        forecast: row['forecast'] || '',
        actual: row['actual'] || '',
        error: row['error'] || '',
      }));
    }
    
    // Extract learnings
    const learningsMatch = sectionContent.match(/\*\*Learnings:\*\*\s*([\s\S]*?)(?=\n\n---|\n\n##|$)/);
    const learnings = learningsMatch ? learningsMatch[1].trim() : '';
    
    experiments.push({
      id,
      hypothesis: summary?.hypothesis || fullHypothesis.split('\n')[0],
      status: parseStatus(statusText),
      result: summary?.result || 'Pending',
      fullHypothesis,
      testCriteria,
      timeline,
      trades: trades.length > 0 ? trades : undefined,
      data: data.length > 0 ? data : undefined,
      learnings: learnings && learnings !== '*(To be updated)*' ? learnings : undefined,
    });
  }
  
  return experiments;
}

export async function GET() {
  try {
    const content = await readFile(EXPERIMENTS_FILE, 'utf-8');
    const experiments = parseExperiments(content);
    
    // Calculate stats
    const stats = {
      total: experiments.length,
      active: experiments.filter(e => e.status === 'active').length,
      validated: experiments.filter(e => e.status === 'validated').length,
      invalidated: experiments.filter(e => e.status === 'invalidated').length,
    };
    
    return NextResponse.json({ 
      experiments, 
      stats,
      lastUpdated: new Date().toISOString(),
    });
  } catch (error) {
    return NextResponse.json({ 
      error: String(error), 
      experiments: [],
      stats: { total: 0, active: 0, validated: 0, invalidated: 0 },
    }, { status: 500 });
  }
}
