# Update Operations Reference

---

## Transition Issue Status

**MCP tools:** `getTransitionsForJiraIssue` → `transitionJiraIssue`

**Workflow:**

1. Parse issue key + target status name from user request (e.g. "move PROJ-42 to In Review").
2. Call `getTransitionsForJiraIssue` with `cloudId` and `issueIdOrKey`.
3. Match target to a transition by name (case-insensitive):
   - Exact match → proceed.
   - No match → show all available transition names and ask the user to pick.
   - Multiple partial matches → show them and ask user to confirm.
4. Call `transitionJiraIssue` with `cloudId`, `issueIdOrKey`, and `transition: { "id": "<id>" }`.
5. On success, confirm the new status. On error, surface the exact MCP response.

---

## Add Comment

**MCP tool:** `addCommentToJiraIssue`

**Required parameters:**
- `cloudId`
- `issueIdOrKey` — e.g. `PROJ-42`
- `commentBody` — comment text; use `contentFormat: "markdown"` for markdown formatting

**Optional parameters:**
- `commentVisibility` — restrict visibility to a group or role:
  ```json
  { "type": "role", "value": "Service Desk Team" }
  ```
  Only use if the user explicitly requests restricted visibility.

On success: confirm the comment was added and show the issue link.

---

## Edit Issue Fields

**MCP tool:** `editJiraIssue`

Use when the user asks to update a field on an existing issue (e.g. "change priority of PROJ-42 to Low", "set fix version to 2.0.0").

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

---

## Link Issues

**MCP tool:** `createIssueLink`

Use when the user says "link PROJ-42 to PROJ-18 as a blocker" or "mark PROJ-10 as duplicated by PROJ-11".

**Workflow:**

1. Parse the two issue keys and the link direction/type from the user's request.
2. Call `getIssueLinkTypes` to get available link type names (e.g. `"Blocks"`, `"Duplicate"`, `"Relates to"`).
3. Match the user's intent to the correct type and direction.
4. Call `createIssueLink` directly.
