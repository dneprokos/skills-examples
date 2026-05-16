---
name: jira-mcp-assistant
description: >-
  Work with Jira Cloud via the Atlassian MCP: search with JQL, view backlogs
  and sprints, create and update issues, transition statuses, and add comments.
  Loads project defaults from a local config file so you don't need to repeat
  project key or site on every prompt. Use when the user asks for Jira backlog
  items, project issues, sprint scope, any JQL-driven list, wants to create a
  Jira ticket, move an issue to a different status, add a comment to a ticket,
  update issue fields, or link two issues together.
---

# Jira MCP Assistant

Use the **Atlassian (Jira) MCP** tools already configured in Cursor (or another MCP client). This skill does not call the REST API directly; it tells the agent **how** to use MCP consistently.

## Prerequisites

- Atlassian MCP is connected and authenticated (OAuth or API token per your org's [Rovo MCP settings](https://support.atlassian.com/rovo/docs/setting-up-ides/)).
- The authenticated user can **browse** the target project and run JQL.

If tools are missing, complete MCP authentication first; do not guess endpoints or tokens.

## When this skill fits

- List backlog or board issues for a project.
- Run a user-supplied or template JQL query and return a readable summary.
- Create, edit, or transition Jira issues.
- Add comments to existing issues.
- Link two issues together.

## Workflow

### Step 0. Load config defaults

Before asking the user for anything, check whether `config/jira-defaults.local.json` exists in the skill directory.

- If the file exists, read it and treat its values as **defaults** for the current session:
  - `site` → default Atlassian site
  - `projectKey` → default project key for queries and new issues
  - `boardName` → informational label; use in output headings
  - `defaultIssueType` → pre-fill issue type when creating issues
  - `defaultFields` → columns to include in result tables
  - `defaultOrderBy` → default JQL `ORDER BY` clause
  - `maxResultsPerPage` → default page size for searches
- If the file is absent, fall back to asking the user for site and project key.

The user can always override any default in their prompt.

To set up the config file, copy `config/jira-defaults.local.example.json` to `config/jira-defaults.local.json` and fill in your values.

### Step 1. Collect inputs

From the user (or config defaults), obtain:

- **Site** (e.g. `your-site.atlassian.net`) — use config `site` if set; confirm with user if multiple sites are accessible.
- **Project key** (e.g. `SCRUM`) — use config `projectKey` if set.
- **Intent:** search / list / create / transition / comment / edit / link.

### Step 2. Resolve `cloudId`

Use `getAccessibleAtlassianResources` to get the `cloudId` for the target site.

- If only one site is accessible and a `site` is configured, use that `cloudId` without asking.
- **Session hint:** once `cloudId` is resolved, reuse it for all subsequent calls in the same session. Do not call `getAccessibleAtlassianResources` again unless the user switches sites.

### Step 3. Execute the intent

Route to the appropriate step below based on the user's request.

---

### Steps 4–5: Read / search (JQL queries)

#### Step 4. Search with JQL

Call `searchJiraIssuesUsingJql`.

- Build JQL using [references/jql-snippets.md](./references/jql-snippets.md) or the user's own query. Default project key and `ORDER BY` come from config when available.
- Request fields from `defaultFields` in config, plus any extra fields the user's question requires. Minimum: `key`, `summary`, `issuetype`, `status`.
- Always use `responseContentFormat: "markdown"` for readable output.
- Respect pagination (`maxResults` from config or default 25). If the user wants the full set, page until no more results or a cap the user confirms.

#### Step 5. Present results

Return a **markdown table** with the columns from `defaultFields` (or user-specified fields).

- Include issue URLs as clickable links in the key column: `[PROJ-42](https://site.atlassian.net/browse/PROJ-42)`.
- When results are truncated: show `Showing 25 of 142 issues. Say "next page" to continue.`
- Use a **compact** format (key, summary, status) for quick overviews; use a **detailed** format (all configured fields) when the user asks for full details.

**Optional deep fetch:** if search results omit fields the user needs, use `getJiraIssue` for specific keys — avoid N+1 calls for large lists unless necessary.

---

### Steps 6–8: Write operations

All write operations require explicit user confirmation before the MCP tool is called. See [references/write-operations.md](./references/write-operations.md) for full parameter details and confirmation block templates.

#### Step 6. Create issue

Use when the user asks to create a ticket, file a bug, add a task, etc.

1. Pre-fill `projectKey` and `issueTypeName` from config defaults; ask only for what is missing.
2. Build `summary` and (optional) `description` from the user's input.
3. Resolve `assignee_account_id` via `lookupJiraAccountId` if an assignee is named.
4. Show a confirmation block (see `references/write-operations.md`).
5. On confirmation, call `createJiraIssue`. Return the new issue key and URL.

#### Step 7. Transition issue status

Use when the user asks to move an issue to a different status.

1. Parse the issue key and target status name from the user's request.
2. Call `getTransitionsForJiraIssue` to fetch available transitions.
3. Match the target to a transition by name (case-insensitive). If no match, show available transitions and ask the user to pick.
4. Show a confirmation block.
5. On confirmation, call `transitionJiraIssue`. Return the new status.

#### Step 8. Add comment

Use when the user asks to comment on or update an issue with a note.

1. Parse the issue key and comment text.
2. Show a preview of the comment (first 300 characters) with a confirmation prompt.
3. On confirmation, call `addCommentToJiraIssue` with `contentFormat: "markdown"`.
4. Confirm success and return the issue link.

---

## Guardrails

- Do not fabricate issues, JQL results, or field values; only report what MCP returns.
- For all **mutating** operations (create, transition, edit, comment, link), confirm with the user before calling the tool.
- If `cloudId` resolution returns multiple sites and no `site` is configured, present them and ask the user to pick one.
- Never invent transition IDs; always fetch them with `getTransitionsForJiraIssue` first.

## Extending this skill

See the repository [README.md](../../../README.md) section **Jira skills and Atlassian MCP** for how to add new workflows without renaming the skill.

Additional reference files:
- [references/jql-snippets.md](./references/jql-snippets.md) — JQL templates for common backlog, sprint, and QA queries
- [references/write-operations.md](./references/write-operations.md) — MCP tool parameters for create, transition, comment, edit, link
- [config/jira-defaults.local.example.json](./config/jira-defaults.local.example.json) — config template
