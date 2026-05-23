# Jira Issue Creator

Create new Jira Cloud issues via the Atlassian MCP: bugs, tasks, stories, sub-tasks. Loads project defaults from a local config file so you don't repeat project key or issue type on every prompt.

## Setup

Copy the example config and fill in your values:

```powershell
Copy-Item ./.github/skills/jira-issue-creator/config/jira-defaults.local.example.json `
          ./.github/skills/jira-issue-creator/config/jira-defaults.local.json
```

```json
{
  "site": "your-site.atlassian.net",
  "projectKey": "SCRUM",
  "defaultIssueType": "Bug"
}
```

`jira-defaults.local.json` is gitignored.

## Example prompts

```text
Create a Bug: [Checkout] Order total shows $0.00 after applying a discount code on Safari iOS
```

```text
Add a Task to SCRUM: Set up staging environment for v2 release
```

```text
Create a Story in project PROJ assigned to Jane Doe with priority High: User can reset password via email link
```

## Reference files

- [`references/create-issue.md`](references/create-issue.md) — MCP tool parameters and confirmation block template
- [`config/jira-defaults.local.example.json`](config/jira-defaults.local.example.json) — config template
