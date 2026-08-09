"""Tests for the list's tooling. Stdlib unittest only — no dependencies."""
import datetime
import pathlib
import sys
import unittest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "scripts"))

import build_readme  # noqa: E402
import check_health  # noqa: E402
import validate  # noqa: E402
from common import load_categories, load_entries, slugify  # noqa: E402

NOW = datetime.datetime(2026, 8, 9, tzinfo=datetime.timezone.utc)


class TestData(unittest.TestCase):
    def test_shipped_data_validates(self):
        self.assertEqual(validate.validate(), [])

    def test_readme_in_sync(self):
        current = build_readme.README.read_text(encoding="utf-8")
        self.assertEqual(current, build_readme.render(), "README.md is out of date")

    def test_every_category_has_entries(self):
        used = {e.category for e in load_entries()}
        for c in load_categories():
            self.assertIn(c.slug, used, f"category {c.slug!r} has no entries")


class TestSlugify(unittest.TestCase):
    def test_anchors(self):
        self.assertEqual(slugify("Instead of ChatGPT"), "instead-of-chatgpt")
        self.assertEqual(slugify("Instead of the OpenAI API"), "instead-of-the-openai-api")
        self.assertEqual(slugify("Instead of Cursor and Devin"), "instead-of-cursor-and-devin")


class TestClassify(unittest.TestCase):
    def test_dead(self):
        state, _ = check_health.classify(404, {}, NOW)
        self.assertEqual(state, "dead")

    def test_archived(self):
        state, _ = check_health.classify(200, {"archived": True, "pushed_at": "2026-08-01T00:00:00Z"}, NOW)
        self.assertEqual(state, "archived")

    def test_stale_beyond_12_months(self):
        state, detail = check_health.classify(
            200, {"archived": False, "pushed_at": "2025-06-01T00:00:00Z"}, NOW
        )
        self.assertEqual(state, "stale")
        self.assertIn("2025-06-01", detail)

    def test_fresh_within_12_months(self):
        state, _ = check_health.classify(
            200, {"archived": False, "pushed_at": "2026-07-01T00:00:00Z"}, NOW
        )
        self.assertEqual(state, "ok")

    def test_rate_limit_aborts(self):
        with self.assertRaises(check_health.Aborted):
            check_health.classify(403, {}, NOW)

    def test_unexpected_status_is_error_not_dead(self):
        state, _ = check_health.classify(500, {}, NOW)
        self.assertEqual(state, "error")


class TestReport(unittest.TestCase):
    def test_report_lists_problems(self):
        results = [
            {"name": "Good", "repo": "a/good", "state": "ok", "detail": "last push 2026-08-01"},
            {"name": "Bad", "repo": "a/bad", "state": "dead", "detail": "repository not found"},
        ]
        report = check_health.build_report(results, NOW)
        self.assertIn("1 need attention", report)
        self.assertIn("**dead**", report)
        self.assertIn("[a/bad](https://github.com/a/bad)", report)

    def test_report_all_healthy(self):
        results = [{"name": "Good", "repo": "a/good", "state": "ok", "detail": "fine"}]
        report = check_health.build_report(results, NOW)
        self.assertIn("Everything is alive", report)


if __name__ == "__main__":
    unittest.main()
