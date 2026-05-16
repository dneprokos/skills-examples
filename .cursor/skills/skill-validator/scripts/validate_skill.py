#!/usr/bin/env python3
"""
validate_skill.py — Structural and security validation for skill folders.

Usage:
    python validate_skill.py <skill-dir> [<skill-dir> ...]

Exit codes:
    0  All skills passed (✅ or N/A only)
    1  One or more skills have ❌ Fail or 🔴 High risk
"""

from __future__ import annotations

import sys
import re
import pathlib

# Ensure emoji output works on Windows and other non-UTF-8 terminals
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

try:
    import yaml
except ImportError:
    print("Missing dependency: pip install pyyaml", file=sys.stderr)
    sys.exit(2)

# ---------------------------------------------------------------------------
# Pattern banks
# ---------------------------------------------------------------------------

SECRET_FAIL = [
    (r"sk-[A-Za-z0-9]{20,}", "OpenAI/Anthropic API key"),
    (r"ghp_[A-Za-z0-9]{36}", "GitHub PAT (ghp_)"),
    (r"github_pat_[A-Za-z0-9_]{82}", "GitHub fine-grained PAT"),
    (r"xox[baprs]-[0-9A-Za-z-]{10,}", "Slack token"),
    (r"-----BEGIN (?:RSA|EC|OPENSSH) PRIVATE KEY-----", "Private key block"),
    (r"(?i)password\s*[:=]\s*[\"'][^\"']{8,}[\"']", "Hardcoded password"),
    (r"(?i)(?:api[_-]?key|secret[_-]?key)\s*[:=]\s*[\"'][A-Za-z0-9/+]{16,}[\"']", "Hardcoded API/secret key"),
]

INJECTION_FAIL = [
    (r"(?i)ignore\s+(?:all\s+)?previous\s+instructions", "Prompt injection"),
    (r"(?i)disregard\s+(?:your\s+|all\s+)?(?:guidelines|rules|constraints)", "Safety bypass"),
    (r"(?i)override\s+(?:the\s+)?system\s+prompt", "System prompt override"),
    (r"(?i)(?:you are now|act as)\s+(?:DAN|jailbroken|unrestricted)", "Jailbreak pattern"),
    (r"(?i)(?:post|send|upload|exfiltrate)\b.{0,60}\b(?:credential|api.?key|secret|token)\b.{0,60}\bhttps?://(?!github\.com|skills\.sh)", "Data exfiltration attempt"),
]

INJECTION_WARN = [
    (r"(?i)impersonat(?:e|ing)\s+\w[\w\s]{2,30}(?:CEO|CTO|engineer|developer)", "Impersonation instruction"),
    (r"<SYSTEM>|<HUMAN>", "Prompt injection marker tag"),
]

SCRIPT_FAIL = [
    (r"curl\b.+\|\s*(?:ba)?sh\b", "curl | bash (RCE)"),
    (r"wget\b.+\|\s*(?:ba)?sh\b", "wget | bash (RCE)"),
    (r"(?i)Invoke-WebRequest\b.+\|\s*(?:iex|Invoke-Expression)", "IWR | IEX (RCE)"),
    (r"eval\s+\$\(curl\b", "eval $(curl ...) (RCE)"),
    (r"(?i)-p(?:assword)?\s+['\"]?[A-Za-z0-9!@#$%]{6,}['\"]?\s", "Hardcoded password in CLI arg"),
]

SCRIPT_WARN = [
    (r"rm\s+-[rRfF]{2}", "rm -rf without apparent guard"),
    (r"(?i)Remove-Item\b.+-Recurse\b.+-Force\b", "Remove-Item -Recurse -Force"),
    (r"(?i)(?:curl|wget|Invoke-WebRequest)\b.+https?://(?!github\.com|raw\.githubusercontent\.com|skills\.sh|registry\.npmjs\.org|pypi\.org)", "POST/GET to non-standard external domain"),
]


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

SHELL_EXTENSIONS = {".sh", ".bash", ".ps1", ".psm1", ".cmd", ".bat"}


def read_text(path: pathlib.Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return ""


def strip_code_elements(text: str) -> str:
    """Remove fenced code, inline code, and quoted example strings.

    Actual malicious instructions appear as plain directives, not wrapped in
    fences or quotation marks. Stripping these eliminates false positives from
    skills that document bad-pattern examples (like this validator itself).
    """
    text = re.sub(r"```[\s\S]*?```", "", text)      # fenced code blocks
    text = re.sub(r"`[^`\n]{1,200}`", "", text)      # inline code
    text = re.sub(r'"[^"\n]{1,120}"', "", text)      # double-quoted example strings
    return text


def scan(text: str, patterns: list[tuple]) -> list[str]:
    findings = []
    for pattern, label in patterns:
        if re.search(pattern, text, re.MULTILINE):
            findings.append(label)
    return findings


def parse_frontmatter(text: str):
    """Return (dict, error_string). error_string is None on success."""
    if not text.startswith("---"):
        return None, "No YAML frontmatter block found"
    try:
        end = text.index("---", 3)
    except ValueError:
        return None, "Frontmatter block not closed (missing closing ---)"
    try:
        data = yaml.safe_load(text[3:end])
        return data or {}, None
    except yaml.YAMLError as exc:
        return None, f"Invalid YAML: {exc}"


# ---------------------------------------------------------------------------
# The five checks
# ---------------------------------------------------------------------------

def check_structure(skill_path: pathlib.Path, skill_name: str):
    skill_md = skill_path / "SKILL.md"
    if not skill_md.exists():
        return "❌", ["SKILL.md not found"]

    text = read_text(skill_md)
    fm, err = parse_frontmatter(text)
    if err:
        return "❌", [err]

    findings = []
    if "name" not in fm:
        findings.append("Missing required field: `name`")
    elif str(fm["name"]) != skill_name:
        findings.append(f"`name` is `{fm['name']}` but directory is `{skill_name}`")

    if "description" not in fm or not str(fm.get("description", "")).strip():
        findings.append("Missing or empty `description`")

    return ("❌", findings) if findings else ("✅", [])


def check_content(skill_path: pathlib.Path):
    skill_md = skill_path / "SKILL.md"
    # Strip code/quoted examples so documented bad patterns don't self-trigger
    text = strip_code_elements(read_text(skill_md))

    fails = scan(text, INJECTION_FAIL)
    warns = scan(text, INJECTION_WARN)

    if fails:
        return "❌", [f"**{f}**" for f in fails] + warns
    if warns:
        return "⚠️", warns
    return "✅", []


def check_scripts(skill_path: pathlib.Path):
    scripts_dir = skill_path / "scripts"
    if not scripts_dir.exists():
        return "✅ N/A", []

    all_fails, all_warns = [], []
    for f in scripts_dir.rglob("*"):
        if not f.is_file():
            continue
        rel = f.relative_to(skill_path)
        # Shell-safety patterns only apply to shell/PowerShell files, not Python/JS/etc.
        if f.suffix.lower() in SHELL_EXTENSIONS:
            text = read_text(f)
            for label in scan(text, SCRIPT_FAIL):
                all_fails.append(f"`{rel}`: {label}")
            for label in scan(text, SCRIPT_WARN):
                all_warns.append(f"`{rel}`: {label}")

    if all_fails:
        return "❌", all_fails + all_warns
    if all_warns:
        return "⚠️", all_warns
    return "✅", []


def check_secrets(skill_path: pathlib.Path):
    findings_fail, findings_warn = [], []

    # Documentation directories contain intentional examples of bad patterns
    DOC_DIRS = {"references", "rules", "templates", "docs", "assets", "evals"}

    for f in skill_path.rglob("*"):
        if not f.is_file():
            continue
        rel = str(f.relative_to(skill_path))
        parts = set(pathlib.Path(rel).parts[:-1])  # parent directory names

        # Skip files inside documentation subdirectories
        if parts & DOC_DIRS:
            continue

        # Skip example/template files — they document format, not real values
        if re.search(r"(?i)(\.example\.|example\.|template)", rel):
            continue

        # Warn about local credential files
        if re.search(r"(?i)\.local\.(json|yaml|yml|env|cfg|ini)$", rel):
            findings_warn.append(f"`{rel}` — local credential file; ensure it is gitignored")
            continue

        text = read_text(f)
        for label in scan(text, SECRET_FAIL):
            findings_fail.append(f"`{rel}`: {label}")

    if findings_fail:
        return "❌", findings_fail + findings_warn
    if findings_warn:
        return "⚠️", findings_warn
    return "✅", []


def check_permissions(skill_path: pathlib.Path):
    skill_md = skill_path / "SKILL.md"
    text = read_text(skill_md)
    fm, err = parse_frontmatter(text)
    if err or not fm or "tools" not in fm:
        return "✅ N/A", []

    tools = fm["tools"]
    if not isinstance(tools, list):
        return "⚠️", ["`tools` field is not a list"]

    body_start = text.find("---", 3)
    body = text[body_start + 3:] if body_start != -1 else text

    findings = []
    for tool in tools:
        t = str(tool)
        if t in ("*", "all"):
            findings.append(f"Wildcard `{t}` in tools — consider listing specific tools")
        elif t.lower() not in body.lower():
            findings.append(f"`{t}` listed in `tools` but not referenced in body")

    return ("⚠️", findings) if findings else ("✅", [])


# ---------------------------------------------------------------------------
# Risk level
# ---------------------------------------------------------------------------

def risk_level(results: dict) -> str:
    statuses = [v["status"] for v in results.values()]
    if any("❌" in s for s in statuses):
        return "🔴 High"
    warn_count = sum(1 for s in statuses if "⚠️" in s)
    if warn_count >= 3:
        return "🔴 High"
    if warn_count >= 1:
        return "🟡 Medium"
    return "🟢 Low"


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def validate(skill_dir: str) -> dict:
    skill_path = pathlib.Path(skill_dir).resolve()
    skill_name = skill_path.name

    structure_s, structure_f = check_structure(skill_path, skill_name)
    content_s,   content_f   = check_content(skill_path)
    scripts_s,   scripts_f   = check_scripts(skill_path)
    secrets_s,   secrets_f   = check_secrets(skill_path)
    perms_s,     perms_f     = check_permissions(skill_path)

    results = {
        "structure":   {"status": structure_s, "findings": structure_f},
        "content":     {"status": content_s,   "findings": content_f},
        "scripts":     {"status": scripts_s,   "findings": scripts_f},
        "secrets":     {"status": secrets_s,   "findings": secrets_f},
        "permissions": {"status": perms_s,     "findings": perms_f},
    }
    results["risk"]  = risk_level(results)
    results["name"]  = skill_name
    return results


def short_status(s: str) -> str:
    if "❌" in s: return "❌"
    if "⚠️" in s: return "⚠️"
    if "N/A" in s: return "N/A"
    return "✅"


def main(skill_dirs: list[str]) -> int:
    if not skill_dirs:
        print("Usage: validate_skill.py <skill-dir> [<skill-dir> ...]")
        return 2

    all_results = [validate(d) for d in skill_dirs]
    today = __import__("datetime").date.today().isoformat()

    # --- Summary table ---
    print(f"\n## Skills Security Validation Report")
    print(f"Checked: {len(all_results)} skill(s)  |  Date: {today}\n")
    print("| Skill | Structure | Content | Scripts | Secrets | Permissions | Risk |")
    print("|-------|:---------:|:-------:|:-------:|:-------:|:-----------:|:----:|")
    for r in all_results:
        row = (
            f"| {r['name']} "
            f"| {short_status(r['structure']['status'])} "
            f"| {short_status(r['content']['status'])} "
            f"| {short_status(r['scripts']['status'])} "
            f"| {short_status(r['secrets']['status'])} "
            f"| {short_status(r['permissions']['status'])} "
            f"| {r['risk']} |"
        )
        print(row)

    # --- Findings ---
    findings_printed = False
    for r in all_results:
        for check, data in r.items():
            if check in ("name", "risk"):
                continue
            if data["findings"]:
                if not findings_printed:
                    print("\n## Findings\n")
                    findings_printed = True
                icon = data["status"].split()[0]
                print(f"### {r['name']} — {check.capitalize()} {icon}")
                for f in data["findings"]:
                    print(f"- {f}")
                print()

    if not findings_printed:
        print("\n✅ All skills passed security validation — no issues found.")

    # Machine-readable summary line consumed by CI steps
    high   = sum(1 for r in all_results if "🔴" in r["risk"])
    medium = sum(1 for r in all_results if "🟡" in r["risk"])
    low    = sum(1 for r in all_results if "🟢" in r["risk"])
    print(f"\nSTAT:checked={len(all_results)},high={high},medium={medium},low={low}")

    # Compact findings list for Slack (one entry per failing check)
    slack_items: list[str] = []
    for r in all_results:
        for check, data in r.items():
            if check in ("name", "risk") or not data["findings"]:
                continue
            icon = ":red_circle:" if "❌" in data["status"] else ":large_yellow_circle:"
            slack_items.append(f"{icon} *{r['name']}* — {check}")
    if slack_items:
        print(f"FINDINGS:{' | '.join(slack_items)}")

    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
