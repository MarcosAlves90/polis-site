"""Regression tests for contribution metadata validation."""

import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from tools.check_conventions import check_event, check_pr_body, check_subject, git_subjects


class ContributionConventionTests(unittest.TestCase):
    def test_valid_conventional_commit_subjects(self):
        for subject in (
            "docs: Clarify the build instructions",
            "fix(search): Preserve localized results",
            "feat!: Remove deprecated routing",
            "ci(pull-request): Validate new metadata",
        ):
            with self.subTest(subject=subject):
                self.assertEqual(check_subject(subject), [])

    def test_invalid_commit_subjects(self):
        for subject in (
            "Update the README",
            "Docs: Update the README",
            "docs: Finish with a period.",
            "docs(BadScope): Fix routing",
            "docs: " + "x" * 70,
            " docs: Remove leading whitespace",
        ):
            with self.subTest(subject=subject):
                self.assertTrue(check_subject(subject))

    def test_pr_body_requires_completed_sections(self):
        template = (
            "## Summary\n<!-- Explain the change in English. -->\n"
            "## Validation\n<!-- Include checks. -->\n## Related issues\n"
        )
        self.assertEqual(len(check_pr_body(template)), 2)
        completed = (
            "## Summary\nDocumented commit conventions.\n\n"
            "## Validation\n- Python tests passed.\n\n## Related issues\nNone.\n"
        )
        self.assertEqual(check_pr_body(completed), [])
        self.assertEqual(len(check_pr_body(None)), 2)

    def test_pr_event_validates_title_body_and_introduced_commits(self):
        event = {
            "pull_request": {
                "title": "docs: Explain the PR format",
                "body": "## Summary\nExplain PR descriptions.\n## Validation\nTests passed.",
                "base": {"sha": "a" * 40},
                "head": {"sha": "b" * 40},
            }
        }
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "event.json"
            path.write_text(json.dumps(event), encoding="utf-8")
            with patch.dict(os.environ, {
                "GITHUB_EVENT_NAME": "pull_request",
                "GITHUB_EVENT_PATH": str(path),
            }):
                with patch("tools.check_conventions.git_subjects", return_value=[
                    "docs: Update docs", "Untyped subject"
                ]) as read_subjects:
                    errors = check_event()
        read_subjects.assert_called_once_with("a" * 40, "b" * 40)
        self.assertEqual(len(errors), 1)
        self.assertIn("Untyped subject", errors[0])

    def test_new_branch_push_checks_only_latest_commit(self):
        event = {"before": "0" * 40, "after": "a" * 40}
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "event.json"
            path.write_text(json.dumps(event), encoding="utf-8")
            with patch.dict(os.environ, {
                "GITHUB_EVENT_NAME": "push",
                "GITHUB_EVENT_PATH": str(path),
            }):
                with patch("tools.check_conventions.git_subjects", return_value=[
                    "fix: Correct typo"
                ]) as read_subjects:
                    self.assertEqual(check_event(), [])
        read_subjects.assert_called_once_with("0" * 40, "a" * 40)

    def test_new_branch_commit_lookup_does_not_visit_older_history(self):
        with patch("tools.check_conventions.subprocess.run") as run:
            run.return_value.stdout = "docs: Update contributor guide\n"
            self.assertEqual(git_subjects("0" * 40, "a" * 40), [
                "docs: Update contributor guide"
            ])
        self.assertEqual(run.call_args.args[0], [
            "git", "log", "--no-merges", "--format=%s", "--no-walk", "a" * 40
        ])
        with self.assertRaises(ValueError):
            git_subjects("bad", "a" * 40)


if __name__ == "__main__":
    unittest.main()
