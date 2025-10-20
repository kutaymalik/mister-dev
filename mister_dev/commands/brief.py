from __future__ import annotations
import click, json
from typing import List, Dict
from ..openai_client import chat_json

BRIEF_SYSTEM = {
    "role": "system",
    "content": (
        "You are a pragmatic product owner. "
        "Given a Turkish brief, output English Jira artifacts in JSON: "
        "{title, description, acceptanceCriteria[], checklist[], labels[], suggestedBranch}."
    ),
}

BRIEF_USER_TEMPLATE = (
    "Turkish brief (business + tech):\n"
    "----\n{brief}\n----\n"
    "Return strict JSON with keys: title, description, acceptanceCriteria, checklist, labels, suggestedBranch."
)

@click.command(help="Generate EN Jira title/description/AC/checklist/labels/branch from a Turkish brief.")
@click.argument("brief", nargs=-1, required=True)
def brief(brief: List[str]):
    text = " ".join(brief).strip()
    payload = chat_json([
        BRIEF_SYSTEM,
        {"role": "user", "content": BRIEF_USER_TEMPLATE.format(brief=text)}
    ])
    click.echo(json.dumps(payload, ensure_ascii=False, indent=2))
