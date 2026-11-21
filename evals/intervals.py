"""Exact 95% intervals (Clopper-Pearson) for the pass counts reported in docs/portfolio-results.md.
Standard library only. Run from the repository root: python evals/intervals.py

The interval assumes independent trials. The two repeats of each plan or task are related, so the
true uncertainty is wider than printed here."""

from math import comb

# (what was counted, passes, trials), copied from the results page
COUNTS = [
    ("Outcome test, first builds that passed (each arm)", 12, 12),
    ("Planted blockers found (each reviewer)", 18, 18),
    ("Format check passed, Codex", 24, 24),
    ("Format check passed, Claude, main run", 21, 24),
    ("Format check passed, Claude, rerun with current validator", 24, 24),
    ("Planted flaws fixed by \"make it better\" (each arm)", 24, 24),
    ("Stakes rule correct (each model)", 10, 12),
    ("Reworded stakes rule correct (each model)", 16, 16),
    ("Two blind graders agreed on a Codex finding", 47, 55),
]


def tail_at_least(k, n, p):
    return sum(comb(n, i) * p**i * (1 - p) ** (n - i) for i in range(k, n + 1))


def exact_interval(k, n, confidence=0.95):
    """Clopper-Pearson interval for k passes in n trials, found by bisection on the binomial tail."""
    alpha = (1 - confidence) / 2

    def solve(target, rising):
        low, high = 0.0, 1.0
        for _ in range(60):
            mid = (low + high) / 2
            if (target(mid) < alpha) == rising:
                low = mid
            else:
                high = mid
        return (low + high) / 2

    lower = 0.0 if k == 0 else solve(lambda p: tail_at_least(k, n, p), True)
    upper = 1.0 if k == n else solve(lambda p: 1 - tail_at_least(k + 1, n, p), False)
    return lower, upper


if __name__ == "__main__":
    for label, k, n in COUNTS:
        lower, upper = exact_interval(k, n)
        print(f"{k:>2}/{n:<2}  {100 * lower:5.1f}% to {100 * upper:5.1f}%  {label}")
