import os
import sys
import json
from google import genai

api_key = os.getenv("GEMINI_API_KEY")
pr_number = int(os.getenv("PR_NUMBER"))
semgrep_config = os.getenv("SEMGREP_CONFIG", "auto")

diff_path = sys.argv[1] if len(sys.argv) > 1 else None
semgrep_path = sys.argv[2] if len(sys.argv) > 2 else None

diff_content = ""
if diff_path and os.path.exists(diff_path):
    with open(diff_path, "r", encoding="utf-8") as f:
        diff_content = f.read()

if len(diff_content) < 10:
    print("Diff missing or too small. Exiting.")
    sys.exit(0)

semgrep_json = {}
if semgrep_path and os.path.exists(semgrep_path):
    try:
        with open(semgrep_path, "r", encoding="utf-8") as f:
            semgrep_json = json.load(f)
    except:
        semgrep_json = {}

analysis_metadata = {
    "version": semgrep_json.get("version"),
    "configs": semgrep_json.get("configs"),
    "rules": semgrep_json.get("rules"),
    "paths_scanned": semgrep_json.get("paths", {}).get("scanned"),
    "errors": semgrep_json.get("errors"),
    "total_findings": len(semgrep_json.get("results", [])),
}

os.makedirs("analysis_output", exist_ok=True)
with open("analysis_output/semgrep_metadata.json", "w", encoding="utf-8") as f:
    json.dump(analysis_metadata, f, indent=2)

def load_repo_context_dynamic(root=".", diff_text=""):
    context = {}
    affected_files = set()

    for line in diff_text.splitlines():
        if line.startswith("+++ b/"):
            filepath = line.replace("+++ b/", "").strip()
            affected_files.add(filepath)

    for fp in affected_files:
        if os.path.exists(fp):
            try:
                with open(fp, "r", encoding="utf-8") as f:
                    context[fp] = f.read()[:4000]
            except:
                pass

    return context

repo_context = load_repo_context_dynamic(".", diff_content)

Prompt = f"""
You are an expert PR reviewer. You MUST base your review ONLY on:

1. Actual PR diff
2. Semgrep findings (full results)
3. Repository context (only relevant files)

Never write generic advice. Only comment on **real issues proven by Semgrep or seen in the diff**.

# PR DIFF
{diff_content}

# SEMGREP FINDINGS (full results)
{json.dumps(semgrep_json.get("results", []), indent=2)}

# REPO CONTEXT (only files touched)
{json.dumps(repo_context, indent=2)}

Respond using EXACTLY this format:

## Summary of Actual Changes
- Describe what changed in the PR.

## Impact on This Repository
- Explain how these changes affect the repo’s behavior or files.

## Issues / Risks Found
- Pull issues ONLY from:
  - Semgrep findings
  - Actual diff issues (bugs, logic problems)

## Required Fixes
- Fixes must reference exact lines, files, or Semgrep rules.
- No generic security advice.
- No assumptions beyond the diff/context.

Output MUST be under 100 words. No extra text.
"""

client = genai.Client(api_key=api_key)
response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=Prompt,
)

print(response.text.strip())