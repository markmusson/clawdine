# VULN-188: Default Admin Scope Granted on WebSocket Connect

## 1. Title
Default Admin Scope Granted on WebSocket Connect

## 2. Severity Assessment
**High** - Authentication bypass leading to privilege escalation

## 3. Impact
Unauthenticated or low-privilege clients connecting without explicit scope requests are automatically granted `operator.admin` privileges, enabling full administrative access to the gateway without authorization.

## 4. Affected Component
- **File:** `src/gateway/server/ws-connection/message-handler.ts`
- **Lines:** 360-366
- **Component:** WebSocket connection handler
- **Versions:** Current HEAD (as of 2026-02-10)

## 5. Technical Reproduction

**Steps:**
1. Connect to OpenClaw gateway WebSocket endpoint as `operator` role
2. Omit `scopes` parameter in connection handshake (or send empty array)
3. Observe granted scopes in connection response

**Code Location:**
```typescript
// src/gateway/server/ws-connection/message-handler.ts:360-366
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

## 6. Demonstrated Impact
A client connecting as `operator` without requesting scopes receives `operator.admin` by default, granting:
- Full gateway configuration access
- Ability to manipulate sessions
- Administrative control over all gateway functions
- Bypasses intended least-privilege design

## 7. Environment
- **OpenClaw Version:** HEAD (commit from 2026-02-10)
- **Repository:** github.com/openclaw/openclaw
- **Platform:** All platforms running OpenClaw gateway
- **Node.js:** 22.12.0+

## 8. Remediation Advice

### Recommended Fix
Default to **least-privilege** (no scopes) and require explicit scope authorization:

```typescript
const requestedScopes = Array.isArray(connectParams.scopes) ? connectParams.scopes : [];
const scopes = requestedScopes; // default to none

// Reject connections without explicit scopes for operator role
if (role === "operator" && scopes.length === 0) {
  send({ 
    type: "res", 
    id: frame.id, 
    ok: false, 
    error: errorShape(ErrorCodes.INVALID_REQUEST, "scopes required") 
  });
  close(1008, "scopes required");
  return;
}
```

### Alternative Approach
If backward compatibility is required:
1. Default to minimal read-only scope
2. Require explicit opt-in for admin privileges
3. Add scope validation against authorized scope list per client

### Testing
Add test cases ensuring:
- Connections without scopes are rejected or granted minimal privileges
- Admin scopes require explicit authorization
- Scope escalation attempts are logged and blocked

---

**CWE:** CWE-269 (Improper Privilege Management)  
**OWASP:** A01:2021 – Broken Access Control  
**Reporter:** Clawdine (ClawdSure security audit)  
**Date:** 2026-02-10
