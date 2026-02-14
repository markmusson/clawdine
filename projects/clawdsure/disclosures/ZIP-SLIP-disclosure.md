# Archive Extraction Path Traversal (Zip Slip)

## 1. Title
Archive Extraction Allows Path Traversal (Zip Slip) in Skill Installation

## 2. Severity Assessment
**High** - Arbitrary file write leading to code execution

## 3. Impact
Skill archive extraction using system `unzip` and `tar` commands does not validate entry paths, allowing an attacker to write files outside the intended extraction directory. A malicious skill archive can overwrite critical system files (e.g., `~/.bashrc`, `~/.ssh/authorized_keys`, startup scripts) leading to persistent code execution.

## 4. Affected Component
- **File:** `src/agents/skills-install.ts`
- **Lines:** 255-278
- **Component:** Skill archive extraction
- **Versions:** Current HEAD (as of 2026-02-10)

## 5. Technical Reproduction

**Steps:**
1. Create malicious skill archive with path traversal entries:
```bash
# Create malicious skill
mkdir malicious-skill
echo '#!/bin/bash' > malicious-skill/payload.sh
echo 'echo "PWNED" > /tmp/pwned.txt' >> malicious-skill/payload.sh

# Create archive with traversal path
cd malicious-skill
tar czf ../malicious-skill.tar.gz --transform 's,payload.sh,../../.bashrc,' payload.sh
```

2. Install skill: `openclaw skills install malicious-skill.tar.gz`
3. Observe file written outside skills directory (e.g., `~/.bashrc` overwritten)

**Code Location:**
```typescript
// src/agents/skills-install.ts:255-278
if (archiveType === "zip") {
  const argv = ["unzip", "-q", archivePath, "-d", targetDir];
  return await runCommandWithTimeout(argv, { timeoutMs });
}
// ...
const argv = ["tar", "xf", archivePath, "-C", targetDir];
```

**Malicious Archive Entry Examples:**
- `../../.bashrc` (shell startup hijack)
- `../../.ssh/authorized_keys` (SSH backdoor)
- `../../../../usr/local/bin/openclaw` (binary replacement)
- `../../Library/LaunchAgents/evil.plist` (macOS persistence)

## 6. Demonstrated Impact
- **Arbitrary File Write:** Overwrite any file writable by gateway user
- **Code Execution:** Modify shell profiles, cron jobs, startup scripts
- **Persistence:** Install backdoors that survive restarts
- **Privilege Escalation:** Overwrite setuid binaries or configuration files
- **Data Exfiltration:** Replace legitimate scripts with wrappers that log/exfiltrate

## 7. Environment
- **OpenClaw Version:** HEAD (commit from 2026-02-10)
- **Repository:** github.com/openclaw/openclaw
- **Platform:** All platforms (macOS, Linux, Windows with WSL)
- **Node.js:** 22.12.0+
- **Attack Vector:** Skill installation from untrusted sources

## 8. Remediation Advice

### Recommended Fix
Replace shell command execution with safe extraction libraries that validate paths:

**For TAR archives:**
```typescript
import * as tar from "tar";
import path from "node:path";

await tar.x({
  file: archivePath,
  cwd: targetDir,
  strict: true,
  onentry: (entry) => {
    const outPath = path.resolve(targetDir, entry.path);
    const safeBase = path.resolve(targetDir) + path.sep;
    
    if (!outPath.startsWith(safeBase)) {
      throw new Error(
        `Archive entry escapes targetDir: ${entry.path} -> ${outPath}`
      );
    }
  },
});
```

**For ZIP archives:**
```typescript
import { Extract } from "unzipper";
import path from "node:path";
import { createReadStream } from "fs";

const safeBase = path.resolve(targetDir) + path.sep;

await createReadStream(archivePath)
  .pipe(Extract({
    path: targetDir,
    concurrency: 1,
  }))
  .on('entry', (entry) => {
    const outPath = path.resolve(targetDir, entry.path);
    if (!outPath.startsWith(safeBase)) {
      throw new Error(`Path traversal attempt: ${entry.path}`);
    }
  })
  .promise();
```

### Additional Safeguards
1. **Symlink Protection:** Check for symlinks that point outside targetDir
2. **Allowlisting:** Only accept skills from verified sources (ClawHub)
3. **Sandboxing:** Extract archives in isolated container with no write access to parent dirs
4. **Integrity Checks:** Verify archive signatures before extraction
5. **User Warnings:** Alert users when installing from untrusted sources

### Testing
Add test cases ensuring:
- Archives with `../` paths are rejected
- Absolute paths are rejected
- Symlinks to parent directories are rejected
- Legitimate archives extract correctly

### Migration Path
1. Add safe extraction as default
2. Keep unsafe extraction behind `--unsafe-extraction` flag (with loud warnings)
3. Deprecate unsafe mode after one release cycle

---

**CWE:** CWE-22 (Improper Limitation of a Pathname to a Restricted Directory)  
**OWASP:** A01:2021 – Broken Access Control  
**Related CVE:** CVE-2018-1000544 (Zip Slip in Ruby gem_install)  
**Snyk Advisory:** https://security.snyk.io/research/zip-slip-vulnerability  
**Reporter:** Clawdine (ClawdSure security audit)  
**Date:** 2026-02-10
