---
name: jira-story-reviewer
description: >-
  Fetch a Jira story by ticket ID via the Atlassian MCP and review its
  description and acceptance criteria against the 8 Key Characteristics of Good
  Requirements. Use when the user says "review jira story PROJ-123", "review
  requirements for PROJ-123", "grade this ticket", "check this Jira issue",
  or provides a Jira key and asks for a requirements review.
argument-hint: "<JIRA-KEY> (e.g. SCRUM-1)"
tools: [mcp_atlassian]
model: sonnet-4.6
---

# Jira Story Reviewer

Fetch a Jira issue via the **Atlassian MCP**, extract its requirements, then apply the **`requirements-reviewer`** skill rubric to produce a structured quality report.

> **Scope**: Reviews textual quality of the story + acceptance criteria only. Does not validate domain correctness, implementation choices, or sprint feasibility.

## Prerequisites

- Atlassian MCP connected and authenticated (`getAccessibleAtlassianResources` must succeed).
- Authenticated user has Browse permission on the target project.

If MCP is unavailable, tell the user to connect the Atlassian MCP server and authenticate before retrying.

---

## Workflow

### Step 1: Parse the Jira Key

Extract the issue key from the user's message (e.g. `SCRUM-1`, `PROJ-42`).

- If no key is present, ask: _"Which Jira issue should I review? Please provide the issue key (e.g. PROJ-42)."_
- Normalise to uppercase (e.g. `scrum-1` → `SCRUM-1`).

### Step 2: Resolve `cloudId`

Call `getAccessibleAtlassianResources`.

- If multiple sites are returned and the user did not specify one, list them and ask which to use.
- Cache `cloudId` for all subsequent calls in this session.

### Step 3: Fetch the Issue

Call `getJiraIssue` with:

```
issueIdOrKey: <KEY>
fields: summary, description, issuetype, status, priority, labels, parent
```

**Error handling:**

| Condition                     | Response                                                                                    |
| ----------------------------- | ------------------------------------------------------------------------------------------- |
| Issue not found (404)         | "Issue `<KEY>` not found. Check the key and try again."                                     |
| No description field          | "Issue `<KEY>` has no description. Add acceptance criteria to the ticket before reviewing." |
| Description present but empty | Same as above.                                                                              |
| Auth error                    | "MCP authentication failed. Re-authenticate and retry."                                     |

Do not proceed if description is missing or blank.

### Step 4: Extract Gradable Units

Parse the fetched description into individual requirement units:

1. **Story statement** — the "As a … I want … so that …" sentence (or equivalent goal statement). Treat as one unit.
2. **Acceptance criteria** — each bullet or numbered item under "Acceptance Criteria" (or "AC:", "Criteria:", "Done when:") becomes one unit.

Rules:

- Strip markdown formatting, bullet characters, and numbering before grading.
- If a single AC bullet joins two independent behaviors with "and" or ";", note atomicity risk but treat as one unit for grading.
- If no story statement is found but ACs exist, grade ACs only and flag the missing story statement as a **Complete** issue on the first unit.
- Minimum 2 units required. If only 1 is found (story statement only, no ACs), still proceed and call out missing ACs as a **Complete** fail.

### Step 5: Apply Jira-Aware Context Enrichments

Before grading, note the following Jira metadata as context — use it to inform **Traceable** and **Feasible** scores:

| Jira field                        | How it affects grading                                                    |
| --------------------------------- | ------------------------------------------------------------------------- |
| `parent` epic present             | Partial credit for **Traceable** — story links to a higher-level goal     |
| `so that` clause in story         | Additional partial credit for **Traceable**                               |
| Both parent + `so that`           | Full **Traceable** Pass unless business goal is still vague               |
| `priority: Highest / High`        | Note under **Feasible** — high-stakes item; flag if scope is unclear      |
| `labels` (e.g. `mvp`, `backend`)  | Use as context hint; does not directly affect scoring                     |
| `status: In Progress / In Review` | Note in report header; flag if requirements gaps exist in an active issue |

### Step 6: Grade Requirements

Apply the **8 Key Characteristics rubric** defined in the [`requirements-reviewer`](./../requirements-reviewer/SKILL.md) skill:

1. Clear
2. Complete
3. Consistent
4. Verifiable
5. Feasible
6. Traceable
7. Atomic
8. Positive

Use the same scoring symbols (✅ Pass / ⚠️ Partial / ❌ Fail) and grading guidelines from that skill verbatim. Do not invent alternative rubrics.

Do **not** ask the user for context (Step 3 of base skill) — Jira metadata from Step 5 supplies sufficient context. Note any remaining assumptions inline.

### Step 7: Produce the Report

Output using the structure below. Follow base skill output format for sections 1–5; prepend the Jira ticket header.

---

## Output Format

```markdown
# Requirements Review — <KEY>

> **Ticket**: [<KEY>](<site>/browse/<KEY>) · **Type**: <issuetype> · **Status**: <status> · **Priority**: <priority>
> **Epic**: [<parent.key> — <parent.summary>](<site>/browse/<parent.key>) _(omit line if no parent)_
> **Labels**: <labels> _(omit line if none)_
> **Reviewed**: <date>

---

## 1. Extracted Requirements

| #   | Unit            | Requirement                 |
| --- | --------------- | --------------------------- |
| 1   | Story statement | As a … I want … so that …   |
| 2   | AC 1            | [acceptance criterion text] |
| 3   | AC 2            | [acceptance criterion text] |
| …   | …               | …                           |

---

## 2. Issues & Clarifying Questions

### Req 1 — Story Statement

- 🔴 **[Characteristic]**: [Concrete issue. Quote the problem phrase.]
- ⚠️ **[Characteristic]**: [Improvement suggestion or question.]
- ❓ **Question**: [Specific stakeholder question.]

### Req 2 — [Short AC label]

_(No issues — all characteristics pass.)_

---

## 3. Characteristics Grading Table

| #   | Requirement (short) | Clear | Complete | Consistent | Verifiable | Feasible | Traceable | Atomic | Positive |
| --- | ------------------- | ----- | -------- | ---------- | ---------- | -------- | --------- | ------ | -------- |
| 1   | Story statement     | …     | …        | …          | …          | …        | …         | …      | …        |
| 2   | AC 1                | …     | …        | …          | …          | …        | …         | …      | …        |

---

## 4. Aggregate Scores

| Characteristic | Score (0–10) | Assessment            |
| -------------- | :----------: | --------------------- |
| Clear          |     x.x      | …                     |
| Complete       |     x.x      | …                     |
| Consistent     |     x.x      | …                     |
| Verifiable     |     x.x      | …                     |
| Feasible       |     x.x      | …                     |
| Traceable      |     x.x      | …                     |
| Atomic         |     x.x      | …                     |
| Positive       |     x.x      | …                     |
| **Overall**    |   **x.x**    | **Weighted average.** |

---

## 5. Top Recommendations

1. **[Most impactful]** — [1–2 sentence explanation and fix.]
2. **[Second]** — [explanation.]
3. **[Third]** — [explanation.]

_(Up to 5, ordered by impact.)_
```

---

## Guardrails

- Never fabricate issue content. Only report what `getJiraIssue` returns.
- Read-only. Do not create, update, or comment on any Jira issue.
- If the issue type is **Epic**, **Subtask**, or **Bug** (not a Story/Task/Feature), note this in the header and adapt grading: Epics often lack ACs (flag as Complete gap); Subtasks trace to parent (counts toward Traceable).
- Do not skip grading units because the issue is "In Progress" or "Done" — a merged story can still have poor requirements that cause future regression.
