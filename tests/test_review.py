import importlib.util
import io
import json
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / ".claude/skills/challenge/review.py"
SPEC = importlib.util.spec_from_file_location("challenge_review", SCRIPT)
runner = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(runner)

CLEAR = "VERDICT: NO BLOCKING ISSUES"
BLOCKED = """VERDICT: BLOCKED
### 1. [blocker] Data lost
- Failure: Restart drops the attendance history.
- Fix: Persist entries before reporting success."""


def codex_result(answer, *extra):
    events = [
        {"type": "thread.started", "thread_id": "test"},
        *extra,
        {"type": "item.completed", "item": {"type": "agent_message", "text": answer}},
        {"type": "turn.completed", "usage": {"input_tokens": 400, "cached_input_tokens": 200, "output_tokens": 28}},
    ]
    return "\n".join(map(json.dumps, events))


def claude_result(answer, **overrides):
    result = {
        "type": "result", "subtype": "success", "result": answer, "is_error": False, "num_turns": 1,
        "usage": {"input_tokens": 240, "output_tokens": 27, "cache_read_input_tokens": 80},
    }
    return json.dumps(result | overrides)


class ReviewTests(unittest.TestCase):
    def setUp(self):
        folder = tempfile.TemporaryDirectory(prefix="challenge tests ")
        self.addCleanup(folder.cleanup)
        self.project = Path(folder.name)
        self.plan = self.project / "draft.md"
        self.plan.write_text("## Goal\nSave attendance.\n## Plan\nStore entries in memory.", encoding="utf-8")
        self.report = self.project / "critique.md"
        self.metrics = self.project / "critique.usage.json"

    def run_review(self, provider, stdout, *, returncode=0, stderr=""):
        observed = {}

        def invoke(command, **kwargs):
            observed.update(command=command, **kwargs)
            cwd = Path(kwargs["cwd"])
            self.assertTrue(cwd.is_dir())
            self.assertEqual(list(cwd.iterdir()), [])
            self.assertNotEqual(cwd, self.project)
            return subprocess.CompletedProcess(command, returncode, stdout, stderr)

        with patch.object(runner.shutil, "which", return_value=f"/test/{provider}"), patch.object(
            runner, "run_limited", side_effect=invoke
        ):
            runner.save_review(provider, self.plan, self.report)
        return observed

    def test_codex_blocker_and_usage(self):
        call = self.run_review("codex", codex_result(BLOCKED))
        self.assertIn("--ignore-user-config", call["command"])
        self.assertIn("read-only", call["command"])
        self.assertIn("features.shell_tool=false", call["command"])
        self.assertIn('model_reasoning_effort="low"', call["command"])
        self.assertEqual(call["command"][-1], "-")
        self.assertEqual(call["input"].split("=== PLAN ===\n", 1)[1], self.plan.read_text(encoding="utf-8"))
        self.assertEqual(self.report.read_text(encoding="utf-8"), BLOCKED + "\n")
        self.assertEqual(json.loads(self.metrics.read_text(encoding="utf-8"))["usage"]["cached_input_tokens"], 200)

    def test_claude_fresh_process_and_usage(self):
        with patch.dict(runner.os.environ, {"CLAUDECODE": "1"}):
            call = self.run_review("claude", claude_result(CLEAR))
        command = call["command"]
        self.assertNotIn("CLAUDECODE", call["env"])
        self.assertIn("--safe-mode", command)
        self.assertIn("--strict-mcp-config", command)
        self.assertEqual(command[command.index("--tools") + 1], "")
        self.assertEqual(command[command.index("--effort") + 1], "medium")
        self.assertEqual(call["input"], "=== PLAN ===\n" + self.plan.read_text(encoding="utf-8"))
        self.assertEqual(self.report.read_text(encoding="utf-8"), CLEAR + "\n")
        self.assertEqual(json.loads(self.metrics.read_text(encoding="utf-8"))["usage"]["cache_read_input_tokens"], 80)

    def test_claude_resolved_model_and_cost_are_recorded(self):
        self.run_review("claude", claude_result(CLEAR, modelUsage={"claude-test-1": {}}, total_cost_usd=0.0123))
        saved = json.loads(self.metrics.read_text(encoding="utf-8"))
        self.assertEqual((saved["resolved_models"], saved["reported_cost_usd"]), (["claude-test-1"], 0.0123))

    def test_rejects_codex_tool_event(self):
        event = {"type": "item.completed", "item": {"type": "command_execution"}}
        with self.assertRaisesRegex(runner.ReviewError, "used a tool"):
            self.run_review("codex", codex_result(CLEAR, event))
        self.assertFalse(self.report.exists())
        self.assertFalse(self.metrics.exists())

    def test_rejects_truncated_codex_stream(self):
        stdout = '\n'.join(codex_result(CLEAR).splitlines()[:-1])
        with self.assertRaisesRegex(runner.ReviewError, "no completed critique"):
            self.run_review("codex", stdout)
        self.assertFalse(self.report.exists())
        self.assertFalse(self.metrics.exists())

    def test_rejects_claude_failure_and_extra_turn(self):
        for override in ({"is_error": True}, {"num_turns": 2}):
            with self.subTest(override=override), self.assertRaises(runner.ReviewError):
                self.run_review("claude", claude_result(CLEAR, **override))
        self.assertFalse(self.report.exists())
        self.assertFalse(self.metrics.exists())

    def test_rejects_malformed_and_inconsistent_critique(self):
        for answer in ("", "VERDICT: BLOCKED", BLOCKED.replace("### 1.", "### 3.")):
            with self.subTest(answer=answer), self.assertRaises(runner.ReviewError):
                runner.validate(answer)

    def test_slightly_long_review_passes_and_rejected_reply_is_kept(self):
        long = BLOCKED.replace("history.", "history. " + "word " * 250)  # about 270 words, as Claude returned live
        self.assertGreater(len(long.split()), 250)
        runner.validate(long)
        with self.assertRaises(runner.ReviewError):
            runner.validate(BLOCKED.replace("history.", "history. " + "word " * 400))
        with self.assertRaises(runner.ReviewError):
            self.run_review("claude", claude_result("VERDICT: BLOCKED"))
        self.assertFalse(self.report.exists())
        self.assertFalse(self.metrics.exists())
        self.assertEqual((self.project / "critique.rejected.txt").read_text(encoding="utf-8"), "VERDICT: BLOCKED")

    def test_closing_remark_is_dropped_but_a_later_issue_is_not(self):
        self.assertEqual(runner.validate(CLEAR + "\n\nThe plan is sound."), CLEAR + "\n")
        self.assertEqual(runner.validate(BLOCKED + "\n\nSteps 3 and 4 are fine."), BLOCKED + "\n")
        with self.assertRaises(runner.ReviewError):
            runner.validate(BLOCKED + "\nA remark.\n### 2. [minor] Lost\n- Failure: x\n- Fix: y")

    def test_login_failure_preserves_plan_and_hides_raw_output(self):
        plan_before = self.plan.read_bytes()
        with self.assertRaisesRegex(runner.ReviewError, "^claude requires sign-in$"):
            self.run_review("claude", "Not logged in · internal diagnostics", returncode=1)
        self.assertEqual(self.plan.read_bytes(), plan_before)
        self.assertFalse(self.report.exists())
        self.assertFalse(self.metrics.exists())

    def test_missing_cli_returns_actionable_message(self):
        with patch.object(runner.shutil, "which", return_value=None):
            with self.assertRaisesRegex(runner.ReviewError, "codex CLI not found on PATH"):
                runner.save_review("codex", self.plan, self.report)
        self.assertFalse(self.report.exists())

    def test_timeout_exits_without_artifacts(self):
        error = subprocess.TimeoutExpired("codex", runner.TIMEOUT)
        args = ["review.py", "codex", str(self.plan), str(self.report)]
        stderr = io.StringIO()
        with patch("sys.argv", args), patch("sys.stderr", stderr), patch.object(
            runner, "run_limited", side_effect=error
        ), patch.object(runner.shutil, "which", return_value="codex"):
            with self.assertRaises(SystemExit) as exit_info:
                runner.main()
        self.assertEqual(exit_info.exception.code, 1)
        self.assertIn("NOT CHALLENGED: codex timed out", stderr.getvalue())
        self.assertFalse(self.report.exists())
        self.assertFalse(self.metrics.exists())

    def test_timeout_also_stops_a_grandchild_that_holds_the_pipe(self):
        # The Windows .cmd shim case on any OS: the child exits only when killed, and its own
        # child keeps the output pipe open. Plain subprocess.run waited the full 30 s here.
        import sys
        from time import monotonic
        grandchild = "import subprocess, sys, time; subprocess.Popen([sys.executable, '-c', 'import time; time.sleep(30)']); time.sleep(30)"
        started = monotonic()
        with self.assertRaises(subprocess.TimeoutExpired):
            runner.run_limited([sys.executable, "-c", grandchild], input="", cwd=None, env=None, timeout=2)
        self.assertLess(monotonic() - started, 15)

    def test_input_limits_and_collision_stop_before_cli_call(self):
        for text in ("", "word " * 501, "é" * 2049):
            self.plan.write_text(text, encoding="utf-8")
            with patch.object(runner, "review") as invoke, self.assertRaises(runner.ReviewError):
                runner.save_review("codex", self.plan, self.report)
            invoke.assert_not_called()
        self.report.write_text("existing", encoding="utf-8")
        with patch.object(runner, "review") as invoke, self.assertRaisesRegex(runner.ReviewError, "already exists"):
            runner.save_review("codex", self.plan, self.report)
        invoke.assert_not_called()
        self.assertEqual(self.report.read_text(encoding="utf-8"), "existing")

    def test_seeded_plan_paths_fit_default_budget(self):
        for path in sorted((ROOT / "challenge/seeded-test").glob("plan-?.md")):
            with self.subTest(path=path):
                self.assertLessEqual(path.stat().st_size, 4096)
                self.assertLessEqual(len(path.read_text(encoding="utf-8").split()), 500)
