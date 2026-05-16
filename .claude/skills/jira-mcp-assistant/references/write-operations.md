# Write Operations Reference

This file documents the MCP tool parameters and confirmation patterns for mutating Jira operations. The SKILL.md workflow sections 6–8 reference this file.

**Hard rule for all write operations:** always show the user what will be sent and ask for explicit confirmation before calling any mutating MCP tool. Never skip confirmation even if the user seems certain.

---

## Create Issue (Section 6)

**MCP tool:** `createJiraIssue`

**Required parameters:**
- `cloudId` — resolved from `getAccessibleAtlassianResources`
- `projectKey` — from prompt or `config/jira-defaults.local.json`
- `issueTypeName` — from prompt or `defaultIssueType` in config (e.g. `"Bug"`, `"Task"`, `"Story"`)
- `summary` — short title, built from user input

**Common optional parameters:**
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

**Confirmation block to show the user before calling:**

```
About to create:
  Type:    Bug
  Project: SCRUM
  Title:   [Checkout] Order total shows $0.00 after discount code on Safari
  Priority: High
  Assignee: (unassigned)

Proceed? (Yes / No)
```

**On success:** return the issue key and the Jira URL:
`https://<site>/browse/<issue-key>`

**Assignee resolution:** if the user provides a display name (e.g. "assign to John Doe"), call `lookupJiraAccountId` with the name as `searchString`, pick the best match, and use the returned `accountId`.

---

## Transition Issue Status (Section 7)

**MCP tools:** `getTransitionsForJiraIssue` → `transitionJiraIssue`

**Workflow:**

1. Parse the user's request: issue key + target status name (e.g. "move PROJ-42 to In Review").
2. Call `getTransitionsForJiraIssue` with `cloudId` and `issueIdOrKey`.
3. From the returned list, find the transition whose `name` matches (case-insensitive) the user's target.
   - If an exact match: proceed.
   - If no match: show all available transition names and ask the user to pick one.
   - If multiple partial matches: show them and ask the user to confirm.
4. Show confirmation:

```
About to transition:
  Issue:  PROJ-42
  From:   In Progress
  To:     In Review  (transition id: 31)

Proceed? (Yes / No)
```

5. Call `transitionJiraIssue` with `cloudId`, `issueIdOrKey`, and `transition: { "id": "<id>" }`.
6. On success, confirm the new status. On error, surface the exact MCP response.

---

## Add Comment (Section 8)

**MCP tool:** `addCommentToJiraIssue`

**Required parameters:**
- `cloudId`
- `issueIdOrKey` — e.g. `PROJ-42`
- `commentBody` — the comment text; send with `contentFormat: "markdown"` for markdown formatting

**Optional parameters:**
- `commentVisibility` — restrict visibility to a group or role:
  ```json
  { "type": "role", "value": "Service Desk Team" }
  ```
  Only use this if the user explicitly requests restricted visibility.

**Confirmation block:**

```
About to add a comment to PROJ-42:

---
<comment text preview (first 300 chars)>
---

Proceed? (Yes / No)
```

**On success:** confirm the comment was added and show the issue link.

---

## Edit Issue Fields (bonus, not a numbered section)

**MCP tool:** `editJiraIssue`

Use when the user asks to update a field on an existing issue (e.g. "change the priority of PROJ-42 to Low", "set fix version to 2.0.0").

**Parameters:**
- `cloudId`, `issueIdOrKey`
- `fields` — JSON object of fields to update:
  ```json
  { "priority": { "name": "Low" } }
  { "fixVersions": [{ "name": "2.0.0" }] }
  { "labels": ["smoke", "regression"] }
  { "summary": "Updated title text" }
  ```
- Use `contentFormat: "markdown"` when updating description.

**Confirmation block:**

```
About to update PROJ-42:
  priority: Medium → Low

Proceed? (Yes / No)
```

---

## Link Issues (bonus)

**MCP tool:** `createIssueLink`

Use when the user says "link PROJ-42 to PROJ-18 as a blocker" or "mark PROJ-10 as duplicated by PROJ-11".

**Parameters:** see `getIssueLinkTypes` for available link type names (e.g. `"Blocks"`, `"Duplicate"`, `"Relates to"`).

Confirm the link type and direction before calling.
