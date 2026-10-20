"""Command line.

    python -m synthtool [--profile FILE] [--out DIR] [--seed N] [--report-only]    generate + realism report
    python -m synthtool benchmark --real DIR --synthetic DIR [...]                  compare with a real client
"""
from __future__ import annotations

import argparse
import json
import sys
import time

from .config import load_profile
from .generate import generate
from .qa import write_report


def main(argv=None):
    argv = sys.argv[1:] if argv is None else list(argv)
    if argv and argv[0] == "benchmark":
        from .benchmark import main as bench
        return bench(argv[1:])
    ap = argparse.ArgumentParser(prog="synthtool", description="Generate a synthetic warehouse dataset with an "
                                 "answer key. ('synthtool benchmark -h' compares one with a real client.)")
    ap.add_argument("--profile", help="YAML profile (defaults are used for anything missing)")
    ap.add_argument("--out", default="data/synthetic/default")
    ap.add_argument("--seed", type=int)
    ap.add_argument("--report-only", action="store_true", help="re-run the realism report on an existing folder")
    a = ap.parse_args(argv)
    t = time.time()
    if not a.report_only:
        kw = {"seed": a.seed} if a.seed is not None else {}
        m = generate(load_profile(a.profile, **kw), a.out)
        print(json.dumps(m["counts"], indent=2))
    path = write_report(a.out)
    print(f"report: {path}  ({time.time() - t:.1f}s)")


if __name__ == "__main__":
    main()
