# Git PR Creator

A GitHub Copilot skill for creating a pull request from the current branch to `main`.

## What it does

- detects the current local branch
- blocks PR creation from `main`
- keeps the same local and remote branch name
- generates a PR title from a ticket prefix, branch suffix, or commit changes
- checks for an existing PR with the same ticket prefix before continuing

## GitHub token (required for real PR runs)

Creating a PR **without** `-DryRun` requires a GitHub personal access token. The helper resolves it in this order:

1. **`GITHUB_TOKEN`** or **`GH_TOKEN`** in the environment (first non-empty wins between the two env checks; both are accepted).
2. Otherwise, **`.github/skills/git-pr-creator/config/github-pr.local.json`** with a **`github_token`** string.

The script sets **`GH_TOKEN`** for the GitHub CLI from that value. Do **not** print or log the token.

### Config file setup

1. Copy the committed example to the **ignored** local file (same directory):

   - From: `config/github-pr.local.example.json`
   - To: `config/github-pr.local.json`

2. Replace the placeholder with your real token.

**Committed example** (`github-pr.local.example.json` — safe to commit, no secrets):

```json
{
  "github_token": "PASTE_TOKEN_HERE"
}
```

**Local file** (`github-pr.local.json` — **never commit**; listed in the repo root `.gitignore`):

```json
{
  "github_token": "ghp_xxxxxxxxxxxxxxxxxxxx"
}
```

If this file is ever pushed or leaked, **revoke** the token immediately in GitHub (**Settings → Developer settings → Personal access tokens**) and create a new one. Prefer a **fine-grained** token limited to this repository when possible.

### Where to create a token

1. Open GitHub in a browser: **Settings** (profile) → **Developer settings** → **Personal access tokens**.
2. Use either:
   - **Fine-grained token**: select the repository; grant permissions needed for pull requests (e.g. **Pull requests** read/write, **Contents** read as required by your org).
   - **Classic token**: for private repos, the **`repo`** scope is typically required for `gh pr create` / `gh pr list`.

Official reference: [Managing your personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens).

### Optional: reuse an existing `gh` login

If you already ran `gh auth login`, you can copy the token once into `github-pr.local.json` or export it for the session (avoid storing it in shell history):

```powershell
gh auth token
```

Prefer the config file or a secret manager for anything long-lived.

## Suggested prompt

```text
Create a pull request from this branch using the git-pr-creator skill.
```

## Helper script

Preview only (no token required):

```powershell
pwsh -NoProfile -File ./.github/skills/git-pr-creator/scripts/create-pr.ps1 -DryRun
```

Create a PR (token required via env or `github-pr.local.json`):

```powershell
pwsh -NoProfile -File ./.github/skills/git-pr-creator/scripts/create-pr.ps1
```

Headless-friendly install flags (token still required):

```powershell
pwsh -NoProfile -File ./.github/skills/git-pr-creator/scripts/create-pr.ps1 -ApproveInstall -ApproveAuth
```

## Title examples

- `TST-2056_testBranch` → `[TST-2056]: added new git related skills`
- `2056_testBranch` → `[2056]: added new git related skills`
- `readme_and_git_skills` → `add readme and git skills`

## Notes

- The default base branch is `main`.
- If the remote branch does not exist yet, the helper can publish it using the same name.
- Duplicate ticket-prefix PRs require explicit user confirmation.
- The real config path is always **`.github/skills/git-pr-creator/config/`** under the repository root, even if you invoke a copy of the script from `.cursor/skills/`.
