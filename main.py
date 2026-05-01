from src.github_client.client import get_repos


def main():
    print("Scanning GitHub...\n")

    repos = get_repos()

    if not repos:
        print("No repos found.")
        return

    for repo in repos:
        print(f"- {repo['name']}")


if __name__ == "__main__":
    main()