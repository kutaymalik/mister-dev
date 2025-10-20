from __future__ import annotations
import click, subprocess

@click.command(help="Generate a PR title/description template from recent commits.")
@click.option("--n", default=5, show_default=True, help="How many commits to include.")
def pr(n: int):
    log = subprocess.getoutput(f"git log -n {n} --pretty=format:%s")
    title = "Improve stability and documentation across services"
    desc = f"""## Changes
{log}

## Testing
- [ ] Unit tests added/updated
- [ ] Manual verification in dev

## Risk
Low

## Rollback
Revert this PR
"""
    click.echo(title)
    click.echo()
    click.echo(desc)
