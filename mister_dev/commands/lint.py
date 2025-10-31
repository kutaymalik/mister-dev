from __future__ import annotations

import os
import py_compile
import re
import subprocess
from dataclasses import dataclass
from typing import Iterable, List, Sequence

import click


@dataclass
class Issue:
    path: str
    line: int
    message: str


WARNING_PATTERNS: Sequence[tuple[re.Pattern[str], str]] = (
    (re.compile(r"\bprint\s*\("), "Debug print statement found."),
    (re.compile(r"\bpdb\s*\.\s*set_trace\s*\("), "Debugger breakpoint (pdb.set_trace) found."),
)

TODO_PATTERN = re.compile(r"(#|//)\s*(TODO|FIXME)", re.IGNORECASE)


def _iter_staged_files() -> List[str]:
    result = subprocess.getoutput("git diff --cached --name-only")
    files = [line.strip() for line in result.splitlines() if line.strip()]
    return [f for f in files if os.path.exists(f)]


def _check_python_file(path: str) -> Iterable[Issue]:
    try:
        py_compile.compile(path, doraise=True)
    except py_compile.PyCompileError as exc:
        yield Issue(path, exc.lineno or 0, f"Python syntax error: {exc.msg}")
        return

    with open(path, "r", encoding="utf-8", errors="ignore") as handle:
        for idx, line in enumerate(handle, start=1):
            stripped = line.rstrip("\n")
            if len(stripped) > 120:
                yield Issue(path, idx, "Line length exceeds 120 characters.")
            if stripped.rstrip() != stripped:
                yield Issue(path, idx, "Trailing whitespace detected.")
            for pattern, message in WARNING_PATTERNS:
                if pattern.search(line):
                    yield Issue(path, idx, message)
            if TODO_PATTERN.search(line):
                yield Issue(path, idx, "TODO/FIXME marker left in code.")


def _check_text_file(path: str) -> Iterable[Issue]:
    with open(path, "r", encoding="utf-8", errors="ignore") as handle:
        for idx, line in enumerate(handle, start=1):
            stripped = line.rstrip("\n")
            if stripped.rstrip() != stripped:
                yield Issue(path, idx, "Trailing whitespace detected.")
            for pattern, message in WARNING_PATTERNS:
                if pattern.search(line):
                    yield Issue(path, idx, message)
            if TODO_PATTERN.search(line):
                yield Issue(path, idx, "TODO/FIXME marker left in code.")


@click.command(help="Run lightweight quality checks on staged files before committing.")
def lint():
    staged_files = _iter_staged_files()
    if not staged_files:
        click.echo("No staged files detected. Stage your changes before running lint.")
        return

    issues: List[Issue] = []
    for path in staged_files:
        if path.endswith(".py"):
            issues.extend(_check_python_file(path))
        else:
            issues.extend(_check_text_file(path))

    if not issues:
        click.echo("✅ Lint passed. You're ready to commit!")
        return

    click.echo("Found issues:")
    for issue in issues:
        location = f"{issue.path}:{issue.line}" if issue.line else issue.path
        click.echo(f"  - {location}: {issue.message}")
    raise SystemExit(1)
