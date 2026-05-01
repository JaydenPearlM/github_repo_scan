import base64
import requests
from src.config import GITHUB_TOKEN

BASE_URL = "https://api.github.com"

session = requests.Session()
session.headers.update(
    {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json",
    }
)


def get_repo_tree(owner, repo, branch="main"):
    url = f"{BASE_URL}/repos/{owner}/{repo}/git/trees/{branch}?recursive=1"

    response = session.get(url, timeout=20)

    if response.status_code != 200:
        print(f"Could not fetch files for {repo}: {response.text}")
        return []

    return response.json().get("tree", [])


def get_file_content(owner, repo, file_path, branch="main"):
    url = f"{BASE_URL}/repos/{owner}/{repo}/contents/{file_path}"

    response = session.get(url, params={"ref": branch}, timeout=20)

    if response.status_code != 200:
        return ""

    data = response.json()

    if data.get("encoding") != "base64":
        return ""

    return base64.b64decode(data["content"]).decode("utf-8", errors="replace")