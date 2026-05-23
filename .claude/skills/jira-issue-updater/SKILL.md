---
name: jira-issue-updater
description: >-
  Update existing Jira Cloud issues via the Atlassian MCP: transition statuses,
  add comments, edit fields (priority, labels, fix version, summary), and link
  issues. Use when the user asks to move an issue to a different status, add a
  comment to a ticket, change a field on an existing issue, or link two issues
  together.
---

# Jira Issue Updater

Use the **Atlassian (Jira) MCP** tools already configured in your MCP client. This skill does not call the REST API directly.

## Prerequisites

- Atlassian MCP is connected and authenticated.
- The authenticated user has **edit** permissions on the target issues.

## Workflow

### Step 0. Load config defaults

Check whether `config/jira-defaults.local.json` exists in the skill directory.

- If present, read it and treat its values as **session defaults**:
  - `site` → default Atlassian site
  - `projectKey` → informational default (issue keys in update operations are always explicit)
- If absent, ask the user for the site if needed.

The user can override any default in their prompt.

### Step 1. Collect inputs

From the user (or config), obtain:

- **Site** — use `site` from config if set
- **Issue key** — explicit (e.g. `PROJ-42`)
- **Operation** — transition / comment / edit / link

### Step 2. Resolve `cloudId`

Call `getAccessibleAtlassianResources` to get the `cloudId` for the target site. Reuse it for all subsequent calls in this session.

### Step 3. Execute the operation

Route based on the user's request. See [references/update-operations.md](./references/update-operations.md) for full MCP tool parameters and confirmation block templates.

#### Transition status

1. Call `getTransitionsForJiraIssue` to fetch available transitions.
2. Match the user's target status (case-insensitive). If no match, show available transitions and ask the user to pick.
3. Call `transitionJiraIssue` directly.
4. Return the new status.

#### Add comment

1. Parse issue key and comment text.
2. Call `addCommentToJiraIssue` with `contentFormat: "markdown"` directly.
3. Return the issue link on success.

#### Edit fields

1. Parse the field(s) to update (priority, labels, fix version, summary, description, etc.).
2. If updating the **description of a Bug issue**, apply [templates/bug-description.md](./templates/bug-description.md) to format the description. Collect any missing required sections (Steps to Reproduce, Expected Results, Actual Results) before proceeding.
3. Call `editJiraIssue` directly.

#### Link issues

1. Parse the two issue keys and the link type (e.g. "blocks", "duplicates", "relates to").
2. Call `getIssueLinkTypes` to confirm available link types and pick the correct one.
3. Call `createIssueLink` directly.

## Guardrails

- Never invent transition IDs; always fetch them with `getTransitionsForJiraIssue` first.
- If `cloudId` resolution returns multiple sites and no `site` is configured, present them and ask.
