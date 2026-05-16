"""Grade all 6 eval runs against their assertions and write grading.json files."""
import json
import os
import re

WORKSPACE = os.path.dirname(os.path.abspath(__file__))

EVALS = {
    "eval-1-freeform-announcement": {
        "assertions": [
            ("Output file slack-message.json is valid JSON",
             lambda j: (True, "Parsed successfully") if j else (False, "Could not parse")),
            ("Top-level key is 'blocks' and its value is an array",
             lambda j: (isinstance(j.get("blocks"), list), f"blocks={type(j.get('blocks')).__name__}")),
            ("Every block in the array has 'type' equal to 'markdown'",
             lambda j: (all(b.get("type") == "markdown" for b in j.get("blocks", [])),
                        f"types={[b.get('type') for b in j.get('blocks', [])]}")),
            ("Every block in the array has a non-empty 'text' field",
             lambda j: (all(b.get("text") for b in j.get("blocks", [])),
                        f"texts={[bool(b.get('text')) for b in j.get('blocks', [])]}")),
            ("No block contains image markdown syntax '![' anywhere in its text",
             lambda j: (not any("![" in b.get("text", "") for b in j.get("blocks", [])),
                        "No image syntax found" if not any("![" in b.get("text", "") for b in j.get("blocks", [])) else "Found ![" )),
            ("The text mentions 'v2.5' or 'version 2.5' preserving the version number",
             lambda j: (any(("v2.5" in b.get("text", "") or "version 2.5" in b.get("text", "").lower()) for b in j.get("blocks", [])),
                        "Checked for v2.5")),
            ("The text mentions the analytics dashboard",
             lambda j: (any("dashboard" in b.get("text", "").lower() for b in j.get("blocks", [])),
                        "Checked for 'dashboard'")),
            ("The text mentions the login bug fix",
             lambda j: (any("login" in b.get("text", "").lower() for b in j.get("blocks", [])),
                        "Checked for 'login'")),
            ("The text mentions the legacy API or v1 API removal",
             lambda j: (any(("legacy" in b.get("text", "").lower() or "/v1" in b.get("text", "")) for b in j.get("blocks", [])),
                        "Checked for 'legacy' or '/v1'")),
            ("No single block's text field exceeds 12000 characters",
             lambda j: (all(len(b.get("text", "")) <= 12000 for b in j.get("blocks", [])),
                        f"max chars={max((len(b.get('text','')) for b in j.get('blocks',[])), default=0)}")),
        ]
    },
    "eval-2-standard-markdown-conversion": {
        "assertions": [
            ("Output file slack-message.json is valid JSON",
             lambda j: (True, "Parsed successfully") if j else (False, "Could not parse")),
            ("Top-level key is 'blocks' and its value is an array",
             lambda j: (isinstance(j.get("blocks"), list), f"blocks={type(j.get('blocks')).__name__}")),
            ("Every block in the array has 'type' equal to 'markdown'",
             lambda j: (all(b.get("type") == "markdown" for b in j.get("blocks", [])),
                        f"types={[b.get('type') for b in j.get('blocks', [])]}")),
            ("Every block in the array has a non-empty 'text' field",
             lambda j: (all(b.get("text") for b in j.get("blocks", [])),
                        f"texts={[bool(b.get('text')) for b in j.get('blocks', [])]}")),
            ("No block text contains the pattern '![' (image embed syntax)",
             lambda j: (not any("![" in b.get("text", "") for b in j.get("blocks", [])),
                        "No image syntax found" if not any("![" in b.get("text", "") for b in j.get("blocks", [])) else "Found ![" )),
            ("The converted image URL 'cdn.example.com/images/phoenix-banner.png' appears as a plain link or is referenced in the output",
             lambda j: (any("cdn.example.com/images/phoenix-banner.png" in b.get("text", "") for b in j.get("blocks", [])),
                        "Checked for cdn.example.com URL")),
            ("The table with Issue/Severity/Fixed columns is present in at least one block's text",
             lambda j: (any(("Severity" in b.get("text", "") or "severity" in b.get("text", "")) for b in j.get("blocks", [])),
                        "Checked for table column 'Severity'")),
            ("The JavaScript code block (getReport) is present in at least one block's text",
             lambda j: (any("getReport" in b.get("text", "") for b in j.get("blocks", [])),
                        "Checked for 'getReport'")),
            ("The blockquote about backing up configuration files is present",
             lambda j: (any(("backup" in b.get("text", "").lower() or "back up" in b.get("text", "").lower() or "configuration" in b.get("text", "").lower()) for b in j.get("blocks", [])),
                        "Checked for backup/configuration mention")),
            ("No single block's text field exceeds 12000 characters",
             lambda j: (all(len(b.get("text", "")) <= 12000 for b in j.get("blocks", [])),
                        f"max chars={max((len(b.get('text','')) for b in j.get('blocks',[])), default=0)}")),
        ]
    },
    "eval-3-structured-status-update": {
        "assertions": [
            ("Output file slack-message.json is valid JSON",
             lambda j: (True, "Parsed successfully") if j else (False, "Could not parse")),
            ("Top-level key is 'blocks' and its value is an array",
             lambda j: (isinstance(j.get("blocks"), list), f"blocks={type(j.get('blocks')).__name__}")),
            ("Every block in the array has 'type' equal to 'markdown'",
             lambda j: (all(b.get("type") == "markdown" for b in j.get("blocks", [])),
                        f"types={[b.get('type') for b in j.get('blocks', [])]}")),
            ("Every block in the array has a non-empty 'text' field",
             lambda j: (all(b.get("text") for b in j.get("blocks", [])),
                        f"texts={[bool(b.get('text')) for b in j.get('blocks', [])]}")),
            ("No block contains image markdown syntax '![' anywhere in its text",
             lambda j: (not any("![" in b.get("text", "") for b in j.get("blocks", [])),
                        "No image syntax found" if not any("![" in b.get("text", "") for b in j.get("blocks", [])) else "Found ![" )),
            ("The project name 'Orion Data Pipeline' appears in the output",
             lambda j: (any("Orion Data Pipeline" in b.get("text", "") for b in j.get("blocks", [])),
                        "Checked for 'Orion Data Pipeline'")),
            ("The owner 'Sarah Chen' is mentioned",
             lambda j: (any("Sarah Chen" in b.get("text", "") for b in j.get("blocks", [])),
                        "Checked for 'Sarah Chen'")),
            ("The IT ticket reference 'IT-4482' is preserved",
             lambda j: (any("IT-4482" in b.get("text", "") for b in j.get("blocks", [])),
                        "Checked for 'IT-4482'")),
            ("The status 'At Risk' is present in the output",
             lambda j: (any("At Risk" in b.get("text", "") or "at risk" in b.get("text", "").lower() for b in j.get("blocks", [])),
                        "Checked for 'At Risk'")),
            ("No single block's text field exceeds 12000 characters",
             lambda j: (all(len(b.get("text", "")) <= 12000 for b in j.get("blocks", [])),
                        f"max chars={max((len(b.get('text','')) for b in j.get('blocks',[])), default=0)}")),
        ]
    }
}

CONFIGS = ["with_skill", "without_skill"]


def load_json(path):
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        return None


def grade_eval(eval_name, config):
    output_path = os.path.join(WORKSPACE, eval_name, config, "outputs", "slack-message.json")
    data = load_json(output_path)

    assertions_config = EVALS[eval_name]["assertions"]
    results = []
    passed = 0

    if data is None:
        for text, _ in assertions_config:
            results.append({"text": text, "passed": False, "evidence": f"Could not load {output_path}"})
    else:
        for text, check_fn in assertions_config:
            try:
                ok, evidence = check_fn(data)
            except Exception as e:
                ok, evidence = False, f"Error: {e}"
            results.append({"text": text, "passed": ok, "evidence": str(evidence)})
            if ok:
                passed += 1

    total = len(assertions_config)
    grading = {
        "expectations": results,
        "summary": {
            "passed": passed,
            "failed": total - passed,
            "total": total,
            "pass_rate": round(passed / total, 2) if total else 0
        }
    }
    grading_path = os.path.join(WORKSPACE, eval_name, config, "grading.json")
    with open(grading_path, "w", encoding="utf-8") as f:
        json.dump(grading, f, indent=2)
    print(f"Graded {eval_name}/{config}: {passed}/{total} ({grading['summary']['pass_rate']*100:.0f}%)")
    return grading


all_results = {}
for eval_name in EVALS:
    all_results[eval_name] = {}
    for config in CONFIGS:
        all_results[eval_name][config] = grade_eval(eval_name, config)

print("\n=== Summary ===")
for eval_name in EVALS:
    for config in CONFIGS:
        s = all_results[eval_name][config]["summary"]
        print(f"  {eval_name}/{config}: {s['passed']}/{s['total']} ({s['pass_rate']*100:.0f}%)")
