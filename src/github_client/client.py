import requests
from src.config import GITHUB_TOKEN, GITHUB_USERNAME

BASE_URL = "https://api.github.com"


def get_repos():
    url = f"{BASE_URL}/users/{GITHUB_USERNAME}/repos"

    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json",
    }

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print("Error:", response.text)
        return []

    return response.json()