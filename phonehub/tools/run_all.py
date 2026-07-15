#!/usr/bin/env python3
"""
PhoneHub pipeline — run every stage in order.
    python run_all.py            # import -> content -> price -> build
    python run_all.py --skip-content   # e.g. refresh prices only
Stdlib only.
"""
import subprocess
import sys
import os

HERE = os.path.dirname(os.path.abspath(__file__))
PY = sys.executable


def step(script, args=None):
    args = args or []
    print(f"\n=== {script} ===")
    r = subprocess.run([PY, os.path.join(HERE, script)] + args)
    if r.returncode != 0:
        print(f"[run_all] {script} failed (exit {r.returncode}). Stopping.")
        sys.exit(r.returncode)


def main():
    flags = sys.argv[1:]
    if "--no-import" not in flags:      # dataset-seed mode skips live scraping
        step("import_specs.py")
    if "--skip-content" not in flags:
        step("content_agent.py")
    step("price_job.py")
    if "--skip-news" not in flags:
        step("news_fetch.py")
    step("build.py")
    print("\n[run_all] done. Open index.html or serve the folder.")


if __name__ == "__main__":
    main()
