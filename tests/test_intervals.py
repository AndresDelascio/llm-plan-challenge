"""The exact interval must match closed forms and a published value."""

from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "evals"))
import intervals  # noqa: E402


class ExactInterval(unittest.TestCase):
    def test_all_passed_has_a_closed_form_lower_bound(self):
        lower, upper = intervals.exact_interval(12, 12)
        self.assertAlmostEqual(lower, 0.025 ** (1 / 12), places=6)  # 73.5%
        self.assertEqual(upper, 1.0)

    def test_none_passed_mirrors_all_passed(self):
        self.assertAlmostEqual(intervals.exact_interval(0, 12)[1], 1 - 0.025 ** (1 / 12), places=6)

    def test_a_textbook_value(self):
        # 5 of 10: Clopper-Pearson 95% is 0.1871 to 0.8129
        lower, upper = intervals.exact_interval(5, 10)
        self.assertAlmostEqual(lower, 0.1871, places=4)
        self.assertAlmostEqual(upper, 0.8129, places=4)


if __name__ == "__main__":
    unittest.main()
