import importlib.util
from pathlib import Path
import unittest


SCRIPT = Path(__file__).resolve().parents[1] / ".claude/skills/challenge/routing.py"
SPEC = importlib.util.spec_from_file_location("challenge_routing", SCRIPT)
routing = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(routing)


class RoutingTests(unittest.TestCase):
    def test_routine_uses_one_codex_critic(self):
        self.assertEqual(routing.route("auto", "routine"), "codex")

    def test_consequential_waits_for_confirmation(self):
        self.assertEqual(routing.route("auto", "consequential"), "confirm")

    def test_explicit_choices_win_at_every_stakes_level(self):
        for critic in ("codex", "claude", "both", "measure"):
            for stakes in ("routine", "consequential", None):
                with self.subTest(critic=critic, stakes=stakes):
                    self.assertEqual(routing.route(critic, stakes), critic)

    def test_no_silent_default_when_stakes_are_unknown(self):
        with self.assertRaisesRegex(ValueError, "classify"):
            routing.route("auto")
