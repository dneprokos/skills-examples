# Bug Description Template

Use this template when editing the description of a Bug issue. Fill each section from user input; omit sections the user did not provide (do not leave them blank in the submitted description).

```markdown
**Version:** {version or "N/A"}

**Initial Condition:** {preconditions / environment state before reproducing}

**Steps to Reproduce:**
{numbered steps}

**Expected Results:** {what should happen}

**Actual Results:** {what actually happened}

**Affected Tests:** {test names, suites, or "N/A"}
```

## Rules

- Use `contentFormat: "markdown"` when passing this to `editJiraIssue`.
- If the user only provides some fields, include only those fields — do not include empty headings.
- Show the formatted description in the confirmation block before calling `editJiraIssue`.
- `Version` and `Affected Tests` are optional; include them only if the user provides values.
