# How to Build a Claude Code Plugin — Test Coverage Gap Analyzer

A hands-on, step-by-step guide for building your first Claude Code plugin **manually**. The goal is practice: you type every file yourself so you learn the plugin anatomy.

The plugin we build is the **Test Coverage Gap Analyzer** — it maps requirements (user stories / acceptance criteria) to existing tests and reports the gaps: ACs with no test, and tests with no AC (orphans).

---

## What a plugin actually is

A Claude Code plugin is a folder with a manifest (`.claude-plugin/plugin.json`) plus any combination of these capability folders:

| Folder                       | What it adds                            | Required? |
| ---------------------------- | --------------------------------------- | --------- |
| `.claude-plugin/plugin.json` | Manifest — name, version, description   | **Yes**   |
| `commands/`                  | Slash commands (`/coverage-gaps`)       | Optional  |
| `skills/`                    | Skills (model-invoked workflows)        | Optional  |
| `agents/`                    | Subagents (specialized workers)         | Optional  |
| `hooks/hooks.json`           | Hooks (event-triggered automation)      | Optional  |
| `.mcp.json`                  | MCP server definitions                  | Optional  |
| `scripts/`                   | Helper scripts called by commands/hooks | Optional  |

A plugin only needs the manifest plus **at least one** capability. For this practice we use **command + skill + agent** (the three most common building blocks).

---

## Final folder structure we are building

```
test-coverage-gap-analyzer/
├── .claude-plugin/
│   └── plugin.json
├── commands/
│   └── coverage-gaps.md
├── skills/
│   └── coverage-mapper/
│       └── SKILL.md
├── agents/
│   └── traceability-agent.md
├── scripts/
│   └── Find-TestFiles.ps1
└── README.md
```

---

## Step 1 — Create the plugin root folder

Pick a workspace folder for plugin development (not inside an existing project). For practice you can use a `plugins/` folder.

```powershell
New-Item -ItemType Directory -Force plugins/test-coverage-gap-analyzer
New-Item -ItemType Directory -Force plugins/test-coverage-gap-analyzer/.claude-plugin
```

The folder name (`test-coverage-gap-analyzer`) is the plugin's identity. Use kebab-case.

---

## Step 2 — Write the manifest (`plugin.json`)

Create `.claude-plugin/plugin.json`. This is the only mandatory file.

```json
{
  "name": "test-coverage-gap-analyzer",
  "version": "0.1.0",
  "description": "Maps requirements and acceptance criteria to existing tests, then reports coverage gaps and orphan tests.",
  "author": {
    "name": "Your Name"
  },
  "keywords": ["qa", "testing", "coverage", "traceability", "requirements"]
}
```

**Field notes:**

- `name` must match the folder name and be unique.
- `version` follows semver. Start at `0.1.0`.
- `description` is what users see when browsing plugins — make it searchable.
- `author` and `keywords` are optional but good practice.

**Checkpoint:** This minimal manifest is already a valid (empty) plugin. Everything else adds capability.

---

## Step 3 — Add the slash command (`/coverage-gaps`)

Commands are Markdown files in `commands/`. The filename becomes the command name: `coverage-gaps.md` → `/coverage-gaps`.

Create `commands/coverage-gaps.md`:

```markdown
---
description: Map acceptance criteria to tests and report coverage gaps and orphan tests.
argument-hint: "[path-to-requirements-file]"
---

# Coverage Gap Analysis

You are running a requirements-to-test traceability analysis.

## Inputs

- Requirements source: `$ARGUMENTS` (a file path, Jira export, or pasted ACs).
  If empty, ask the user where the acceptance criteria live.
- Test files: search the current repository for test files
  (`*.test.*`, `*.spec.*`, `*_test.*`, `test_*.*`, `*Tests.cs`, `*Test.java`).

## Steps

1. Parse each acceptance criterion into a discrete, testable statement.
   Assign each one a stable ID (AC-1, AC-2, ...).
2. Scan the repository test files. For each test, capture its name and
   the behavior it asserts (from the test/describe/it title).
3. Match ACs to tests by intent, not just keywords. A test covers an AC
   when it verifies the same behavior.
4. Produce a **traceability matrix**:
   | AC ID | Acceptance Criterion | Covering Test(s) | Status |
   Status is one of: Covered, Partial, **Gap (no test)**.
5. List **orphan tests** — tests that map to no AC.
6. End with a short summary: total ACs, covered, partial, gaps, orphans,
   and the top 3 highest-risk gaps to address first.

## Rules

- Never invent a test that does not exist in the repo.
- If an AC is ambiguous, flag it instead of guessing coverage.
- Keep the matrix the centerpiece of the output.
```

**Key concepts:**

- `$ARGUMENTS` — whatever the user types after `/coverage-gaps` lands here.
- The frontmatter `description` shows in the command picker; `argument-hint` shows expected input.
- The body is a **prompt** — it instructs Claude what to do when the command runs.

---

## Step 4 — Add a skill (`coverage-mapper`)

Skills differ from commands: commands are **user-invoked** (you type `/name`), skills are **model-invoked** (Claude triggers them automatically when the description matches the situation). Add a skill so coverage analysis kicks in even when the user just _describes_ the need.

Create `skills/coverage-mapper/SKILL.md`:

```markdown
---
name: coverage-mapper
description: >-
  Map acceptance criteria or user stories to existing automated tests and
  identify coverage gaps and orphan tests. Use when the user asks whether
  requirements are tested, wants a traceability matrix, asks "what is not
  covered", reviews test coverage against a spec, or pastes user stories and
  asks if tests exist for them.
---

# Coverage Mapper

Build a requirements-to-test traceability map and surface gaps.

## When to use

- User shares user stories / ACs and asks "are these tested?"
- User wants a traceability matrix.
- User asks which features lack automated tests.

## Workflow

1. **Extract ACs.** Break the spec into atomic, testable statements.
   Give each an ID (AC-1...). Split compound criteria ("and"/"or") apart.
2. **Inventory tests.** Locate test files in the repo and read their
   titles + assertions to learn what each verifies.
3. **Match by behavior.** Link AC ↔ test on intent. One AC may need
   several tests (e.g. happy path + boundary + error).
4. **Classify** each AC: Covered / Partial / Gap.
5. **Find orphans.** Tests that match no AC — either dead tests or
   undocumented requirements.

## Output

- Traceability matrix table (AC ID | Criterion | Tests | Status).
- Orphan test list.
- Risk-ranked gap summary (which gaps matter most and why).

## Hard rules

- Do not claim coverage without a real matching test in the repo.
- Flag ambiguous ACs rather than scoring them as covered.
- Prefer behavior matching over keyword matching.
```

**Why both a command and a skill?** The command is the explicit "run it now" trigger. The skill makes the same capability _discoverable_ — Claude pulls it in when the conversation matches the `description`. Writing a strong `description` (with trigger phrases) is the single most important part of a skill.

---

## Step 5 — Add a subagent (`traceability-agent`)

Agents are specialized workers Claude can delegate to. They run with their own context, so they're ideal for the heavy "scan the whole repo" part without polluting the main conversation.

Create `agents/traceability-agent.md`:

```markdown
---
name: traceability-agent
description: >-
  Scans a repository for test files, extracts what each test verifies, and
  matches them against a provided list of acceptance criteria. Returns a
  traceability matrix and gap list. Use when a coverage analysis needs a
  full-repo test inventory.
tools: Read, Grep, Glob
---

You are a test traceability specialist.

Given a list of acceptance criteria (with IDs) and access to a repository:

1. Use Glob/Grep to find every test file.
2. Read test titles and assertions to determine the behavior each test checks.
3. Match each AC to covering tests by behavior.
4. Return ONLY:
   - A traceability matrix (AC ID | Criterion | Covering Test(s) | Status).
   - An orphan-tests list.
   - A one-paragraph gap summary.

Do not modify any files. Do not invent tests. If no tests match an AC,
mark it "Gap (no test)".
```

**Notes:**

- `tools:` restricts the agent to read-only tools — good safety practice for an analysis agent.
- The command/skill can delegate the repo scan to this agent for large codebases.

---

## Step 6 — (Optional) Add a helper script

If you want deterministic test-file discovery instead of relying on the model, add a script. Create `scripts/Find-TestFiles.ps1`:

```powershell
param(
    [string]$Root = "."
)

$patterns = @(
    "*.test.*", "*.spec.*", "*_test.*", "test_*.*",
    "*Tests.cs", "*Test.java", "*_spec.rb"
)

Get-ChildItem -Path $Root -Recurse -File -Include $patterns |
    Where-Object { $_.FullName -notmatch "node_modules|\\bin\\|\\obj\\" } |
    Select-Object FullName, Name |
    Sort-Object FullName
```

A command or hook can call this to feed Claude an exact test-file list. (Optional — skip if you want a pure-prompt plugin.)

---

## Step 7 — Add a README (human-facing)

Create `README.md` so humans understand the plugin:

```markdown
# Test Coverage Gap Analyzer

Maps acceptance criteria to automated tests and reports gaps + orphans.

## Commands

- `/coverage-gaps [requirements-file]` — run a traceability analysis.

## Skills

- `coverage-mapper` — auto-triggers when you ask about test coverage vs. a spec.

## Agents

- `traceability-agent` — read-only repo scanner for the test inventory.

## Example

> /coverage-gaps ./docs/user-stories.md
```

---

## Step 8 — Test the plugin locally

You don't need to publish to try it. Load it from disk:

1. **Validate the manifest** — confirm `plugin.json` is valid JSON (no trailing commas).
2. **Install from local path** using the plugin marketplace/CLI flow:
   - Run `/plugin` in Claude Code to open the plugin manager, **or**
   - Add a local marketplace pointing at your `plugins/` folder, then install.
3. **Verify it loaded** — type `/` and confirm `/coverage-gaps` appears in the list.
4. **Smoke test the command:**
   ```
   /coverage-gaps ./docs/user-stories.md
   ```
5. **Smoke test the skill** — without typing the command, ask:
   > "Are my user stories in docs/ covered by tests?"
   > Confirm Claude pulls in `coverage-mapper`.

---

## Step 9 — Iterate

- Tighten the skill `description` with real trigger phrases users say — this drives auto-activation accuracy.
- Add `evals/` scenarios (input → expected behavior) to measure quality.
- Bump `version` in `plugin.json` on each meaningful change.

---

## Step 10 — (Optional) Package as a marketplace

To share the plugin, create a marketplace manifest (`.claude-plugin/marketplace.json` in a parent repo) that lists your plugin(s), push to GitHub, and others install via that repo URL. This is the distribution step — not needed for personal practice.

---

## Recap checklist

- [ ] `.claude-plugin/plugin.json` — valid manifest
- [ ] `commands/coverage-gaps.md` — user-invoked command
- [ ] `skills/coverage-mapper/SKILL.md` — model-invoked skill with strong description
- [ ] `agents/traceability-agent.md` — read-only repo scanner
- [ ] `scripts/Find-TestFiles.ps1` — optional deterministic discovery
- [ ] `README.md` — human-facing summary
- [ ] Loaded locally and smoke-tested both command and skill

Build each file by hand, load it, break it, fix it — that's the practice loop. Once this plugin works, the same skeleton (manifest + commands + skills + agents + hooks) builds any plugin.

```

```
