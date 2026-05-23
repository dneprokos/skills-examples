# Copilot Skill Examples

[![License](https://img.shields.io/github/license/dneprokos/copilot-skill-examples?style=flat-square)](LICENSE)
[![Stars](https://img.shields.io/github/stars/dneprokos/copilot-skill-examples?style=flat-square)](https://github.com/dneprokos/copilot-skill-examples/stargazers)

Reusable agent skills you can copy into `.github/skills/`, `.cursor/skills/`, or `.claude/skills/` and adapt for your own repositories. The repo contains workflows, supporting templates, and helper scripts — no build system or package manager required.

![Reusable Copilot skills: modular SKILL.md workflows you copy into .github/skills](docs/assets/skills-hero.svg)

## Overview

Each skill targets a specific workflow and is activated by natural-language prompts:

| Skill                                                                                    | Purpose                                                                                                                                              | Contents                                 |
| ---------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------- |
| [`api-test-scenario-generator`](.github/skills/api-test-scenario-generator/)             | Generates structured REST API test scenarios with boundary and validation coverage                                                                   | `SKILL.md`, templates, config, script    |
| [`bug-report-formatter`](.github/skills/bug-report-formatter/)                           | Converts messy bug descriptions, stack traces, or error logs into a structured Jira-ready report; optionally creates a Jira ticket via Atlassian MCP | `SKILL.md`                               |
| [`dneprokos-medium-article-reviewer`](.github/skills/dneprokos-medium-article-reviewer/) | Section-by-section critique of a Medium article with actionable suggestions based on the author's established style                                  | `SKILL.md`, references                   |
| [`educational-resource-searcher`](.github/skills/educational-resource-searcher/)         | Finds top-rated tutorials, courses, and videos on any topic across YouTube, Udemy, Coursera, Pluralsight, and more                                   | `SKILL.md`                               |
| [`git-branch-creator`](.github/skills/git-branch-creator/)                               | Creates a new Git branch after verifying that `main` is ready and up to date                                                                         | `SKILL.md`, README, script               |
| [`git-commit-creator`](.github/skills/git-commit-creator/)                               | Creates a Conventional Commits message from staged changes                                                                                           | `SKILL.md`, README, references, script   |
| [`git-pr-creator`](.github/skills/git-pr-creator/)                                       | Creates a pull request from the current branch with ticket-style PR titles                                                                           | `SKILL.md`, README, references, script   |
| [`git-push-creator`](.github/skills/git-push-creator/)                                   | Pushes the current local branch to `origin`                                                                                                          | `SKILL.md`, README, script               |
| [`git-workflow-orchestrator`](.github/skills/git-workflow-orchestrator/)                 | Phased branch → commit → push → PR with per-phase status and PR URL                                                                                  | `SKILL.md`, script                       |
| [`jira-mcp-assistant`](.github/skills/jira-mcp-assistant/)                               | Jira Cloud JQL and backlog-style lists via Atlassian MCP (read-first; extend for writes)                                                             | `SKILL.md`, references                   |
| [`meeting-notes-summarizer`](.github/skills/meeting-notes-summarizer/)                   | Turns transcripts or messy notes into a Teams/email-ready structured recap                                                                           | `SKILL.md`, references                   |
| [`readme-polisher`](.github/skills/readme-polisher/)                                     | Drafts or upgrades a repository `README.md` using real project evidence                                                                              | `SKILL.md`, references, assets, script   |
| [`requirements-reviewer`](.github/skills/requirements-reviewer/)                         | Reviews requirements against 8 quality characteristics (clear, complete, consistent…) and produces a graded report                                   | `SKILL.md`, references                   |
| [`rest-api-design`](.github/skills/rest-api-design/)                                     | Designs and reviews REST APIs: paths, HTTP semantics, pagination, versioning, errors, OpenAPI                                                        | `SKILL.md`, README, references           |
| [`skill-copier`](.github/skills/skill-copier/)                                           | Copies or syncs skills between `.claude/skills/`, `.cursor/skills/`, and `.github/skills/`                                                           | `SKILL.md`, script                       |
| [`skill-creator`](.github/skills/skill-creator/)                                         | Creates, tests, and iteratively improves agent skills with eval runs and a results viewer                                                            | `SKILL.md`, agents, scripts, eval-viewer |
| [`slack-markdown-generator`](.github/skills/slack-markdown-generator/)                   | Converts any content into a Slack Block Kit JSON payload, handling the 12k-char limit and Slack-specific quirks                                      | `SKILL.md`                               |
| [`token-usage-reporting`](.github/skills/token-usage-reporting/)                         | Produces day/week/month token usage reports in table format                                                                                          | `SKILL.md`, config, template, script     |
| [`ut-analyst`](.github/skills/ut-analyst/)                                               | **Phase 1** — classifies dependencies, detects non-determinism, enumerates test cases using EP/BVA/DT/ST, produces JSON test plan                    | `SKILL.md`, README, references, evals    |
| [`ut-architect`](.github/skills/ut-architect/)                                           | **Phase 2** — assigns mock/real strategy per dependency, resolves assertion style, specifies non-determinism abstractions                            | `SKILL.md`, README, references, evals    |
| [`ut-coder`](.github/skills/ut-coder/)                                                   | **Phase 3** — generates the complete, compilable test file: AAA pattern, parameterized tests, mocks, null-guards, setup/teardown                     | `SKILL.md`, README, references, evals    |
| [`windows-secretmanagement-setup`](.github/skills/windows-secretmanagement-setup/)       | Installs and configures Windows SecretManagement + SecretStore for PowerShell credential storage (bootstraps `GitHubToken` for PR skills)            | `SKILL.md`                               |

## Unit Test Generator Agent

The three `ut-*` skills are coordinated by a dedicated agent: [`.github/agents/unit-test-generator.agent.md`](.github/agents/unit-test-generator.agent.md).

The agent enforces a strict **Analyst → Architect → Coder** pipeline where responsibilities are never combined across phases:

```
Source class
     │
     ▼
Phase 1 — Analyst    → JSON test plan  (dependencies, test cases, null-guards, non-determinism)
     │
     ▼
Phase 2 — Architect  → Strategy summary (mock/real assignments, assertion style, abstractions)
     │
     ▼
Phase 3 — Coder      → Complete, compilable test file
```

**Usage:** Open a source file in the editor, then invoke the agent:

```text
@unit-test-generator generate tests for MyService
@unit-test-generator generate tests for the open file, skipReview: true
```

Each skill can also be used **standalone** via slash commands (`/ut-analyst`, `/ut-architect`, `/ut-coder`) when you want to run only one phase or inspect intermediate outputs.

## Getting Started

1. Clone this repository and open it in VS Code or Cursor.
2. Browse the skill folders under `.github/skills/`.
3. Copy the skill you want into your own project's `.github/skills/` (Copilot), `.cursor/skills/` (Cursor), or `.claude/skills/` (Claude Code) directory.
4. Prompt the agent with a request that matches the skill's domain.

### Clone locally

```bash
git clone https://github.com/dneprokos/copilot-skill-examples.git
cd copilot-skill-examples
```

### Example prompts

```text
Improve this repository README using the readme-polisher skill.
Generate API test scenarios for POST /api/users.
Review these REST endpoints using the rest-api-design skill (paste OpenAPI or routes).
@unit-test-generator generate tests for MyService
@unit-test-generator generate tests for the open file, skipReview: true
/ut-analyst analyze MyService
/ut-architect [paste Analyst JSON]
/ut-coder [paste Analyst JSON and Architect strategy]
Create a new branch named feature/add-login-flow.
Commit the current branch using the git-commit-creator skill.
Push the current branch using the git-push-creator skill.
Create a pull request from this branch using the git-pr-creator skill.
Run the git-workflow-orchestrator to ship my branch (branch, commit, push, PR).
Create a token usage report for this week.
Summarize these meeting notes using the meeting-notes-summarizer skill (paste notes below).
List Jira backlog issues for project SCRUM using the jira-mcp-assistant skill.
Copy skills from .github to .claude using the skill-copier skill.
Help me draft and evaluate a new agent skill using the skill-creator skill.
Format this bug report for Jira.
Review my requirements document.
Find top Python courses on Udemy.
Format this status update for Slack.
```

> Exact invocation style varies by tool surface (Copilot, Cursor, Claude Code), but natural-language prompts work well across all of them.

## Skill Mirrors

This repository maintains the same skill set under three locations:

| Location          | Tool                              |
| ----------------- | --------------------------------- |
| `.github/skills/` | GitHub Copilot (canonical source) |
| `.cursor/skills/` | Cursor Agent Skills               |
| `.claude/skills/` | Claude Code                       |

**Keep all three in sync when you add or modify a skill.** Use the [`skill-copier`](.github/skills/skill-copier/) skill to copy skills between folders automatically:

```text
Copy skills from .github to .claude
Copy skills from .github to .cursor, overwrite existing
```

The `skill-copier` skill runs `.github/skills/skill-copier/scripts/Copy-Skills.ps1` under the hood and reports how many were copied, skipped, or failed.

Known gaps in the Cursor and Claude mirrors:

- **`ut-architect`** — `.cursor/skills/ut-architect/` has no `evals/` folder.
- **Project-patterns templates** — `project-patterns-java-example.md`, `project-patterns-python-example.md`, and `project-patterns-typescript-example.md` exist under `.github/skills/ut-coder/references/` but may not be present in all mirrors. Copy them if needed.

Shared reference files (`project-patterns.md`, `analyst-test-plan-schema.md`) are replicated across skill folders. Each copy includes a **Sync** callout — update all copies together.

## Jira Skills and Atlassian MCP

The [`jira-mcp-assistant`](.github/skills/jira-mcp-assistant/) and [`bug-report-formatter`](.github/skills/bug-report-formatter/) skills can create Jira issues via the Atlassian MCP. The `jira-mcp-assistant` skill is read-first: resolve `cloudId`, run JQL through the MCP (e.g. `searchJiraIssuesUsingJql`), paginate, and format results.

You still need to connect Cursor (or another client) to the [Atlassian Rovo MCP Server](https://support.atlassian.com/rovo/docs/setting-up-ides/) and authenticate (OAuth or API token).

**How to extend `jira-mcp-assistant` without renaming it:**

1. Keep the umbrella id `jira-mcp-assistant` so existing prompts keep working.
2. Widen the YAML `description` with new trigger phrases (e.g. "create Jira issue", "dashboard filter").
3. Add workflow sections to `SKILL.md` for new flows (create issue, transition, comments).
4. Split large sections into `references/` files when `SKILL.md` grows long.
5. Add a **separate skill** only for large or high-risk flows (e.g. release approvals) that should not share triggers with everyday queries.

## Token Prediction Demo

[`token_prediction_example.py`](token_prediction_example.py) is a small standalone script that demonstrates how a language model predicts tokens one at a time. It streams Claude's response and prints each token delta as it arrives — a concrete illustration of how the model builds output incrementally rather than "thinking" the full answer first.

### Setup

```bash
pip install anthropic python-dotenv
cp .env.example .env
# open .env and fill in your ANTHROPIC_API_KEY
```

Get an API key at [console.anthropic.com](https://console.anthropic.com) → **API Keys**.

> `.env` is listed in `.gitignore` — it will not be committed.

### Run

```bash
python token_prediction_example.py
```

The script opens an interactive REPL. Type any prompt and press Enter to watch Claude predict tokens live. Each printed chunk is one streaming delta from the API. The session ends with a summary of streaming deltas received, output tokens (as counted by the API), input tokens, elapsed time, and approximate tokens per second.

```
You: Explain recursion in one sentence.

Tokens arriving (each character group is one predicted token):

Recursion is a programming technique where a function calls itself...

============================================================
Streaming deltas received : 32
Output tokens (API count) : 28
Input tokens              : 15
Wall-clock time           : 1.43s
Approx tokens/sec         : 19.6
```

Type `quit` or press Ctrl+C to exit.

## Typical Skill Layout

```text
.github/skills/{skill-name}/
├── SKILL.md          # required — agent instructions and YAML frontmatter
├── README.md         # optional — human-facing summary and example prompts
├── config/           # optional — configuration files
├── scripts/          # optional — PowerShell helper scripts
├── templates/        # optional — output templates
└── references/       # optional — supporting guidance files
```

## Repository Map

```text
copilot-skill-examples/
├── docs/
│   └── assets/
│       └── skills-hero.svg
├── .github/
│   ├── agents/
│   │   └── unit-test-generator.agent.md  # Orchestrates the ut-* pipeline
│   └── skills/
│       ├── api-test-scenario-generator/
│       ├── bug-report-formatter/
│       ├── dneprokos-medium-article-reviewer/
│       ├── educational-resource-searcher/
│       ├── git-branch-creator/
│       ├── git-commit-creator/
│       ├── git-pr-creator/
│       ├── git-push-creator/
│       ├── git-workflow-orchestrator/
│       ├── jira-mcp-assistant/
│       ├── meeting-notes-summarizer/
│       ├── readme-polisher/
│       ├── requirements-reviewer/
│       ├── rest-api-design/
│       ├── skill-copier/
│       ├── skill-creator/
│       ├── slack-markdown-generator/
│       ├── token-usage-reporting/
│       ├── ut-analyst/     # Phase 1: dependency analysis + test plan
│       ├── ut-architect/   # Phase 2: mocking strategy + structure
│       ├── ut-coder/       # Phase 3: test file generation
│       └── windows-secretmanagement-setup/
├── .cursor/
│   └── skills/    # Cursor Agent Skills mirror
├── .claude/
│   ├── settings.json          # Claude Code permissions (blocks .env reads)
│   └── skills/                # Claude Code mirror of the same skills
├── token_prediction_example.py  # Streaming token prediction demo
├── .env.example               # Template for ANTHROPIC_API_KEY
├── README.md
└── LICENSE
```

## Contributing

Contributions are welcome. If you add a new skill:

1. Create `.github/skills/{skill-name}/SKILL.md` with correct YAML frontmatter.
2. Mirror the folder to `.cursor/skills/{skill-name}/` and `.claude/skills/{skill-name}/`.
3. Keep the skill focused on one workflow domain.
4. If the skill coordinates other skills, create an agent under `.github/agents/` instead.

test

## License

Released under the MIT License. See [`LICENSE`](LICENSE) for details.
