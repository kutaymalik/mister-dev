from __future__ import annotations
import subprocess, click, json, shutil
from typing import Dict, Any, List
from ..openai_client import chat_json

COMMIT_SYSTEM = {
    "role": "system",
    "content": (
        "You are a senior backend engineer. "
        "Given a staged git diff, output JSON: "
        "{commit, jiraComment}. "
        "Use conventional commits (feat|fix|refactor|docs|test|chore). "
        "Keep 'commit' under 72 chars. Be precise, professional."
    ),
}

def get_staged_diff() -> str:
    return subprocess.getoutput("git diff --cached")

@click.command(help="Generate a conventional commit message (and Jira comment) from staged diff.")
@click.option("--apply", is_flag=True, help="Run 'git commit -m' automatically with the generated message.")
def commit(apply: bool):
    diff = get_staged_diff()
    if not diff.strip():
        click.echo("No staged changes found. Hint: git add .")
        return
    payload = chat_json([
        COMMIT_SYSTEM,
        {"role": "user", "content": f"""Staged git diff:
---
{diff}
---
Return JSON with: commit, jiraComment.
"""}
    ])
    # Pretty print result
    click.echo(json.dumps(payload, ensure_ascii=False, indent=2))

    if apply and isinstance(payload, dict) and "commit" in payload:
        msg = payload["commit"]
        # run git commit -m "msg"
        if shutil.which("git"):
            code = subprocess.call(["git", "commit", "-m", msg])
            if code == 0:
                click.echo("✔ Commit created.")
            else:
                click.echo("Failed to run git commit.")
        else:
            click.echo("git not found in PATH. Skipping --apply.")
