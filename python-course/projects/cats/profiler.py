"""Fair profiler for cats diff functions.

Fixes vs the old version:
  - Old code printed ``fn.__name__``: every ``@memo_diff`` function shows up
    as ``"memoized"`` (no ``functools.wraps``), so you couldn't tell
    minimum_mewtations apart from final_diff. We now use explicit labels.
    (We deliberately do NOT add functools.wraps in cats.py: tests/EC.py
    asserts the wrapper is named 'memoized'.)
  - Old code ran ``repeats=5`` over the same workload with a shared,
    never-cleared cache and only warmed up final_diff. Median was then
    dominated by warm cache hits while total was dominated by first-pass
    misses, and ``real`` polluted ``wrong``. We now clear caches before
    each bench and report cold (pass 0) vs warm (passes 1+) separately.
  - Old ``total`` was wall time including loop overhead and ``p95`` had an
    off-by-one. We report sum-of-call-times plus proper percentiles.
"""
import argparse
import gc
import pickle
import random
import statistics
import time
from typing import Callable, Dict, List, Sequence, Tuple

import cats


# ---------------------------------------------------------------------------
# cache helpers (no changes to cats.py needed)
# ---------------------------------------------------------------------------

def clear_cache(fn: Callable) -> int:
    """Clear any dict found in fn's closure cells (memo/memo_diff caches).

    Returns number of entries cleared. Also resets call_count if present
    (utils.count wrapper).
    """
    cleared = 0
    for cell in getattr(fn, "__closure__", None) or []:
        try:
            contents = cell.cell_contents
        except ValueError:
            continue
        if isinstance(contents, dict):
            cleared += len(contents)
            contents.clear()
    if hasattr(fn, "call_count"):
        fn.call_count = 0
    # memo_diff wraps diff_function which may itself be counted/wrapped;
    # recurse one level so call_count resets propagate.
    for cell in getattr(fn, "__closure__", None) or []:
        try:
            contents = cell.cell_contents
        except ValueError:
            continue
        if callable(contents) and hasattr(contents, "call_count"):
            contents.call_count = 0
    return cleared


def cache_size(fn: Callable) -> int:
    n = 0
    for cell in getattr(fn, "__closure__", None) or []:
        try:
            contents = cell.cell_contents
        except ValueError:
            continue
        if isinstance(contents, dict):
            n += len(contents)
    return n


def describe(fn: Callable, label: str) -> str:
    # Show explicit label plus real __name__ for debugging collisions.
    return f"{label} (as {getattr(fn, '__name__', '?')})" if getattr(fn, "__name__", label) != label else label


# ---------------------------------------------------------------------------
# bench core
# ---------------------------------------------------------------------------

def _stats(samples: List[float]) -> Dict:
    if not samples:
        return {"n": 0, "total": 0.0, "mean": 0.0, "median": 0.0,
                "p95": 0.0, "max": 0.0, "thr": 0.0}
    s = sorted(samples)
    n = len(s)
    total = sum(s)
    # nearest-rank percentile
    p95 = s[min(n - 1, max(0, int(n * 0.95 + 0.5) - 1))]
    return {
        "n": n,
        "total": total,
        "mean": total / n,
        "median": statistics.median(s),
        "p95": p95,
        "max": s[-1],
        "thr": n / total if total > 0 else 0.0,
    }


def bench_cold_warm(fn: Callable, workload: Sequence[tuple],
                    repeats: int = 5, clear: bool = True) -> Dict:
    """Run workload `repeats` times. Pass 0 = cold, passes 1+ = warm.

    Cache is cleared once up front (if clear=True) so cold is truly cold
    and warm hits stay within this bench only.
    """
    if clear:
        clear_cache(fn)
    cold: List[float] = []
    warm: List[float] = []
    gc_was_enabled = gc.isenabled()
    gc.disable()
    try:
        for r in range(repeats):
            for args in workload:
                t = time.perf_counter()
                fn(*args)
                dt = time.perf_counter() - t
                (cold if r == 0 else warm).append(dt)
    finally:
        if gc_was_enabled:
            gc.enable()
    return {"cold": _stats(cold), "warm": _stats(warm) if warm else _stats([]),
            "cache_entries": cache_size(fn)}


def fmt_ms(x: float) -> str:
    return f"{x * 1e3:8.4f}ms"


def load_workloads(seed: int = 0, limit: int = None, autocorrect_n: int = 100,
                   autocorrect_words: int = None):
    with open("data/testcases.out", "rb") as f:
        test_dict = pickle.load(f)
    correct_words = list(test_dict.keys())
    random.seed(seed)
    random.shuffle(correct_words)
    lim = cats.FINAL_DIFF_LIMIT if limit is None else limit
    real_pairs = [(typo, correct, lim)
                  for correct, typos in test_dict.items()
                  for typo in typos]
    wrong_pairs = []
    for i, (correct, typos) in enumerate(test_dict.items()):
        other = correct_words[(i * 7 + 1) % len(correct_words)]
        if other == correct:
            other = correct_words[(i * 7 + 2) % len(correct_words)]
        wrong_pairs += [(typo, other, lim) for typo in typos]
    return test_dict, correct_words, real_pairs, wrong_pairs


def main() -> None:
    ap = argparse.ArgumentParser(description="Fair cats diff profiler (cold vs warm).")
    ap.add_argument("--repeats", type=int, default=5, help="passes per bench (1 cold + rest warm)")
    ap.add_argument("--sample", type=int, default=0, help="use only first N pairs per workload (0=all)")
    ap.add_argument("--limit", type=int, default=None, help="override diff limit (default FINAL_DIFF_LIMIT)")
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--no-clear", action="store_true", help="do NOT clear caches between benches (old behavior)")
    ap.add_argument("--autocorrect-n", type=int, default=20,
                    help="end-to-end autocorrect calls to bench (0 to skip)")
    args = ap.parse_args()

    _, correct_words, real_pairs, wrong_pairs = load_workloads(seed=args.seed, limit=args.limit)
    if args.sample:
        real_pairs = real_pairs[:args.sample]
        wrong_pairs = wrong_pairs[:args.sample]
    clear = not args.no_clear
    lim = cats.FINAL_DIFF_LIMIT if args.limit is None else args.limit
    print(f"limit={lim} pairs real={len(real_pairs)} wrong={len(wrong_pairs)} "
          f"repeats={args.repeats} clear_cache={clear} seed={args.seed}")

    # Explicit labels: __name__ collides for @memo_diff wrappers ("memoized").
    diffs: List[Tuple[str, Callable]] = [
        ("furry_fixes", cats.furry_fixes),
        ("minimum_mewtations", cats.minimum_mewtations),
        ("final_diff", cats.final_diff),
    ]
    for fn_label, fn in diffs:
        if getattr(fn, "__name__", "") != fn_label:
            print(f"note: {fn_label} has __name__={getattr(fn, '__name__', '?')!r} "
                  f"(memo wrapper) -- using explicit label")

    header = (f"{'workload':6s} {'fn':20s} {'pass':5s} "
              f"{'total':>12s} {'mean':>12s} {'median':>12s} {'p95':>12s} {'max':>12s} {'thr/s':>10s} {'n':>6s}")
    print(header)
    print("-" * len(header))
    for wl_label, wl in [("real", real_pairs), ("wrong", wrong_pairs)]:
        for fn_label, fn in diffs:
            r = bench_cold_warm(fn, wl, repeats=args.repeats, clear=clear)
            for pass_label in ("cold", "warm"):
                s = r[pass_label]
                print(f"{wl_label:6s} {fn_label:20s} {pass_label:5s} "
                      f"{fmt_ms(s['total']):>12s} {fmt_ms(s['mean']):>12s} "
                      f"{fmt_ms(s['median']):>12s} {fmt_ms(s['p95']):>12s} "
                      f"{fmt_ms(s['max']):>12s} {s['thr']:10.1f} {s['n']:6d}")

    # End-to-end: autocorrect over the full word list (the real use case).
    if args.autocorrect_n:
        from cats import autocorrect
        typos = [t for t, _, _ in real_pairs[:args.autocorrect_n]]
        print(f"\nautocorrect end-to-end: {len(typos)} typos x {len(correct_words)} words, limit={lim}")
        for fn_label, fn in diffs:
            if clear:
                clear_cache(fn)
            t0 = time.perf_counter()
            for t in typos:
                autocorrect(t, correct_words, fn, lim)
            dt = time.perf_counter() - t0
            print(f"  {fn_label:20s} total={dt * 1e3:8.2f}ms per-typo={dt / max(1, len(typos)) * 1e3:8.2f}ms")


if __name__ == "__main__":
    main()
