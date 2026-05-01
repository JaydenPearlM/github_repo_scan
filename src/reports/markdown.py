from datetime import datetime
from pathlib import Path


def save_analysis_report(repo_name, content):
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)

    safe_repo_name = repo_name.replace("/", "__").replace(" ", "_")
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    file_path = output_dir / f"{safe_repo_name}_{timestamp}.md"

    file_path.write_text(content, encoding="utf-8")

    return file_path