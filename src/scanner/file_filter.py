ALLOWED_EXTENSIONS = (
    ".py",
    ".js",
    ".jsx",
    ".ts",
    ".tsx",
    ".sql",
    ".ipynb",
)

BLOCKED_PARTS = (
    "node_modules",
    ".git",
    ".venv",
    "dist",
    "build",
    "__pycache__",
    "package-lock.json",
    "pnpm-lock.yaml",
)


def is_useful_code_file(path):
    lower_path = path.lower()

    if any(blocked in lower_path for blocked in BLOCKED_PARTS):
        return False

    return lower_path.endswith(ALLOWED_EXTENSIONS)


def select_code_files(tree, max_files=8):
    files = []

    for item in tree:
        path = item.get("path", "")

        if item.get("type") == "blob" and is_useful_code_file(path):
            files.append(path)

    return files[:max_files]