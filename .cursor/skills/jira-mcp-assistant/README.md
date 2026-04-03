# Jira MCP Assistant

A workflow skill for working with **Jira Cloud** via the **Atlassian (Jira) MCP** tools already configured in Cursor. Supports read queries (JQL/backlog/sprint) and write operations (create, transition, comment, edit, link).

## What it does

- Loads project defaults from a local config file — no need to repeat project key or site in every prompt
- Resolves the Atlassian `cloudId` automatically (and caches it within the session)
- Runs **JQL searches** (backlog, sprint, bug lists, stale issues, and more)
- Returns results as a clean **markdown table** with clickable issue links
- **Creates** new Jira issues (Bug, Task, Story, etc.)
- **Transitions** issue statuses (e.g. "move PROJ-42 to In Review")
- **Adds comments** to existing issues
- **Edits** issue fields (priority, labels, fix version, etc.)
- **Links** two issues together

---

## Quick setup: local config file

Copy the example config and fill in your values. The skill will load it automatically and use the values as defaults.

```powershell
Copy-Item ./.cursor/skills/jira-mcp-assistant/config/jira-defaults.local.example.json `
          ./.cursor/skills/jira-mcp-assistant/config/jira-defaults.local.json
```

Then edit `jira-defaults.local.json`:

```json
{
  "site": "your-site.atlassian.net",
  "projectKey": "SCRUM",
  "boardName": "SCRUM board",
  "defaultIssueType": "Bug",
  "defaultFields": ["summary", "status", "priority", "assignee", "sprint"],
  "defaultOrderBy": "Rank ASC",
  "maxResultsPerPage": 25
}
```

`jira-defaults.local.json` is gitignored — safe to store your project key and site there.

---

## Suggested prompts

### Read / search

```text
List backlog issues for project SCRUM using the jira-mcp-assistant skill.
```

```text
Show me open bugs in the current sprint, ordered by priority.
```

```text
Run this JQL and summarize the results as a table:
project = SCRUM AND issuetype = Bug ORDER BY updated DESC
```

```text
Show stale issues not updated in more than 7 days.
```

### Write operations

```text
Create a Bug in SCRUM: [Checkout] Order total shows $0.00 after applying a discount code on Safari iOS
```

```text
Move PROJ-42 to "In Review".
```

```text
Add a comment to PROJ-55: "Reproduced on staging. Logs attached to the ticket."
```

```text
Change the priority of PROJ-33 to Low.
```

---

## Prerequisites

- **Atlassian MCP is connected and authenticated** (OAuth or API token, depending on your org's Rovo MCP settings).
- Your authenticated user can **browse** the target Jira project and run JQL.
- For write operations, the user also needs **edit** permissions on the target project.

## Configure Atlassian MCP auth (API token, no helper scripts)

This skill expects the MCP server to receive an HTTP `Authorization` header.

1. Create an **Atlassian API token** for the same Atlassian account that has access to your Jira Cloud site:  
   https://id.atlassian.com/manage-profile/security/api-tokens

2. Build the HTTP Basic auth value:
   - Take: `email:api_token`
   - Encode the combined string as **Base64 (UTF-8)**
   - Prefix with `Basic `  
   Result format: `Basic <base64(email:api_token)>`

3. Set a Windows **user** environment variable:
   - Name: `ATLASSIAN_MCP_AUTHORIZATION`
   - Value: the full `Basic <base64...>` string from step 2

4. Wire it into MCP config (example for `mcp.json`):

```json
{
  "mcpServers": {
    "Atlassian-MCP-Server": {
      "url": "https://mcp.atlassian.com/v1/mcp",
      "headers": {
        "Authorization": "${env:ATLASSIAN_MCP_AUTHORIZATION}"
      }
    }
  }
}
```

Notes:
- Keep `ATLASSIAN_MCP_AUTHORIZATION` out of git. Prefer **user env vars** over committed files.
- If your org/client setup uses OAuth login, you may not need `mcp.json` at all — Cursor can prompt you to sign in.

## OAuth note (optional)

If you configure MCP with OAuth, Cursor typically opens a browser sign-in flow. In that case, you do not need the API-token-based `ATLASSIAN_MCP_AUTHORIZATION` header.

## Helper scripts (optional) — simplify the same steps

If you don't want to do Base64 and env-var setup manually, you can use the repo scripts:

- [`../../../Build-AtlassianMcpAuthorization.ps1`](../../../Build-AtlassianMcpAuthorization.ps1): prompts for email + token and prints `Basic ...`
- [`../../../Set-AtlassianMcpAuthorizationUserEnv.ps1`](../../../Set-AtlassianMcpAuthorizationUserEnv.ps1): prompts for `Basic ...` and sets `ATLASSIAN_MCP_AUTHORIZATION`

Security reminder: do not commit secrets or paste tokens into issues/PRs.

---

## Output format

By default the skill returns a table with columns from `defaultFields` in your config (or key, summary, type, status as the minimum). Issue keys are clickable links to the Jira UI.

When results are paginated: `Showing 25 of 142 issues. Say "next page" to continue.`

---

## Reference files

- [`references/jql-snippets.md`](references/jql-snippets.md) — JQL templates for backlog, sprint, bugs, staleness, release
- [`references/write-operations.md`](references/write-operations.md) — MCP tool parameters for create, transition, comment, edit, link
- [`config/jira-defaults.local.example.json`](config/jira-defaults.local.example.json) — config template

---

## Extending this skill

To add new Jira workflows without breaking discovery:

1. Keep the umbrella skill id as `jira-mcp-assistant`
2. Update `SKILL.md` description to include new trigger phrases
3. Add implementation guidance as new sections in `SKILL.md`
4. Split large guidance into more files under `references/`

This repo's main README explains the intended extension approach.
