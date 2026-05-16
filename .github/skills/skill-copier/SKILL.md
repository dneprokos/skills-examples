---
name: skill-copier
description: >-
  Copy or sync skills between the .claude/skills, .cursor/skills, and .github/skills
  folders in the current repository. Use this skill whenever the user wants to copy
  skills between tool folders, sync skill directories, mirror skills, keep skills in
  sync across tools, or says things like "copy skills to cursor", "sync github skills
  to claude", "mirror skills", "copy skills from .github to .claude", "propagate skills",
  or asks to copy/move skills from one AI tool folder to another.
tools: [read, edit, run_command]
---

# Skill Copier

Copies skills from one tool folder to another within the same repository.

## Supported folders

| Key      | Path              |
|----------|-------------------|
| `.claude` | `.claude/skills/` |
| `.cursor` | `.cursor/skills/` |
| `.github` | `.github/skills/` |

## Workflow

### Step 1 — Identify source

Check whether the user already stated the source folder in their message (e.g. "copy from .github").
If not, ask:

> "Which folder do you want to copy skills **from**?"
> 1. `.claude/skills`
> 2. `.cursor/skills`
> 3. `.github/skills`

### Step 2 — Identify destination

Check whether the user already stated the destination. If not, ask:

> "Which folder do you want to copy skills **to**?" (list remaining options, excluding the source)

### Step 3 — Handle overwrite preference

Ask whether to overwrite skills that already exist in the destination, or skip them:

> "Skills that already exist in the destination will be **skipped** by default. Do you want to overwrite them instead?"

Default: skip existing (do not overwrite).

### Step 4 — Run the copy script

Run the PowerShell helper from the repository root:

```powershell
.github/skills/skill-copier/scripts/Copy-Skills.ps1 `
  -Source "<source-key>" `
  -Destination "<destination-key>" `
  [-Overwrite]
```

Where `<source-key>` and `<destination-key>` are one of: `.claude`, `.cursor`, `.github`.
Add `-Overwrite` only when the user confirmed they want to replace existing skills.

### Step 5 — Report results

After the script finishes, summarise to the user:
- How many skills were copied
- How many were skipped (already existed)
- Any errors

## Edge cases

- If source and destination are the same, stop and tell the user to pick two different folders.
- If the source folder doesn't exist or is empty, tell the user and stop.
- If the destination folder doesn't exist, the script creates it automatically.
