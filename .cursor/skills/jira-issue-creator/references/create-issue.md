# Create Issue Reference

**MCP tool:** `createJiraIssue`

---

## Required parameters

- `cloudId` — resolved from `getAccessibleAtlassianResources`
- `projectKey` — from prompt or `config/jira-defaults.local.json`
- `issueTypeName` — from prompt or `defaultIssueType` in config (e.g. `"Bug"`, `"Task"`, `"Story"`)
- `summary` — short title built from user input

## Common optional parameters

- `description` — full body; use `contentFormat: "markdown"` for markdown input
- `assignee_account_id` — resolve via `lookupJiraAccountId` if the user names an assignee
- `additional_fields` — use for priority, labels, fix version, and custom fields:
  ```json
  {
    "priority": { "name": "High" },
    "labels": ["regression", "smoke"],
    "fixVersions": [{ "name": "1.2.0" }]
  }
  ```
- `parent` — issue key of the parent (for sub-tasks)

## On success

Return the issue key and the Jira URL: `https://<site>/browse/<issue-key>`

## Assignee resolution

If the user provides a display name (e.g. "assign to John Doe"), call `lookupJiraAccountId` with the name as `searchString`, pick the best match, and use the returned `accountId`.
