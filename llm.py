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

# Read inputs safely
diff_path = sys.argv[1] if len(sys.argv) > 1 else None
semgrep_path = sys.argv[2] if len(sys.argv) > 2 else None

diff_content = ""
if diff_path and os.path.exists(diff_path):
    with open(diff_path, "r", encoding="utf-8") as f:
        diff_content = f.read()

# Handle empty diff (avoid generic LLM output)
if not diff_content or len(diff_content.strip()) < 10:
    print("⚠️ Diff missing or too small. Unable to generate PR summary.")
    sys.exit(0)

# Load Semgrep summary
semgrep_summary = "No Semgrep issues found."
try:
    if semgrep_path and os.path.exists(semgrep_path):
        with open(semgrep_path, "r", encoding="utf-8") as f:
            semgrep_json = json.load(f)
            findings = semgrep_json.get("results", [])
            if findings:
                semgrep_summary = "\n".join(
                    f"- {i['check_id']}: {i['extra'].get('message','')}"
                    for i in findings
                )
except Exception as e:
    semgrep_summary = f"Semgrep error: {e}"

# GitHub client
gh = Github(auth=Auth.Token(github_token))
repo = gh.get_repo(repo_full)
pr = repo.get_pull(pr_number)

# Stronger prompt to prevent generic answers
prompt = f"""
You are an expert senior code reviewer. 
Your summary MUST be based ONLY on the actual diff provided.
Generic statements are forbidden.

### PR Title
{pr.title}

### DIFF (source of truth)
{diff_content}

### SEMGREP FINDINGS
{semgrep_summary}

### STRICT OUTPUT FORMAT

### Summary
- 2–3 bullets describing concrete changes visible in the diff.

### Why It Matters
- 1–2 bullets grounded ONLY in the diff.

### Issues
- Real problems found in the diff or Semgrep. 
- Write "None" if no issues.

### Verdict
- Approve / Needs Fixes / Review Required.

### Risk Level
- LOW / MEDIUM / HIGH.

### Recommendations
- Max 2 bullets based ONLY on the diff.

RULES:
- NEVER write generic or vague statements.
- NEVER invent information not visible in the diff.
- NEVER repeat PR title.
- If something is unclear, explicitly say: "Not visible in diff".
- Maximum length: 120 words.
"""

client = genai.Client(api_key=api_key)

response = client.models.generate_content(
    model="gemini-2.0-flash",
    contents=prompt
)

print(response.text.strip())
