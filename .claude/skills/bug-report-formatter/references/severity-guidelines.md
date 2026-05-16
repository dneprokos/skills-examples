# Severity and Priority Guidelines

## Severity

Severity describes the **technical impact** of the bug — how badly it breaks the system.

| Severity | Definition | Examples |
|----------|------------|---------|
| **Blocker** | System is down, data loss occurs, or a critical path is completely unusable with no workaround | App crashes on launch; payment API returns 500 on every request; user data deleted unexpectedly |
| **Critical** | Core feature is broken with no practical workaround; affects many users or a high-risk area | Login fails for all users; checkout never completes; data saved incorrectly |
| **Major** | Important feature is broken but a workaround exists, or a partial degradation with limited user impact | Export to PDF fails but copy-paste works; filter returns wrong results on one edge case |
| **Minor** | Non-critical feature behaves incorrectly; cosmetic issues with functional consequence; affects few users | Tooltip shows wrong text; date picker allows invalid past dates; success toast not shown |
| **Trivial** | Cosmetic only — layout, spelling, alignment, color; no functional impact | Button text has a typo; icon slightly misaligned in IE; hover state missing on disabled element |

### Severity decision questions

1. Does the bug prevent completing a core business flow? → **Blocker** or **Critical**
2. Does it cause data loss or corruption? → **Blocker**
3. Is there a usable workaround? → Drop one level (Critical → Major, Major → Minor)
4. Does it affect only a visual/cosmetic element? → **Trivial**
5. Does it affect only a subset of users or an uncommon path? → **Minor** or **Major** depending on the flow's importance

---

## Priority

Priority describes **when** the bug should be fixed — a business and scheduling decision.

| Priority | Definition |
|----------|------------|
| **High** | Fix in the current sprint or release; blocking QA sign-off or release readiness |
| **Medium** | Fix in the next sprint; important but does not block the release |
| **Low** | Fix when capacity allows; cosmetic, rare, or low-impact |

### Severity → Priority defaults

Use these as a starting point; the team or product owner can override based on business context.

| Severity | Default Priority |
|----------|-----------------|
| Blocker  | High |
| Critical | High |
| Major    | Medium |
| Minor    | Low |
| Trivial  | Low |

### Override signals

- A **Minor** bug on a high-traffic screen (e.g. homepage hero) may be elevated to Medium.
- A **Critical** bug in a rarely used admin panel may be downgraded to Medium if no users are blocked.
- A **Blocker** on a feature that is not yet live may be Medium until the release date approaches.
