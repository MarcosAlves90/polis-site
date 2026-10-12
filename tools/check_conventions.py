#!/usr/bin/env python3
"""Validate new Git commit subjects and pull request metadata."""

import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path


SUBJECT = re.compile(
    r"^(feat|fix|docs|style|refactor|perf|test|build|ci|chore|revert)"
    r"(?:\([a-z0-9]+(?:-[a-z0-9]+)*\))?!?: [A-Za-z0-9][^\r\n]*$"
)
SHA = re.compile(r"[a-f0-9]{40}")
REQUIRED_SECTIONS = ("Summary", "Validation")


def check_subject(subject):
    """Return the reasons a Conventional Commit subject is invalid."""
    errors = []
    if subject != subject.strip():
        errors.append("Remove leading or trailing whitespace.")
    if len(subject) > 72:
        errors.append("Keep the subject to 72 characters or fewer.")
    if not SUBJECT.fullmatch(subject):
        errors.append("Use 'type(optional-scope): Imperative English summary'.")
    if subject.endswith("."):
        errors.append("Do not end the subject with a period.")
    return errors


def check_pr_body(body):
    """Require useful Summary and Validation sections, ignoring template comments."""
    cleaned = re.sub(r"<!--.*?-->", "", body or "", flags=re.DOTALL)
    headings = list(re.finditer(r"(?m)^## ([^\n]+)\s*$", cleaned))
    sections = {}
    for index, match in enumerate(headings):
        end = headings[index + 1].start() if index + 1 < len(headings) else len(cleaned)
        sections[match.group(1).strip().lower()] = cleaned[match.end():end].strip()
    errors = []
    for heading in REQUIRED_SECTIONS:
        value = sections.get(heading.lower(), "")
        if not re.search(r"[\w]", value, flags=re.UNICODE):
            errors.append(f"Add a substantive '## {heading}' section in English.")
    return errors


def git_subjects(start, end):
    """Read commit subjects from a SHA-bounded range, omitting merge commits."""
    if not SHA.fullmatch(end) or (start and not SHA.fullmatch(start)):
        raise ValueError("Invalid commit SHA in GitHub event.")
    revision = f"{start}..{end}" if start and start != "0" * 40 else end
    command = ["git", "log", "--no-merges", "--format=%s"]
    if not start or start == "0" * 40:
        # A new branch should not fail because of older, pre-policy commits.
        command.extend(["--no-walk", revision])
    else:
        command.append(revision)
    result = subprocess.run(command, check=True, capture_output=True, text=True)
    return [line for line in result.stdout.splitlines() if line]


def check_event():
    """Check only contributions introduced in the current GitHub Actions event."""
    event_path = os.environ.get("GITHUB_EVENT_PATH")
    if not event_path:
        raise ValueError("GITHUB_EVENT_PATH is not defined.")
    event = json.loads(Path(event_path).read_text(encoding="utf-8"))
    event_name = os.environ.get("GITHUB_EVENT_NAME")
    errors = []
    if event_name == "pull_request":
        pr = event["pull_request"]
        errors.extend(f"PR title: {item}" for item in check_subject(pr["title"]))
        errors.extend(f"PR description: {item}" for item in check_pr_body(pr.get("body")))
        start, end = pr["base"]["sha"], pr["head"]["sha"]
    elif event_name == "push":
        start, end = event.get("before"), event.get("after")
        if not end or end == "0" * 40:
            return []
    else:
        raise ValueError(f"Unsupported GitHub event: {event_name}")

    for subject in git_subjects(start, end):
        errors.extend(f"Commit '{subject}': {item}" for item in check_subject(subject))
    return errors


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    subcommands = parser.add_subparsers(dest="command", required=True)
    subcommands.add_parser("event", help="Validate the GitHub Actions event.")
    for name in ("commit-file", "commit-message"):
        subcommands.add_parser(name, help="Validate a new commit subject.").add_argument("value")
    args = parser.parse_args(argv)
    try:
        if args.command == "event":
            errors = check_event()
        elif args.command == "commit-file":
            message = Path(args.value).read_text(encoding="utf-8")
            errors = check_subject(message.splitlines()[0] if message.splitlines() else "")
        else:
            errors = check_subject(args.value)
    except (OSError, KeyError, ValueError, subprocess.CalledProcessError) as exc:
        print(f"Convention check could not run: {exc}", file=sys.stderr)
        return 1

    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1
    print("Contribution conventions validated.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
