import importlib.util
import json
from pathlib import Path
import re
import subprocess
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch


HERE = Path(__file__).resolve().parents[1] / "evals/plan-review"


def load_script(name):
    spec = importlib.util.spec_from_file_location(name, HERE / f"{name}.py")
    script = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(script)
    return script


class BenchmarkTests(unittest.TestCase):
    def setUp(self):
        self.key = [
            json.loads(line)
            for line in (HERE / "answer-key.jsonl").read_text(encoding="utf-8").splitlines()
        ]

    def test_each_pair_repairs_only_the_seeded_steps(self):
        groups = {}
        for row in self.key:
            groups.setdefault(row["pair"], []).append(row)
        self.assertEqual(len(groups), 6)
        for rows in groups.values():
            flawed, control = sorted(rows, key=lambda row: len(row["seeds"]), reverse=True)
            self.assertEqual(len(flawed["seeds"]), 2)
            self.assertFalse(control["seeds"])
            self.assertEqual(flawed["split"], control["split"])
            steps = []
            for row in (flawed, control):
                path = HERE / "plans" / f"{row['id']}.md"
                plan = path.read_text(encoding="utf-8")
                self.assertLessEqual(path.stat().st_size, 4096)
                self.assertLessEqual(len(plan.split()), 500)
                steps.append(dict(re.findall(r"^([0-9]+)\. (.+)", plan, re.M)))
            self.assertEqual(steps[0].keys(), steps[1].keys())
            changed = {int(step) for step in steps[0] if steps[0][step] != steps[1][step]}
            self.assertEqual(changed, {seed["step"] for seed in flawed["seeds"]})

    def test_benchmark_call_budget_and_repeat_balance(self):
        runner = load_script("run_benchmark")
        smoke = runner.collect_jobs("smoke", self.key)
        full = runner.collect_jobs("full", self.key)
        self.assertEqual(len(set(smoke)), 12)
        self.assertEqual(len(set(full)), 48)
        self.assertEqual({case for case, _, _ in smoke}, {row["id"] for row in self.key if row["split"] == "smoke"})
        self.assertEqual(sum(provider == "codex" for _, provider, _ in full), 24)
        one = runner.collect_jobs("full", self.key, ("claude",))
        self.assertEqual((len(one), {provider for _, provider, _ in one}), (24, {"claude"}))

    def test_historical_calculation_matches_archive(self):
        metrics = load_script("historical_summary").summarize()
        findings = metrics["historical_accepted_findings"]
        self.assertEqual((findings["accepted_union"], findings["codex"], findings["claude"]), (20, 6, 18))
        self.assertEqual((findings["shared"], findings["codex_only"], findings["claude_only"]), (4, 2, 14))
        self.assertEqual(metrics["historical_seeded_token_ratio_claude_to_codex"], 7.59)

    def test_setup_failure_stops_batch_and_records_attempt(self):
        runner = load_script("run_benchmark")
        with tempfile.TemporaryDirectory() as directory:
            args = SimpleNamespace(
                out=Path(directory) / "runs", suite="smoke", codex_model=None, claude_model=None, effort=None,
            )
            result = subprocess.CompletedProcess([], 1, "", "NOT CHALLENGED: codex requires sign-in")
            with patch.object(runner, "version", return_value="test"), patch.object(
                runner.subprocess, "run", return_value=result,
            ) as invoke, patch("sys.stderr"):
                self.assertEqual(runner.collect(args, runner.collect_jobs("smoke", self.key)), 1)
            invoke.assert_called_once()
            manifest = json.loads((args.out / "manifest.json").read_text(encoding="utf-8"))
            attempts = (args.out / "runs.jsonl").read_text(encoding="utf-8").splitlines()
            self.assertEqual(manifest["planned_calls"], 12)
            self.assertEqual((manifest["timeout_s"], manifest["effort"]), (180, {"claude": "medium", "codex": "low"}))
            self.assertEqual(len(attempts), 1)
            self.assertFalse(json.loads(attempts[0])["ok"])

    def test_scoring_counts_misses_failed_runs_and_routing(self):
        score = load_script("score")
        key = [
            {"id": "a", "pair": "money", "seeds": [{"id": "s1", "severity": "blocker"}, {"id": "s2", "severity": "major"}]},
            {"id": "b", "pair": "money", "seeds": []},
        ]

        def attempt(provider, case, blind_id, ok=True):
            usage = {"provider": provider, "requested_model": None, "wall_ms": 1000, "usage": (
                {"input_tokens": 100, "cached_input_tokens": 60, "output_tokens": 10} if provider == "codex"
                else {"input_tokens": 40, "cache_read_input_tokens": 60, "output_tokens": 10})}
            return {"provider": provider, "case": case, "repeat": 1, "ok": ok, "blind_id": blind_id, "usage": usage if ok else None}

        attempts = [attempt("codex", "a", "c1"), attempt("codex", "b", "c2"), attempt("claude", "a", "c3"), attempt("claude", "b", None, ok=False)]
        judgments = [
            {"blind_id": "c1", "matched_seeds": ["s2"], "judgment": "seed"},
            {"blind_id": "c2", "matched_seeds": [], "judgment": "repaired-claim"},
            {"blind_id": "c3", "matched_seeds": ["s1", "s2"], "judgment": "seed"},
            {"blind_id": "c3", "matched_seeds": [], "judgment": "valid"},
        ]
        reviewers, policies = score.summarize(attempts, judgments, key, {"money": "consequential"})
        self.assertEqual((reviewers["codex"]["blockers"], reviewers["codex"]["seeds"], reviewers["codex"]["controls"]), ([0, 1, 1], [1, 2, 2], [1, 1]))
        self.assertEqual((reviewers["claude"]["completed"], reviewers["claude"]["attempted"], reviewers["claude"]["novel"]["valid"]), (1, 2, 1))
        self.assertEqual(reviewers["codex"]["tokens"][0], (40, 60, 0, 10))  # same four fields for both CLIs
        self.assertEqual(reviewers["claude"]["tokens"][0], (40, 60, 0, 10))
        self.assertEqual(policies["always codex"]["consequential_blocker_misses"], 1)
        self.assertEqual((policies["routing rule"]["blockers"], policies["routing rule"]["failed"]), ([1, 1], 1))
        self.assertEqual((policies["both"]["calls"], policies["both"]["tokens"]), (4, 330))
