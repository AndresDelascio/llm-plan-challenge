"""The regrade sample must be fixed, balanced, and show each finding in full."""

from pathlib import Path
import collections
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "evals/plan-review"))
import regrade  # noqa: E402


class Sample(unittest.TestCase):
    def test_the_sample_is_fixed_and_balanced(self):
        first, second = regrade.sample(), regrade.sample()
        self.assertEqual(first, second)
        self.assertEqual(collections.Counter(it["reviewer"] for it in first), {"codex": 15, "claude": 15})
        self.assertTrue(all(it["claude_grader"] in ("valid", "unsupported") for it in first))

    def test_a_finding_is_cut_at_the_next_heading(self):
        text = regrade.finding("c01", 1)
        self.assertTrue(text.startswith("### 1."))
        self.assertIn("- Fix:", text)
        self.assertNotIn("### 2.", text)


if __name__ == "__main__":
    unittest.main()
