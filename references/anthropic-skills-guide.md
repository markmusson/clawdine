# The Complete Guide to Building Skills for Claude
## Source: Anthropic (resources.anthropic.com)
## Saved: 2026-02-09

---

## Key Takeaways for ClawdSure Skill Build

### Structure
```
clawdsure/
├── SKILL.md              # Required - main skill file
├── scripts/              # Executable code (bash scripts)
│   ├── attest.sh
│   ├── verify.sh
│   ├── enroll.sh
│   ├── fingerprint.sh
│   ├── publish.sh
│   ├── audit-machine.sh
│   └── portable.sh
├── references/           # Documentation loaded as needed
│   ├── attestation-schema.md
│   ├── chain-rules.md
│   ├── threat-model.md
│   ├── underwriting.md
│   ├── machine-audit.md
│   └── relay-api.md
└── assets/               # Templates, etc.
```

### YAML Frontmatter Rules
- `name`: kebab-case, no spaces/capitals, must match folder name
- `description`: MUST include WHAT it does + WHEN to use it + trigger phrases. Under 1024 chars. No XML tags.
- No README.md inside skill folder
- File must be exactly `SKILL.md` (case-sensitive)

### Progressive Disclosure (3 levels)
1. **YAML frontmatter** — always loaded in system prompt (skill detection)
2. **SKILL.md body** — loaded when skill is relevant
3. **Linked files** (references/) — loaded only as needed

### Core Principles
- **Composability**: Work alongside other skills
- **Portability**: Works across Claude.ai, Claude Code, API
- **Progressive Disclosure**: Minimize token usage

### Skill Categories
1. **Document & Asset Creation** — consistent output, templates, quality checklists
2. **Workflow Automation** — multi-step processes, validation gates, iterative refinement
3. **MCP Enhancement** — workflow guidance on top of tool access

### Patterns
1. **Sequential Workflow Orchestration** — explicit step ordering, dependencies, rollback
2. **Multi-MCP Coordination** — phase separation, data passing between services
3. **Iterative Refinement** — quality checks, refinement loops, validation scripts
4. **Context-aware Tool Selection** — decision trees, fallbacks
5. **Domain-specific Intelligence** — embedded expertise, compliance before action, audit trails

### Testing
- Triggering tests (does it load when it should?)
- Functional tests (correct outputs?)
- Performance comparison (vs baseline)

### Distribution
- Host on GitHub with clear README (repo-level, NOT inside skill folder)
- Zip folder for Claude.ai upload
- Can deploy org-wide via admin

### Best Practices
- Keep SKILL.md under 5,000 words
- Move detailed docs to references/
- Use scripts for critical validations (code > language instructions)
- Include error handling and examples
- Be specific in descriptions — include trigger phrases users would say

---

## Full Guide Text

(See /tmp/anthropic-skills-guide.pdf for original)

### Chapter 1: Fundamentals

A skill is a folder containing:
- SKILL.md (required): Instructions in Markdown with YAML frontmatter
- scripts/ (optional): Executable code
- references/ (optional): Documentation loaded as needed
- assets/ (optional): Templates, fonts, icons

### Chapter 2: Planning and Design

Start with 2-3 concrete use cases. Define success criteria (triggering rate, tool calls, error rate).

### Chapter 3: Testing and Iteration

Three levels: manual testing in Claude.ai, scripted testing in Claude Code, programmatic testing via API.

Pro tip: Iterate on a single task until it works, then extract into skill.

### Chapter 4: Distribution and Sharing

Skills are an open standard. Published as Agent Skills spec. Works across platforms.

### Chapter 5: Patterns and Troubleshooting

See patterns above. Common issues:
- Skill won't upload → check SKILL.md naming, YAML formatting
- Skill doesn't trigger → improve description field
- Skill triggers too often → add negative triggers, be more specific
- MCP connection issues → verify server, auth, tool names
- Instructions not followed → keep concise, put critical stuff first, use scripts for validation

### Reference A: Quick Checklist

Before start: use cases identified, tools identified, structure planned
During dev: kebab-case folder, SKILL.md exists, frontmatter correct, description has WHAT+WHEN
Before upload: trigger tests, functional tests, tool integration works
After upload: test in conversations, monitor triggering, iterate

### Reference B: YAML Frontmatter

Required: name, description
Optional: license, allowed-tools, metadata (author, version, mcp-server, category, tags)
Forbidden: XML brackets, "claude"/"anthropic" in name

### Reference C: Example Skills

- anthropics/skills on GitHub
- Document skills (PDF, DOCX, PPTX, XLSX)
- Partner skills (Asana, Atlassian, Canva, Figma, Sentry, Zapier)
