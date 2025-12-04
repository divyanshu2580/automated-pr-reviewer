import os
import sys
from github import Github, Auth
from google import genai
import json

# Load env vars
api_key = os.getenv("GEMINI_API_KEY")
repo_full = os.getenv("REPO_FULL_NAME")
pr_number = int(os.getenv("PR_NUMBER"))
github_token = os.getenv("GITHUB_TOKEN")
semgrep_config = os.getenv("SEMGREP_CONFIG", "unknown")

# Read inputs safely
diff_path = sys.argv[1] if len(sys.argv) > 1 else "pr_diff.patch"
semgrep_path = sys.argv[2] if len(sys.argv) > 2 else "semgrep_output.json"

diff_content = ""
if os.path.exists(diff_path):
    with open(diff_path, "r", encoding="utf-8") as f:
        diff_content = f.read().strip()

if len(diff_content) < 10:
    print("⚠️ Diff missing or too small. Unable to generate PR summary.")
    sys.exit(0)

# Load Semgrep summary
semgrep_summary = "No Semgrep issues found."
try:
    if os.path.exists(semgrep_path):
        with open(semgrep_path, "r", encoding="utf-8") as f:
            semgrep_json = json.load(f)
            findings = semgrep_json.get("results", [])
            if findings:
                semgrep_summary = "\n".join(
                    f"- {item['check_id']}: {item['extra'].get('message','')}"
                    for item in findings
                )
except Exception as e:
    semgrep_summary = f"Semgrep error: {e}"

# GitHub client
gh = Github(auth=Auth.Token(github_token))
repo = gh.get_repo(repo_full)
pr = repo.get_pull(pr_number)

# LLM prompt
prompt = f"""
You are an expert senior code reviewer. Your summary MUST be based ONLY on the actual diff provided.

### PR Title
{pr.title}

### DIFF
{diff_content}

### SEMGREP CONFIG USED
{semgrep_config}

### SEMGREP FINDINGS
{semgrep_summary}

### STRICT OUTPUT FORMAT

### Summary
- 2–3 bullets describing concrete changes in the diff.

### Why It Matters
- 1–2 bullets based ONLY on the diff.

### Issues
- Real issues from diff or Semgrep. Write "None" if nothing.

### Verdict
- Approve / Needs Fixes / Review Required.

### Risk Level
- LOW / MEDIUM / HIGH.

### Recommendations
- Max 2 bullets based ONLY on the diff.

RULES:
- NEVER invent details.
- NEVER provide generic statements.
- If not visible in diff, say: "Not visible in diff".
- Max length: 120 words.
"""

client = genai.Client(api_key=api_key)

response = client.models.generate_content(
    model="gemini-2.0-flash",
    contents=prompt
)

print(response.text.strip())
