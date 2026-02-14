# Roundy — Product Document for Founders

## What Roundy Does

Roundy watches every investor conversation you have and tells you the one thing you should do today to close your round faster.

You upload transcripts, paste emails, or log quick notes. Roundy extracts the important stuff — who said what, what objections came up, what the next step is, whether this investor is actually moving forward or politely stalling.

Then each morning, you open Roundy and it says: "Emma Wilson asked for your data room two days ago. You haven't sent it. She's responded to every previous message within 24 hours. Send it now."

Not "follow up with your investors." The specific thing. With the specific reason. Backed by the specific evidence.

---

## Your Daily Workflow

### Morning: Open the Today page

The Today page is your war room. It shows you three things:

**1. The Move**
One recommendation. The highest-leverage action you can take right now. It tells you:
- What to do ("Send the financial model to David Moore")
- Why it matters ("He verbally committed $200K but hasn't seen your numbers. He's a fast mover — average response time 6 hours. Silence beyond 48 hours is unusual for him.")
- Evidence cards you can click to see the exact interactions that support this recommendation

**2. Today's Briefing**
A categorized view of your pipeline:
- Hot deals: investors who showed positive signals recently
- Stalled deals: conversations that went quiet (with how many days and why)
- New activity: anything that came in since yesterday
- For each item: a one-line summary, the context, and suggested actions you can take with one click (draft email, schedule call)

**3. Upcoming Meetings**
Your next three investor meetings with a "Prep" button on each one. Click it and Roundy generates a full briefing — the investor's background, what they care about, what landed in previous conversations with them, objections to prepare for, and suggested talking points.

### During the Day: Log interactions as they happen

After a call or meeting, you drop the transcript into Roundy. If you use Granola for meeting notes, it syncs directly.

Roundy processes it in about 30 seconds and extracts:
- Who was in the meeting
- What the investor's sentiment was (leaning in, neutral, blocking)
- Specific commitment signals ("I'll talk to my partners")
- Specific objections raised ("Your burn rate concerns me")
- Action items for you and for them
- A prediction: is this investor likely to invest, unclear, or unlikely?

This becomes a record in your pipeline. The deal card updates. Your pitch score adjusts. Tomorrow's recommendations account for everything that happened today.

You can also paste email threads or type quick notes. Same extraction, same intelligence.

### Between Meetings: Use the Chat

Roundy has a conversational AI that knows your entire pipeline. You can ask it anything:

- "What did Andrea say about our valuation?"
- "Which investors haven't responded in over a week?"
- "Draft a follow-up email to George — reference our last call about the enterprise pilot"
- "What's the biggest risk in my pipeline right now?"
- "Prep me for my call with Blake tomorrow"

It pulls answers from your actual interactions, not generic advice. Every claim it makes links to a specific conversation on a specific date.

---

## Pipeline Management

### The Board

Your pipeline is a drag-and-drop Kanban board with seven stages:

**Sourced** → **Qualified** → **Pitching** → **In DD** → **Committed** → **Closed** → **Passed**

Each deal card shows the investor name, their firm, check size range, days since last contact, and a health indicator.

Drag a deal between columns to update its stage. Roundy records the change and factors it into future recommendations.

At the top: your round metrics. Target amount, amount raised, percentage complete, days until your target close date.

### AI-Suggested Stage Changes

Roundy proposes stage changes when the evidence supports it. For example:

> "Move David Moore from Pitching to In DD. Rationale: He requested your data room on Feb 3, asked detailed questions about unit economics on Feb 5, and scheduled a follow-up with his partner. Confidence: High."

You approve or dismiss. Roundy never moves a deal without your say-so.

### Deal Detail Panel

Click any deal card to open the side panel. You'll see:
- Full interaction history (every email, call, meeting, note)
- Stage change timeline
- Upcoming meetings with this investor
- Pending tasks related to this deal
- Investor details (firm, check size, investment preferences)
- Health metrics (conviction score, response latency, stall risk)

---

## Pitch Intelligence

### How It Works

After every pitch meeting, upload the transcript. Roundy scores your pitch on a 0-100 scale across four dimensions:

- **Clarity**: Did the investor understand what you're building?
- **Structure**: Did your narrative resolve into something investable?
- **Delivery**: Did you convey credibility and control?
- **Overall**: Weighted blend based on engagement signals

### What Landed / What Missed

For each pitch, you get a list of what worked (with evidence quotes from the transcript) and what didn't (with specific suggestions for how to fix it).

After three or more pitches, Roundy detects patterns. It tells you: "Technical depth has landed in 4 out of 5 meetings. Your explanation of unit economics has missed in 3 out of 5 meetings. Here's what the investors actually said."

### Objections

Roundy clusters similar objections across all your pitches. If five different investors raised concerns about your burn rate, you'll see: "Burn rate — raised 5 times" with a list of who said it and links to the transcripts.

From there, you can generate a FAQ entry — a prepared response for next time — so you stop getting caught off guard by the same question.

### Investor Lens

For your next three upcoming meetings, the Analysis page shows investor-specific prep:

- Their priorities (based on their firm type and previous interactions)
- Suggested pitch angle for this specific investor
- Objections to prepare for (based on what this investor or similar investors have raised)
- History badge (if you've pitched them before)

---

## Contact & Company Management

### Investors

Every investor is a record with:
- Name, email, phone, LinkedIn
- Company (fund/firm) with investment preferences
- Check size range
- Stage preferences
- Sector focus
- All interaction history
- Conviction score and behavioral metrics

### Companies

Investor firms are tracked separately:
- Fund name and type (VC, angel, family office, corporate)
- Investment thesis
- Team members (linked to individual contacts)
- Portfolio companies
- All deals with your company

### Automatic Resolution

When you upload a transcript that mentions "Jane from Sequoia," Roundy automatically matches that to Jane Doe at Sequoia Capital in your contacts. If it's a new person, it creates the record and asks you to confirm.

### Bulk Import

You can import your existing investor spreadsheet as a CSV. Map columns to fields (name, email, stage, check size, notes) and Roundy creates the contacts, companies, and deals.

---

## Meeting Prep & Email Drafting

### Meeting Prep Briefings

Before any investor call, click "Prep" to generate a briefing that includes:

- **Investor background**: Who they are, what they invest in, recent activity
- **Previous interactions**: Summary of everything you've discussed before
- **What landed**: Pitch points that resonated with this investor specifically
- **Objections to expect**: Based on their previous questions and their investor type
- **Talking points**: Suggestions for this specific meeting
- **Questions to ask**: Based on where you are in the deal process

Briefings can use web research to pull in recent news about the investor's firm, new portfolio investments, and thesis changes.

### Email Drafting

From any deal or the Today briefing, click "Draft Email" and Roundy generates a context-aware email:

- Follow-up after a meeting (references specific discussion points)
- First outreach (personalized based on investor profile)
- Document sharing (sends materials with relevant context)

You edit it before sending. Roundy drafts; you decide.

---

## Memory & Knowledge

### How Roundy Remembers

Every interaction goes into two systems:

1. **Vault** (always on): A vector database that enables semantic search. When you ask "What did George say about pricing?", Roundy finds the exact paragraph from the exact transcript.

2. **Hindsight** (optional): A pattern memory system that tracks higher-level trends. Not "what did George say" but "investors who ask about pricing in the first meeting are 3x more likely to pass."

Together, these mean Roundy gets smarter the more you use it. After 20 interactions, it knows your pipeline better than you do.

### Context Graph

Behind the scenes, Roundy builds a structured knowledge graph from your interactions:

- "Blake Rhodes is a partner at Sequoia"
- "Blake is concerned about unit economics"
- "Andrea committed $100K on February 3"
- "George requested the data room"

These facts are extracted automatically from transcripts and emails, linked to specific evidence, and used to power recommendations. You don't build this manually — it builds itself from your conversations.

---

## Team Collaboration

### Workspaces

Roundy is multi-user. Your fundraising workspace can include:
- Co-founders
- CFO or head of finance
- Advisors with limited access

### Roles

- **Owner**: Full access, billing, workspace settings
- **Admin**: Manage team, view all data
- **Member**: Read/write pipeline data, use AI features

### Invitations

Invite team members by email. They get a link, create an account (or use existing), and join your workspace immediately. All data is shared within the workspace — everyone sees the same pipeline, the same interactions, the same recommendations.

---

## Integrations

### Granola

Connect your Granola account to auto-import meeting transcripts. After each meeting, the transcript appears in your inbox ready for processing. One click to extract insights.

### Email (Coming)

Gmail and Outlook integration for automatic email capture. Every investor email becomes a logged interaction without manual entry.

### Calendar (Coming)

Google Calendar and Outlook Calendar sync for automatic meeting detection. Before your meeting: a prep briefing. After your meeting: a prompt to upload the transcript.

---

## Pricing

| | Pro | Team |
|---|---|---|
| **Price** | $119/month | $249/month + $59/seat |
| Pipeline tracking | Yes | Yes |
| AI recommendations | Yes | Yes |
| Pitch analysis | Yes | Yes |
| Meeting prep | Yes | Yes |
| Chat assistant | Yes | Yes |
| Adversarial validation | Yes | Yes |
| Team members | 1 | 3 included, $59/additional |
| Rounds | Unlimited | Unlimited |
| Shared pipeline | — | Yes |
| Role-based access | — | Yes |

14-day free trial on Pro. No credit card required to start.

Save 17% with annual billing ($99/month Pro, $209/month Team).

---

## Getting Started

1. **Sign up** at roundy.ai
2. **Create your workspace** — name it, add your company
3. **Set up your round** — target amount, instrument, close date
4. **Import investors** — CSV upload or add manually
5. **Log your first interaction** — paste a transcript, email thread, or quick note
6. **Open Today** — your first recommendation appears

From there, Roundy learns from every interaction. The more you use it, the better it gets at telling you what matters and what to do about it.

---

## What Founders Say

*"I was managing 50 conversations in a spreadsheet and constantly missing follow-ups. After two weeks on Roundy, I realized three of my 'hot leads' were actually stalling and one investor I'd written off was the most responsive person in my pipeline."*

*"The pitch scoring changed how I prepare. I kept getting dinged on unit economics across five different meetings. Once I saw the pattern, I rebuilt that section of my deck and my scores went up 15 points."*

*"The daily recommendation is worth the entire subscription. I used to spend 30 minutes each morning figuring out who to contact. Now I open Roundy and it tells me."*
