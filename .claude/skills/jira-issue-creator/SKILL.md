---
name: jira-issue-creator
description: >-
  Create new Jira Cloud issues via the Atlassian MCP: bugs, tasks, stories,
  sub-tasks. Loads project defaults from a local config file. Use when the user
  asks to create a Jira ticket, file a bug, add a task, add a story, or log a
  new issue.
---

# Jira Issue Creator

Use the **Atlassian (Jira) MCP** tools already configured in your MCP client. This skill does not call the REST API directly.

## Prerequisites

- Atlassian MCP is connected and authenticated.
- The authenticated user has **create issue** permissions on the target project.

## Workflow

### Step 0. Load config defaults

Check whether `config/jira-defaults.local.json` exists in the skill directory.

- If present, read it and treat its values as **session defaults**:
  - `site` → default Atlassian site
  - `projectKey` → default project key
  - `defaultIssueType` → pre-fill issue type (e.g. `"Bug"`, `"Task"`, `"Story"`)
- If absent, ask the user for site and project key.

The user can override any default in their prompt (e.g. "use project XYZ", "make it a Task").

### Step 1. Collect inputs

From the user (or config), obtain:

- **Site** — use `site` from config if set
- **Project key** — use `projectKey` from config if set
- **Issue type** — use `defaultIssueType` from config; ask only if not set and user did not specify
- **Summary** — required; built from user input
- **Description** — see Bug template below if issue type is Bug; optional for other types
- **Assignee** (optional) — display name to resolve via `lookupJiraAccountId`
- **Priority, labels, fix version** (optional) — include if user specifies

#### Bug description template

When issue type is `Bug`, build the description using [templates/bug-description.md](./templates/bug-description.md):

- Collect: Initial Condition, Steps to Reproduce, Expected Results, Actual Results
- Optional: Version, Affected Tests
- If the user did not provide Steps to Reproduce, Expected Results, or Actual Results, ask for them before proceeding

### Step 2. Resolve `cloudId`

Call `getAccessibleAtlassianResources` to get the `cloudId` for the target site. Reuse it for all subsequent calls in this session.

### Step 3. Resolve assignee (if named)

If the user names an assignee, call `lookupJiraAccountId` with the display name as `searchString`. Pick the best match and use the returned `accountId`.

### Step 4. Create the issue

Call `createJiraIssue` directly. See [references/create-issue.md](./references/create-issue.md) for full parameter details.

Return the new issue key and URL: `https://<site>/browse/<issue-key>`

## Guardrails

- Do not fabricate field values; only use what the user or config provides.
- If `cloudId` resolution returns multiple sites and no `site` is configured, present them and ask.
