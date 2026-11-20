from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "evals/plan-review"))
import followup  # noqa: E402


class FollowupJobs(unittest.TestCase):
    def test_call_counts_match_the_frozen_protocol(self):
        self.assertEqual(len(followup.jobs("better", "claude")), 24)
        self.assertEqual(len(followup.jobs("stakes")), 24)
        self.assertEqual(len(followup.jobs("revise", critiques=ROOT / "runs/portfolio-full-codex")), 24)
        claude = followup.jobs("revise", critiques=ROOT / "runs/portfolio-full-claude")
        self.assertEqual(len(claude), 21)
        self.assertTrue(all(provider == "claude" and "=== REVIEW ===" in payload for _, provider, _, payload in claude))


if __name__ == "__main__":
    unittest.main()
