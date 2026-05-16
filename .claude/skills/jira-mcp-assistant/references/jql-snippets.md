# JQL snippets for Jira MCP Assistant

Replace `PROJ` with the user's project key (or the `projectKey` from `config/jira-defaults.local.json`). Adjust issue types, statuses, and field values as needed.

---

## Backlog and ranking

### Ranked project issues (backlog screen: sprint + backlog column)

Often matches what users see on a Scrum backlog view ordered by rank:

```jql
project = PROJ ORDER BY Rank ASC
```

### Issues not in any sprint ("backlog" section only)

```jql
project = PROJ AND sprint IS EMPTY ORDER BY Rank ASC
```

---

## Sprint views

### Active sprint issues

```jql
project = PROJ AND sprint in openSprints() ORDER BY Rank ASC
```

### Open work in a project (not done)

```jql
project = PROJ AND statusCategory != "Done" ORDER BY updated DESC
```

---

## Bug and defect queries (QA focus)

### Open bugs by priority

```jql
project = PROJ AND issuetype = Bug AND statusCategory != "Done" ORDER BY priority ASC, updated DESC
```

### My open bugs

```jql
project = PROJ AND issuetype = Bug AND assignee = currentUser() AND resolution = Unresolved ORDER BY priority ASC
```

### Bugs created this week

```jql
project = PROJ AND issuetype = Bug AND created >= startOfWeek() ORDER BY created DESC
```

### Bugs in a specific release/version

```jql
project = PROJ AND issuetype = Bug AND fixVersion = "1.2.0" ORDER BY priority ASC, Rank ASC
```

### Blocked issues

```jql
project = PROJ AND status = "Blocked" ORDER BY priority ASC, updated ASC
```

---

## Staleness and activity

### Not updated recently (stale issues check)

Issues untouched for more than 7 days that are still open — useful for grooming:

```jql
project = PROJ AND updated <= -7d AND statusCategory != "Done" ORDER BY updated ASC
```

### Created this week across all issue types

```jql
project = PROJ AND created >= startOfWeek() ORDER BY created DESC
```

---

## Filtering by team or component

### Issues assigned to current user

```jql
assignee = currentUser() AND resolution = Unresolved ORDER BY updated DESC
```

### Issues by component

Replace `ComponentName` with the actual Jira component name:

```jql
project = PROJ AND component = "ComponentName" ORDER BY Rank ASC
```

### Issues by label

```jql
project = PROJ AND labels = "regression" ORDER BY priority ASC, updated DESC
```

---

## Release readiness

### Issues in a fix version not yet done

```jql
project = PROJ AND fixVersion = "1.2.0" AND statusCategory != "Done" ORDER BY priority ASC
```

### Issues without a fix version (unversioned backlog)

```jql
project = PROJ AND fixVersion is EMPTY AND statusCategory != "Done" ORDER BY Rank ASC
```

---

## Notes

- **Sprint** field behavior can vary with team-managed vs company-managed projects; if results look wrong, narrow with `board` or saved filter tools when MCP exposes them.
- Prefer `ORDER BY Rank ASC` when the user cares about backlog order.
- `startOfWeek()` and `startOfDay()` are JQL date functions — not all Jira Cloud instances enable all functions; fall back to relative dates like `-7d` if a function errors.
- Status names like `"Blocked"` are project-specific — check actual statuses with `getJiraProjectIssueTypesMetadata` if results are empty.
