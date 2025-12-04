import os
import aiohttp
import asyncio
import logging
from datetime import datetime
from dataclasses import dataclass

# -----------------------------
# Logging Setup
# -----------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

# -----------------------------
# Dataclass for Repo Info
# -----------------------------
@dataclass
class RepoInfo:
    name: str
    stars: int
    forks: int
    open_issues: int
    last_updated: datetime


# -----------------------------
# GitHub API Client (Async)
# -----------------------------
class GitHubClient:
    def __init__(self, token: str):
        self.headers = {"Authorization": f"Bearer {token}"}

    async def fetch_repo(self, session, full_name: str) -> RepoInfo:
        url = f"https://api.github.com/repos/{full_name}"

        try:
            async with session.get(url, headers=self.headers) as response:
                if response.status != 200:
                    raise Exception(f"GitHub API error: {response.status}")

                data = await response.json()

                return RepoInfo(
                    name=data["full_name"],
                    stars=data["stargazers_count"],
                    forks=data["forks_count"],
                    open_issues=data["open_issues_count"],
                    last_updated=datetime.fromisoformat(data["updated_at"].replace("Z", ""))
                )

        except Exception as e:
            logging.error(f"Error fetching repo {full_name}: {e}")
            raise


# -----------------------------
# Analyzer Class
# -----------------------------
class RepoAnalyzer:
    def __init__(self, repos):
        self.repos = repos
        token = os.getenv("GITHUB_TOKEN")

        if not token:
            raise Exception("Missing GITHUB_TOKEN environment variable")

        self.client = GitHubClient(token)

    async def analyze(self):
        async with aiohttp.ClientSession() as session:
            tasks = [self.client.fetch_repo(session, repo) for repo in self.repos]

            results = await asyncio.gather(*tasks, return_exceptions=True)

            for res in results:
                if isinstance(res, Exception):
                    continue
                self.print_report(res)

    @staticmethod
    def print_report(repo: RepoInfo):
        print("\n------------------------------")
        print(f"📦 Repository: {repo.name}")
        print(f"⭐ Stars: {repo.stars}")
        print(f"🍴 Forks: {repo.forks}")
        print(f"🐞 Open Issues: {repo.open_issues}")
        print(f"🕒 Last Updated: {repo.last_updated}")
        print("------------------------------\n")


# -----------------------------
# Main Runner
# -----------------------------
if __name__ == "__main__":
    repos_to_check = [
        "openai/gym",
        "psf/requests",
        "pallets/flask",
    ]

    analyzer = RepoAnalyzer(repos_to_check)

    try:
        asyncio.run(analyzer.analyze())
    except Exception as e:
        logging.error(f"Program failed: {e}")
