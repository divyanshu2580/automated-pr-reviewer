import os
from github import Github, Auth
from google import genai

# Environment variables from GitHub Actions
api_key = os.getenv("GEMINI_API_KEY")
repo_full = os.getenv("REPO_FULL_NAME")
pr_number = int(os.getenv("PR_NUMBER"))
github_token = os.getenv("GITHUB_TOKEN")

# GitHub client
gh = Github(auth=Auth.Token(github_token))
repo = gh.get_repo(repo_full)
pr = repo.get_pull(pr_number)

# Get file list
files = pr.get_files()
files_summary = "\n".join(
    [f"- {f.filename} (+{f.additions} / -{f.deletions})" for f in files]
)

pr_title = pr.title
pr_description = pr.body or "No description provided."

prompt = f"""
You are an expert Senior Software Engineer performing an in-depth Pull Request review.

Your task:
Write a **Automated PR summary** using GitHub Markdown.

### Output Format (IMPORTANT)
Follow this exact format:

## 📝 PR Summary
(1 short paragraph overview)

## 📂 Changed Files
- File name (added/removed/modified)
- Line summary (+ additions / - deletions)

## 🔍 What This PR Changes
(2–5 bullet points)

## 🎯 Why These Changes Matter
(2–4 bullet points)

## ⚠️ Risks & Impact
(1–3 bullet points)

## 🧪 Tests & Validation
- Missing tests?
- Required validations?
- Suggested test cases.

## 💡 Recommendations
(2–4 bullet points of suggestions)

Use **professional tone**, **no unnecessary text**, **no repetition**.

PR Title:
{pr_title}

PR Description:
{pr_description}

Changed Files:
{files_summary}
"""

# Gemini client (NEW API)
client = genai.Client(api_key=api_key)

response = client.models.generate_content(
    model="gemini-2.0-flash",
    contents=prompt
)

clean_text = response.text.strip()
print(clean_text)

print(response.text)
