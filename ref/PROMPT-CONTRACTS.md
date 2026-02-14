# PROMPT-CONTRACTS.md — How to Write Every Prompt

Every prompt is a contract. Not a creative brief. Not a suggestion. A contract.

---

## The Four Components

### 1. GOAL
What does success look like? Quantified. Measurable. No ambiguity.

- Bad: "Make it good"
- Good: "One Telegram message Mark reads in <60 seconds that surfaces decisions needed today"
- Bad: "Write a report"
- Good: "Generate a deal sheet that Sam Clifton can scan in 2 minutes and know whether to take the next meeting"

**Quantify the win condition.** If you can't measure it, you can't tell if it worked.

### 2. CONSTRAINTS
Hard boundaries. Non-negotiable. The walls the output must stay within.

- Word count limits
- Tone rules (no corporate, no filler, no hedging)
- Data freshness requirements
- Security boundaries (stealth mode, no public details)
- Model/cost limits
- Time limits

**If it's not a constraint, it's a suggestion. Suggestions get ignored.**

### 3. OUTPUT FORMAT
Exact structure. Not "a summary" — the specific shape of the output.

- Section headers
- Field names
- Data types
- Example output (if complex)
- Delivery channel and format (Telegram message, markdown file, JSON)

**The more specific the format, the less post-processing needed.**

### 4. FAILURE CONDITIONS
What breaks the contract. What makes the output worthless. The rejection criteria.

- "If it sounds like marketing copy" → FAIL
- "If any data source is >24h stale without flagging it" → FAIL
- "If it exceeds word count" → FAIL
- "If it contains hallucinated references" → FAIL
- "If it requires Mark to ask a follow-up question to understand it" → FAIL

**Failure conditions are the most underused component. They prevent the 80% of bad output that technically meets the goal but is useless.**

---

## Template

```
GOAL: [Exact success metric — what does done look like?]

CONSTRAINTS:
- [Hard boundary 1]
- [Hard boundary 2]
- [Hard boundary 3]

FORMAT:
[Exact output structure]

FAILURE:
- [What makes this worthless — condition 1]
- [What makes this worthless — condition 2]
```

---

## Examples

### Morning Brief (Cron Job)

```
GOAL: One Telegram message Mark reads in <60 seconds
      that surfaces decisions needed TODAY.

CONSTRAINTS:
- <500 words
- No stale data without timestamp ("as of [time]")
- No filler, no preamble, no "Good morning!"
- Haiku model (cost discipline)

FORMAT:
## Overnight
[What happened since last brief — 2-3 bullets max]

## Needs Your Decision
[Decisions only Mark can make — numbered list]

## Running Fine
[One line per item that needs no action]

**Top priority:** [Single sentence]

FAILURE:
- If it reads like a status report instead of a decision brief
- If any data is >24h stale without saying so
- If Mark needs to ask a follow-up to understand any item
- If it exceeds 500 words
```

### Sub-Agent Task

```
GOAL: Build Python CLI tool that passes `clawdsure check --asset-type file`
      with zero errors on first run against live workspace.

CONSTRAINTS:
- Python 3.14 compatible
- No external dependencies beyond stdlib
- All file operations use atomic writes
- Hash chain uses SHA256, canonical JSON serialization
- Must handle missing files gracefully (alert, don't crash)

FORMAT:
- Single file: clawdsure/cli.py
- Docstring at top with usage
- Exit codes: 0 (no drift), 1 (error), 2 (drift detected)

FAILURE:
- If it imports anything not in stdlib
- If hash chain breaks on verification
- If it crashes on missing file instead of alerting
- If it passes tests but fails on live workspace
```

### Deal Sheet / Document

```
GOAL: One-page deal sheet Sam Clifton scans in 2 minutes
      and knows whether to take the next meeting.

CONSTRAINTS:
- <2000 words
- GBP for premiums, USD for market size
- No jargon without parenthetical explanation
- Every number sourced or flagged as estimate

FORMAT:
[See DEAL-SHEET.md structure: opportunity, product, financials,
 capacity, regulatory, competitive, timeline, ask]

FAILURE:
- If an underwriter needs to Google a term
- If loss ratio projections are missing
- If it reads like a pitch deck instead of a deal memo
- If the capacity ask is vague ("$5-50M" is vague; "$5M Year 1" is specific)
```

### Security Audit

```
GOAL: Line-by-line security audit that identifies every external
      network call, crypto operation, and file write in the codebase.

CONSTRAINTS:
- Review actual source code, not documentation claims
- Flag eval(), exec(), dynamic imports
- Identify all environment variables read
- Note all URLs/endpoints contacted

FORMAT:
Per-component sections:
- What It Does (2 sentences)
- External Network Calls (list with URLs)
- Crypto Operations (list with algorithms)
- File Read/Write (list with paths)
- Permissions Required (list)
- Data Collected/Sent (list)
- VirusTotal Flag Explanation
- Security Risks (numbered)
- Recommendation (SAFE / SAFE WITH CONDITIONS / REJECT)

FAILURE:
- If "no network calls" but code contains fetch/curl/http
- If recommendation is given without reviewing actual source
- If risks are listed without mitigation suggestions
```

---

## When to Use Prompt Contracts

**Always.** Every prompt I write — cron job payloads, sub-agent tasks, document generation, code specs, even search queries — gets the four components. Some are one-liners, some are full specs. Scale to complexity, but never skip.

**Minimum viable contract:**
```
GOAL: [one line]
FAILURE: [one line — what makes this worthless]
```

Even two lines is better than zero structure.

## Voice Override

Structure is internal scaffolding. Output still sounds like Clawdine. Contracts improve the thinking, not flatten the voice. If the output could've been written by any assistant, add this failure condition:

```
FAILURE: If it doesn't sound like a gremlin with opinions wrote it.
```

Bullet points are fine. Personality-free bullet points aren't.

---

## Why This Works

1. **Forces clarity before execution.** If you can't write the goal, you don't understand the task.
2. **Eliminates ambiguity.** The model can't misinterpret "Score 8+ on Flesch-Kincaid."
3. **Makes verification binary.** Did it meet the contract or didn't it?
4. **Prevents scope creep.** Constraints are walls, not suggestions.
5. **Catches bad output early.** Failure conditions are the rejection criteria you'd apply anyway — just written down in advance.

---

*Every prompt is a contract. Think legal contract, not creative brief.*
