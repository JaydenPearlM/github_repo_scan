import requests
from src.config import GITHUB_TOKEN

BASE_URL = "https://api.github.com"


def github_headers():
    return {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json",
    }


def delete_repo(owner, repo_name):
    url = f"{BASE_URL}/repos/{owner}/{repo_name}"

    response = requests.delete(url, headers=github_headers(), timeout=30)

    if response.status_code == 204:
        return True

    print(f"Delete failed for {repo_name}: {response.status_code}")
    print(response.text)
    return False