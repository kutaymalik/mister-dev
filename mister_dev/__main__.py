import click
from .commands.brief import brief
from .commands.commit import commit
from .commands.review import review
from .commands.pr import pr
from .commands.summary import summary

@click.group(help="Mister Dev (mr) — your all-in-one developer assistant.")
def cli():
    pass

cli.add_command(brief, "brief")
cli.add_command(commit, "commit")
cli.add_command(review, "review")
cli.add_command(pr, "pr")
cli.add_command(summary, "summary")

if __name__ == "__main__":
    cli()
