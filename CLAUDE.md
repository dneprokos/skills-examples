# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repository is

A collection of reusable GitHub Copilot skills (and Cursor Agent Skills). Each skill is a self-contained folder with a `SKILL.md` at its root. There is no build system, package manager, or test runner — skills are pure Markdown workflows with optional helper scripts.

## Skill locations

| Path | Purpose |
|---|---|
| `.github/skills/` | Canonical skill definitions (GitHub Copilot) |
| `.cursor/skills/` | Manual mirror of the same skills for Cursor Agent Skills |
| `.agents/skills/` | External skills pulled via `skills-lock.json` |
| `.github/agents/` | Orchestrator agents that coordinate multiple skills |

**When you add or modify a skill, update both `.github/skills/` and `.cursor/skills/`.** They must stay in sync. Known gaps in the Cursor mirror: `ut-architect` has no `evals/` folder; some `ut-coder` language-example reference files may be missing.

## SKILL.md format

Every skill starts with YAML frontmatter:

```yaml
---
name: skill-id
description: >-
  One-sentence summary. Trigger phrases that activate this skill.
argument-hint: "optional hint shown to the user"
tools: [read, search, edit]   # only if specific tools are required
---
```

The body contains the workflow: when to use it, step-by-step instructions, hard rules, and examples. Keep it markdown-only — no code execution, no MCP dependency (except `jira-mcp-assistant`).

## Typical skill layout

```
.github/skills/{skill-name}/
├── SKILL.md          # required — agent instructions
├── README.md         # optional — human-facing summary and example prompts
├── references/       # optional — supporting .md guidance files
├── scripts/          # optional — PowerShell helper scripts
├── templates/        # optional — output templates
├── config/           # optional — configuration files
└── evals/            # optional — evaluation scenarios
```

## Unit test pipeline architecture

The `ut-analyst`, `ut-architect`, and `ut-coder` skills form a strict three-phase pipeline coordinated by `.github/agents/unit-test-generator.agent.md`:

- **Phase 1 — Analyst** (`ut-analyst`): classifies dependencies, detects non-determinism, enumerates test cases using EP/BVA/DT/ST, emits a JSON test plan
- **Phase 2 — Architect** (`ut-architect`): assigns mock/real strategy per dependency, resolves assertion style, specifies non-determinism abstractions
- **Phase 3 — Coder** (`ut-coder`): generates the complete compilable test file (AAA pattern, parameterized tests, null-guards, mocks, setup/teardown)

**Hard rule:** never combine responsibilities across phases. The Analyst never generates code; the Coder never classifies dependencies.

Supported languages: C#, Java, Python, TypeScript. Language-specific examples live in `.github/skills/ut-coder/references/examples-{lang}.md`.

Shared reference files (`project-patterns.md`, `analyst-test-plan-schema.md`) are duplicated across skill folders. Each copy includes a **Sync** callout — update all copies together when the canonical changes.

## External skills (`skills-lock.json`)

`skills-lock.json` tracks remotely-sourced skills. Local skills (authored in this repo) are not listed there. External skills are stored under `.agents/skills/` after being pulled.

## Git workflow skills

The five git skills (`git-branch-creator`, `git-commit-creator`, `git-pr-creator`, `git-push-creator`, `git-workflow-orchestrator`) use PowerShell helper scripts under their `scripts/` folders. Scripts support `-PreviewOnly` / `-DryRun` flags. Commit messages follow [Conventional Commits](https://www.conventionalcommits.org/) format.

## Secrets and local config

Files that must never be committed:
- `github-pr.local.json` — GitHub API token for the pr-creator skill
- `.github/skills/jira-mcp-assistant/config/jira-defaults.local.json` — Jira credentials

Use the `.example.json` counterparts as templates.

## Contributing a new skill

1. Create `.github/skills/{skill-name}/SKILL.md` with correct YAML frontmatter.
2. Mirror the folder to `.cursor/skills/{skill-name}/`.
3. Keep the skill focused on one workflow domain.
4. If the skill coordinates other skills, create an agent under `.github/agents/` instead.
