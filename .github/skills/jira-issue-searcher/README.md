# Jira Issue Searcher

Search and browse Jira Cloud issues via the Atlassian MCP. Run JQL queries, view backlogs, sprint scope, bug lists, stale issues, and any JQL-driven list.

## Setup

Copy the example config and fill in your values:

```powershell
Copy-Item ./.github/skills/jira-issue-searcher/config/jira-defaults.local.example.json `
          ./.github/skills/jira-issue-searcher/config/jira-defaults.local.json
```

```json
{
  "site": "your-site.atlassian.net",
  "projectKey": "SCRUM",
  "boardName": "SCRUM board",
  "defaultFields": ["summary", "status", "priority", "assignee", "sprint"],
  "defaultOrderBy": "Rank ASC",
  "maxResultsPerPage": 25
}
```

`jira-defaults.local.json` is gitignored.

## Example prompts

```text
List backlog issues for my default project.
```

```text
Show open bugs in the current sprint ordered by priority.
```

```text
Run this JQL: project = SCRUM AND issuetype = Bug ORDER BY updated DESC
```

```text
Show stale issues not updated in more than 7 days.
```

```text
List issues assigned to me that are not done.
```

## Reference files

- [`references/jql-snippets.md`](references/jql-snippets.md) — JQL templates for backlog, sprint, bugs, staleness, release
- [`config/jira-defaults.local.example.json`](config/jira-defaults.local.example.json) — config template
