import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed

from src.github_client.client import get_repos
from src.github_client.files import get_repo_tree, get_file_content
from src.github_client.repo_manager import delete_repo
from src.scanner.file_filter import select_code_files
from src.reports.analyzer import build_analysis_prompt
from src.claude_client.analyzer import run_claude_analysis
from src.reports.markdown import save_analysis_report


BRANCH_OVERRIDES = {
    "DeltaPets_Brower_Game": "Core_Systems_version_1",
}

IGNORED_REPOS = {
    "JaydenPearlM",
}

MAX_CHARS_PER_FILE = 5000
MAX_WORKERS = 8


def fetch_file_for_report(owner, repo_name, branch, file_path):
    content = get_file_content(owner, repo_name, file_path, branch)

    if not content.strip():
        return None

    return {
        "path": file_path,
        "content": content[:MAX_CHARS_PER_FILE],
    }


def print_repo_list(repos, visibility=None):
    filtered = repos

    if visibility == "private":
        filtered = [repo for repo in repos if repo.get("private") is True]

    if visibility == "public":
        filtered = [repo for repo in repos if repo.get("private") is False]

    if not filtered:
        print(f"No {visibility or ''} repos found.")
        return

    for repo in filtered:
        name = repo["name"]

        if name in IGNORED_REPOS:
            continue

        privacy = "private" if repo.get("private") else "public"
        branch = repo.get("default_branch", "main")
        print(f"- {name} [{privacy}] branch: {branch}")


def run_scan(repos):
    print("Scanning GitHub...\n")

    for repo in repos:
        repo_name = repo["name"]

        if repo_name in IGNORED_REPOS:
            print(f"\nSkipping ignored repo: {repo_name}")
            continue

        owner = repo["owner"]["login"]
        branch = BRANCH_OVERRIDES.get(repo_name, repo.get("default_branch", "main"))

        print(f"\nRepo: {repo_name}")
        print(f"  Branch: {branch}")

        tree = get_repo_tree(owner, repo_name, branch)
        code_files = select_code_files(tree)

        if not code_files:
            print("  No useful code files found.")
            continue

        for file_path in code_files:
            print(f"  - {file_path}")

        files_for_report = []

        with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
            futures = [
                executor.submit(
                    fetch_file_for_report,
                    owner,
                    repo_name,
                    branch,
                    file_path,
                )
                for file_path in code_files
            ]

            for future in as_completed(futures):
                result = future.result()

                if result:
                    files_for_report.append(result)

        files_for_report.sort(key=lambda file: file["path"])

        if not files_for_report:
            print("  No readable file content found.")
            continue

        print("  Running Claude analysis...")

        prompt = build_analysis_prompt(repo_name, files_for_report)
        analysis = run_claude_analysis(prompt)

        report_path = save_analysis_report(repo_name, analysis)

        print(f"  Analysis saved: {report_path}")

    print("\nScan complete.")


def main():
    parser = argparse.ArgumentParser(description="GitHub repo scanner and manager")

    parser.add_argument(
        "--list",
        choices=["all", "public", "private"],
        help="List repositories by visibility.",
    )

    parser.add_argument(
        "--delete",
        help="Delete a repository by exact repo name.",
    )

    parser.add_argument(
        "--confirm",
        action="store_true",
        help="Required confirmation flag for destructive actions.",
    )

    parser.add_argument(
        "--scan",
        action="store_true",
        help="Scan repositories and generate markdown reports.",
    )

    args = parser.parse_args()
    repos = get_repos()

    if not repos:
        print("No repos found.")
        return

    if args.list:
        visibility = None if args.list == "all" else args.list
        print_repo_list(repos, visibility)
        return

    if args.delete:
        matching_repo = next(
            (repo for repo in repos if repo["name"] == args.delete),
            None,
        )

        if not matching_repo:
            print(f"Repo not found: {args.delete}")
            return

        if not args.confirm:
            print("Delete blocked.")
            print("To delete this repo, run:")
            print(f"python main.py --delete {args.delete} --confirm")
            return

        owner = matching_repo["owner"]["login"]
        success = delete_repo(owner, args.delete)

        if success:
            print(f"Deleted repo: {args.delete}")

        return

    if args.scan:
        run_scan(repos)
        return

    print("No command provided.")
    print("Examples:")
    print("python main.py --list all")
    print("python main.py --list public")
    print("python main.py --list private")
    print("python main.py --scan")
    print("python main.py --delete repo_name --confirm")


if __name__ == "__main__":
    main()