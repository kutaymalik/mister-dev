from __future__ import annotations
import click, subprocess, datetime as dt, os, pathlib

@click.command(help="Create a daily/weekly summary from git commits.")
@click.option("--today", is_flag=True, help="Summarize today's commits.")
@click.option("--week", is_flag=True, help="Summarize last 7 days.")
def summary(today: bool, week: bool):
    since = ""
    if today:
        since = "--since=midnight"
    elif week:
        since = "--since='7 days ago'"
    out = subprocess.getoutput(f"git log {since} --pretty=format:'%ad %h %s' --date=short")
    date_str = dt.date.today().isoformat()
    md = f"""# Daily Summary - {date_str}

{out if out.strip() else 'No commits in the selected period.'}
"""
    docs = pathlib.Path("docs")
    docs.mkdir(exist_ok=True)
    path = docs / f"Daily-{date_str}.md"
    path.write_text(md, encoding="utf-8")
    click.echo(f"Written: {path}")
