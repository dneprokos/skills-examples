# Bug Report Template

Use this structure every time. Keep each section present even if empty — use the explicit empty-state markers shown below.

---

## Title

**Pattern:** `[Area] Short description of what breaks and under what condition`

**Good:** `[Checkout] Order total shows $0.00 after applying a discount code on mobile Safari`
**Bad:** `Bug in checkout`, `It doesn't work`

Rules:
- Imperative or noun phrase, no trailing period
- Include the affected area in square brackets
- Under 80 characters

---

## Environment

```
OS:              [e.g. Windows 11 22H2 / macOS 14.4 / Ubuntu 22.04]
Browser / Client:[e.g. Chrome 124 / Safari 17 / iOS App 3.2.1]
App / API version:[e.g. v2.1.4 / commit abc1234 / Unknown]
Test environment:[e.g. Staging / Production / Local]
```

If a value cannot be inferred from the input, write `Unknown`. Never omit the block.

---

## Steps to Reproduce

Numbered list. Each step is one action.

1. Navigate to …
2. Click / enter / select …
3. Observe …

If the user's input is too vague to reconstruct steps, mark the section:
`⚠️ Insufficient information — ask the reporter to provide exact steps.`

---

## Expected Result

One or two sentences describing what should happen when the steps above are followed correctly.

---

## Actual Result

One or two sentences describing what actually happens. Include any visible error messages verbatim.

---

## Severity / Priority

```
Severity: [Blocker | Critical | Major | Minor | Trivial]
Priority: [High | Medium | Low]
```

See `severity-guidelines.md` for the decision matrix.

---

## Logs / Attachments

Paste stack traces, console errors, or API responses in fenced code blocks. Preserve them verbatim — do not truncate or paraphrase.

```
[paste logs here, or write: No logs provided.]
```

---

## Additional Context

Any extra information: related issues, frequency (always / intermittent), workaround found, regression (worked in which version), links to screen recordings.

If nothing to add: `None.`
