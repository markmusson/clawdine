# OpenClaw Security Audit Report

**Scope:** /tmp/openclaw (≈606k LOC, TS/JS)

**Confirmed by requester:**
- VULN-188: Default admin scopes in `src/gateway/server/ws-connection/message-handler.ts` (lines 360–366)
- VULN-210: Missing `--ignore-scripts` in `src/plugins/install.ts` (line ~281)

The findings below focus on *real, exploitable* issues with concrete impact. Each entry includes code, severity, exploit scenario, and a recommended fix.

---

## Findings

### 1) **Default Admin Scope Granted on WebSocket Connect** (VULN-188)
- **Category:** Authentication & Authorization
- **File/Lines:** `src/gateway/server/ws-connection/message-handler.ts` **360–366**
- **CWE:** CWE-269 (Improper Privilege Management)
- **OWASP:** A01:2021 – Broken Access Control
- **Severity:** **High**

**Description:**
When a client connects without requesting explicit scopes, the server defaults to `operator.admin` for the `operator` role. This grants full administrative privileges even when the client did not request or prove entitlement.

**Code Snippet:**
```ts
const requestedScopes = Array.isArray(connectParams.scopes) ? connectParams.scopes : [];
const scopes =
  requestedScopes.length > 0
    ? requestedScopes
    : role === "operator"
      ? ["operator.admin"]
      : [];
connectParams.role = role;
connectParams.scopes = scopes;
```

**Exploit Scenario:**
A client connects as `operator` and omits `scopes` entirely. The connection is implicitly granted `operator.admin`, enabling privileged actions without explicitly requesting or being authorized for them.

**Recommended Fix (example):**
Default to **least-privilege** (no admin) and require explicit admin scope grant.
```ts
const requestedScopes = Array.isArray(connectParams.scopes) ? connectParams.scopes : [];
const scopes = requestedScopes; // default to none

// Optionally: validate requestedScopes against allowed scopes for that client
// and reject if none provided
if (role === "operator" && scopes.length === 0) {
  send({ type: "res", id: frame.id, ok: false, error: errorShape(ErrorCodes.INVALID_REQUEST, "scopes required") });
  close(1008, "scopes required");
  return;
}
```

---

### 2) **NPM Install Executes Untrusted Lifecycle Scripts** (VULN-210)
- **Category:** Supply Chain Security / Process Execution
- **File/Lines:** `src/plugins/install.ts` **277–284**
- **CWE:** CWE-829 (Inclusion of Functionality from Untrusted Control Sphere)
- **OWASP:** A08:2021 – Software and Data Integrity Failures
- **Severity:** **High**

**Description:**
Plugin installs run `npm install` without `--ignore-scripts`, allowing **arbitrary command execution** via `preinstall/postinstall` scripts in dependencies.

**Code Snippet:**
```ts
const npmRes = await runCommandWithTimeout(["npm", "install", "--omit=dev", "--silent"], {
  timeoutMs: Math.max(timeoutMs, 300_000),
  cwd: targetDir,
});
```

**Exploit Scenario:**
A malicious dependency in a plugin’s dependency tree includes a `postinstall` script (e.g., `curl | bash`) that executes during installation, resulting in remote code execution on the host running the gateway.

**Recommended Fix (example):**
Disable lifecycle scripts by default, and optionally allow an explicit override.
```ts
const npmRes = await runCommandWithTimeout(
  ["npm", "install", "--omit=dev", "--silent", "--ignore-scripts"],
  { timeoutMs: Math.max(timeoutMs, 300_000), cwd: targetDir },
);
```

---

### 3) **Archive Extraction Allows Path Traversal (Zip Slip)**
- **Category:** Path Traversal
- **File/Lines:** `src/agents/skills-install.ts` **255–278**
- **CWE:** CWE-22 (Improper Limitation of a Pathname to a Restricted Directory)
- **OWASP:** A01:2021 – Broken Access Control
- **Severity:** **High**

**Description:**
Skill downloads are extracted using system `unzip`/`tar` without validating archive entry paths. A crafted archive can write files **outside** the intended `targetDir` (e.g., `../../.ssh/authorized_keys`).

**Code Snippet:**
```ts
if (archiveType === "zip") {
  const argv = ["unzip", "-q", archivePath, "-d", targetDir];
  return await runCommandWithTimeout(argv, { timeoutMs });
}
...
const argv = ["tar", "xf", archivePath, "-C", targetDir];
```

**Exploit Scenario:**
An attacker publishes a malicious skill archive with entries like `../../.bashrc` or `../../.ssh/authorized_keys`. When installed, the extraction overwrites files outside the skills directory, leading to persistence or code execution.

**Recommended Fix (example):**
Use a safe extractor that validates each entry path before writing. Example using `tar`’s `onentry` with path checks:
```ts
import * as tar from "tar";
import path from "node:path";

await tar.x({
  file: archivePath,
  cwd: targetDir,
  onentry: (entry) => {
    const outPath = path.resolve(targetDir, entry.path);
    if (!outPath.startsWith(path.resolve(targetDir) + path.sep)) {
      throw new Error(`Archive entry escapes targetDir: ${entry.path}`);
    }
  },
});
```
For zip files, switch to a library that iterates entries and validates paths (e.g., `yauzl`/`unzipper`) instead of shelling out to `unzip`.

---

### 4) **SSRF to Internal Network via URL-Based Inputs**
- **Category:** Network Security / API Security
- **Files/Lines:**
  - `src/gateway/openresponses-http.ts` **102–118** (URLs enabled by default)
  - `src/media/input-files.ts` **139–150** (fetch with no private-network restriction)
  - `src/infra/net/fetch-guard.ts` **101–125** (no private IP blocking unless policy provided)
- **CWE:** CWE-918 (Server-Side Request Forgery)
- **OWASP:** A10:2021 – SSRF
- **Severity:** **Medium** (High if gateway is internet-exposed)

**Description:**
OpenResponses input allows `url` sources by default (`allowUrl: true`). The fetch guard pins DNS to prevent rebinding but **does not block private network or localhost addresses** unless a policy is explicitly provided. This enables SSRF to internal services (e.g., `http://127.0.0.1:...`, cloud metadata endpoints).

**Code Snippets:**
```ts
// openresponses-http.ts
files: { allowUrl: files?.allowUrl ?? true, ... }
images: { allowUrl: images?.allowUrl ?? true, ... }
```
```ts
// input-files.ts
const { response } = await fetchWithSsrFGuard({
  url: params.url,
  maxRedirects: params.maxRedirects,
  timeoutMs: params.timeoutMs,
  init: { headers: { "User-Agent": "OpenClaw-Gateway/1.0" } },
});
```
```ts
// fetch-guard.ts (no private network block unless policy provided)
const pinned = usePolicy
  ? await resolvePinnedHostnameWithPolicy(...)
  : await resolvePinnedHostname(parsedUrl.hostname, params.lookupFn);
```

**Exploit Scenario:**
An authenticated attacker submits a request containing `input_image` or file `url` pointing to `http://169.254.169.254/latest/meta-data/` or `http://127.0.0.1:...` and receives sensitive internal data in the response.

**Recommended Fix (example):**
1) Default to **deny** URL fetches unless explicitly enabled.
2) Enforce SSRF policy that blocks private networks by default.
```ts
// openresponses-http.ts
files: { allowUrl: files?.allowUrl ?? false, ... }
images: { allowUrl: images?.allowUrl ?? false, ... }
```
```ts
// input-files.ts
const { response, release } = await fetchWithSsrFGuard({
  url: params.url,
  maxRedirects: params.maxRedirects,
  timeoutMs: params.timeoutMs,
  policy: { allowPrivateNetwork: false },
  init: { headers: { "User-Agent": "OpenClaw-Gateway/1.0" } },
});
```
If private URLs are required for specific deployments, require explicit allowlists (`allowedHostnames`).

---

## Coverage Notes by Category
- **Authentication & Authorization:** ✅ VULN-188 (default admin scopes)
- **Command Injection:** No direct shell-injection found in request paths (commands use argv arrays). Vulnerability addressed in VULN-210 (lifecycle scripts).
- **Path Traversal:** ✅ Zip slip in skill archive extraction
- **Supply Chain Security:** ✅ VULN-210 (npm scripts)
- **Credential Storage:** No unsafe permissions found; sensitive stores use 0o600/0o700 in multiple locations.
- **Input Validation:** URL handling needs tighter SSRF policy (Finding #4)
- **File Permission Issues:** No critical issues observed (permissions generally locked down).
- **Network Security:** ✅ SSRF risk via URL-based inputs
- **Process Execution:** ✅ npm lifecycle scripts; other exec uses spawn with argv arrays
- **API Security:** ✅ SSRF defaults; otherwise endpoints generally enforce auth

---

## Summary
Key risks center on **authorization defaults**, **supply chain execution**, **archive path traversal**, and **SSRF**. Addressing the above four findings materially improves the gateway’s security posture.
