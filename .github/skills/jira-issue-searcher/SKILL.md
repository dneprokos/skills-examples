---
name: jira-issue-searcher
description: >-
  Search and browse Jira Cloud issues via the Atlassian MCP. Run JQL queries,
  view backlogs, sprint scope, bug lists, stale issues, and any JQL-driven list.
  Use when the user asks for Jira backlog items, project issues, sprint issues,
  open bugs, issues by status, or wants to run a JQL query.
---

# Jira Issue Searcher

Use the **Atlassian (Jira) MCP** tools already configured in your MCP client. This skill does not call the REST API directly.

## Prerequisites

- Atlassian MCP is connected and authenticated.
- The authenticated user can **browse** the target project and run JQL.

If tools are missing, complete MCP authentication first.

## Workflow

### Step 0. Load config defaults

Check whether `config/jira-defaults.local.json` exists in the skill directory.

- If present, read it and treat its values as **session defaults**:
  - `site` → default Atlassian site
  - `projectKey` → default project key
  - `boardName` → informational label for output headings
  - `defaultFields` → columns to include in result tables
  - `defaultOrderBy` → default JQL `ORDER BY` clause
  - `maxResultsPerPage` → default page size (default 25 if absent)
- If absent, ask the user for site and project key.

The user can override any default in their prompt (e.g. "use project XYZ").

### Step 1. Collect inputs

From the user (or config), obtain:

- **Site** — use `site` from config if set
- **Project key** — use `projectKey` from config if set; confirm if multiple sites accessible
- **Query intent** — what to search for (backlog, sprint, bugs, custom JQL, etc.)

### Step 2. Resolve `cloudId`

Call `getAccessibleAtlassianResources` to get the `cloudId` for the target site. Reuse it for all subsequent calls in this session — do not call again unless the user switches sites.

### Step 3. Build and run JQL

Call `searchJiraIssuesUsingJql`.

- Use [references/jql-snippets.md](./references/jql-snippets.md) for common query templates.
- Substitute `PROJ` with the active project key.
- Apply default `ORDER BY` from config if the user did not specify one.
- Request `defaultFields` from config, plus any extra fields the user's question requires. Minimum: `key`, `summary`, `issuetype`, `status`.
- Always use `responseContentFormat: "markdown"`.
- Respect `maxResultsPerPage` from config. Page through results if the user wants the full set.

### Step 4. Present results

Return a **markdown table** with columns from `defaultFields` (or user-specified fields).

- Issue keys as clickable links: `[PROJ-42](https://site.atlassian.net/browse/PROJ-42)`
- When truncated: `Showing 25 of 142 issues. Say "next page" to continue.`
- Use **compact** format (key, summary, status) for quick overviews; **detailed** format when the user asks for full details.

**Optional deep fetch:** if search results omit fields the user needs, use `getJiraIssue` for specific keys — avoid N+1 calls for large lists.

## Guardrails

- Do not fabricate issues, JQL results, or field values; only report what MCP returns.
- If `cloudId` resolution returns multiple sites and no `site` is configured, present them and ask the user to pick one.
