"""The hidden tests of the outcome test must pass on a correct answer and fail on the naive one."""

from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "evals/outcome"))
import outcome  # noqa: E402

CORRECT = {
    "t1-gate": "def gate_time_s(start_tick, stop_tick):\n    return ((stop_tick - start_tick) % 65536) / 10000\n",
    "t2-attendance": (
        "from datetime import datetime\n"
        "def merge_attendance(records):\n"
        "    kept = {}\n"
        "    for r in records:\n"
        "        key = (r['player'], r['date'])\n"
        "        when = datetime.fromisoformat(r['updated_at'])\n"
        "        if key not in kept or when > datetime.fromisoformat(kept[key]['updated_at']):\n"
        "            kept[key] = r\n"
        "    return list(kept.values())\n"
    ),
    "t3-forecast": (
        "def trailing_mean(sales, day, window=7):\n"
        "    past = sales[max(0, day - window):day]\n"
        "    return sum(past) / len(past) if past else None\n"
    ),
    "t4-recall": (
        "def clip_recall(highlights, clips):\n"
        "    owner = {}\n"
        "    def place(h, seen):\n"
        "        for c, (cs, ce) in enumerate(clips):\n"
        "            if c not in seen and min(ce, highlights[h][1]) > max(cs, highlights[h][0]):\n"
        "                seen.add(c)\n"
        "                if c not in owner or place(owner[c], seen):\n"
        "                    owner[c] = h\n"
        "                    return True\n"
        "        return False\n"
        "    return sum(place(h, set()) for h in range(len(highlights))) / len(highlights)\n"
    ),
    "t5-inventory": (
        "def available(stock, reservations, now_s):\n"
        "    held = sum(r['qty'] for r in reservations if r['paid'] or now_s - r['created_s'] <= 300)\n"
        "    return max(0, stock - held)\n"
    ),
    "t6-crop": (
        "def to_tracker(x, y):\n"
        "    if not (240 <= x < 1680 and 0 <= y < 1080):\n"
        "        return None\n"
        "    return ((x - 240) / 2, y / 2)\n"
    ),
}
NAIVE = {
    "t1-gate": "def gate_time_s(start_tick, stop_tick):\n    return (stop_tick - start_tick) / 10000\n",
    "t2-attendance": (
        "def merge_attendance(records):\n"
        "    kept = {}\n"
        "    for r in records:\n"
        "        key = (r['player'], r['date'])\n"
        "        if key not in kept or r['updated_at'] > kept[key]['updated_at']:\n"
        "            kept[key] = r\n"
        "    return list(kept.values())\n"
    ),
    "t3-forecast": "def trailing_mean(sales, day, window=7):\n    return sum(sales[day - window:day]) / window if day else None\n",
    "t4-recall": (
        "def clip_recall(highlights, clips):\n"
        "    used, found = set(), 0\n"
        "    for hs, he in highlights:\n"
        "        for c, (cs, ce) in enumerate(clips):\n"
        "            if c not in used and min(ce, he) > max(cs, hs):\n"
        "                used.add(c); found += 1; break\n"
        "    return found / len(highlights)\n"
    ),
    "t5-inventory": "def available(stock, reservations, now_s):\n    return stock - sum(r['qty'] for r in reservations)\n",
    "t6-crop": "def to_tracker(x, y):\n    return (x // 2, y // 2)\n",
}


class HiddenTests(unittest.TestCase):
    def test_six_tasks_each_with_a_prompt_and_tests(self):
        self.assertEqual(outcome.TASKS, sorted(CORRECT))

    def test_correct_answers_pass_and_naive_answers_fail(self):
        for task in outcome.TASKS:
            with self.subTest(task=task):
                self.assertIsNone(outcome.grade(task, CORRECT[task]))
                self.assertIsNotNone(outcome.grade(task, NAIVE[task]))

    def test_the_trap_is_what_fails(self):
        self.assertEqual(outcome.grade("t1-gate", NAIVE["t1-gate"]), "wrong time for start_tick=60000, stop_tick=4464")

    def test_code_is_taken_from_the_last_python_block(self):
        self.assertEqual(outcome.extract_code("x\n```python\na = 1\n```\ny\n```python\nb = 2\n```"), "b = 2\n")
        self.assertEqual(outcome.grade("t1-gate", outcome.extract_code("no code here")), "there was no python code block in the reply")

    def test_a_self_test_block_in_the_answer_does_not_replace_the_hidden_tests(self):
        noisy = "\ndef test_mine():\n    assert False\nif __name__ == '__main__':\n    raise SystemExit(0)\n"
        self.assertIsNone(outcome.grade("t1-gate", CORRECT["t1-gate"] + noisy))
        self.assertIsNotNone(outcome.grade("t1-gate", NAIVE["t1-gate"] + noisy))

    def test_an_answer_cannot_fake_a_pass_or_read_the_hidden_tests(self):
        fake = "import os\nprint('PASS', flush=True)\nos._exit(0)\n"
        self.assertIsNotNone(outcome.grade("t1-gate", fake))
        peek = "import glob\nassert not any('def test_' in open(p).read() for p in glob.glob('*') if p != 'solution.py')\n"
        self.assertIsNone(outcome.grade("t1-gate", peek + CORRECT["t1-gate"]))

    def test_a_hang_or_a_crash_counts_as_a_failure(self):
        self.assertEqual(outcome.grade("t1-gate", "import nothing_like_this"), "the code crashed when it was loaded")


if __name__ == "__main__":
    unittest.main()
