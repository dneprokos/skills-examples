# Bug Report Formatter

A Copilot skill for turning messy bug descriptions, error logs, and stack traces into structured, Jira-ready bug reports.

## What it does

- accepts raw input in any form: stack traces, error logs, casual descriptions, or partial repro steps
- classifies severity (Blocker / Critical / Major / Minor / Trivial) and priority (High / Medium / Low)
- formats a complete bug report following a consistent template (title, environment, steps, expected/actual, logs)
- confirms the report with the user before taking any action
- optionally creates a Jira Bug ticket via the Atlassian MCP

## Suggested prompts

```text
/bug-report-formatter Here's the error I got: NullPointerException at UserService.java:42 — clicking Save on an empty form
```

```text
Format this bug: the checkout page shows $0.00 total after applying discount code SAVE10 on Safari iOS.
```

```text
Turn this stack trace into a Jira ticket: [paste logs]
```

```text
Help me write a proper bug report — I found a defect in the login flow.
```

## Output

A structured markdown report with these sections:

1. Title
2. Environment
3. Steps to Reproduce
4. Expected Result
5. Actual Result
6. Severity / Priority
7. Logs / Attachments
8. Additional Context

## Optional Jira integration

After the report is confirmed, the skill can create a Jira Bug issue directly using the configured Atlassian MCP (`createJiraIssue`). Requires the MCP to be authenticated and a valid project key.

## Reference files

- `references/bug-report-template.md` — the structured output template with field guidance
- `references/severity-guidelines.md` — severity and priority decision matrix
