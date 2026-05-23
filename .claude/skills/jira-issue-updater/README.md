# Jira Issue Updater

Update existing Jira Cloud issues via the Atlassian MCP: transition statuses, add comments, edit fields, and link issues.

## Setup

Copy the example config and fill in your values:

```powershell
Copy-Item ./.github/skills/jira-issue-updater/config/jira-defaults.local.example.json `
          ./.github/skills/jira-issue-updater/config/jira-defaults.local.json
```

```json
{
  "site": "your-site.atlassian.net",
  "projectKey": "SCRUM"
}
```

`jira-defaults.local.json` is gitignored.

## Example prompts

```text
Move PROJ-42 to "In Review".
```

```text
Add a comment to PROJ-55: "Reproduced on staging. Logs attached to the ticket."
```

```text
Change the priority of PROJ-33 to Low.
```

```text
Set fix version of PROJ-18 to 2.0.0.
```

```text
Link PROJ-42 to PROJ-18 as a blocker.
```

## Reference files

- [`references/update-operations.md`](references/update-operations.md) — MCP tool parameters and confirmation block templates for transition, comment, edit, and link
- [`config/jira-defaults.local.example.json`](config/jira-defaults.local.example.json) — config template
