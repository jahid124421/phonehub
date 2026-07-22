#!/usr/bin/env python3
"""
PhoneHub pipeline — run every stage in order.
    python run_all.py                        # import -> content -> price -> build
    python run_all.py --skip-content         # e.g. refresh prices only
    python run_all.py --detect-new           # include new product detection
    python run_all.py --enrich-brands        # include brand enrichment
    python run_all.py --limit 50             # limit products processed (default: 100)
Stdlib only.
"""
import argparse
import subprocess
import sys
import os

HERE = os.path.dirname(os.path.abspath(__file__))
PY = sys.executable

# Steps whose failure should abort the pipeline (critical).
CRITICAL_STEPS = {"build.py"}

# Steps that are optional — failures are warnings, not fatal.
OPTIONAL_STEPS = {
    "content_agent.py",
    "price_job.py",
    "news_fetch.py",
    "brand_enricher.py",
    "new_product_detector.py",
}

failures = []  # list of (script, returncode)


def step(script, args=None):
    args = args or []
    print(f"\n=== {script} ===")
    r = subprocess.run([PY, os.path.join(HERE, script)] + args)
    if r.returncode != 0:
        if script in CRITICAL_STEPS:
            print(f"[run_all] CRITICAL: {script} failed (exit {r.returncode}). Aborting.")
            sys.exit(r.returncode)
        else:
            print(f"[WARN] {script} failed (exit {r.returncode}). Continuing.")
            failures.append((script, r.returncode))


def main():
    parser = argparse.ArgumentParser(description="Run the PhoneHub data pipeline.")
    parser.add_argument("--no-import", action="store_true", help="Skip live spec import")
    parser.add_argument("--skip-content", action="store_true", help="Skip content generation")
    parser.add_argument("--skip-news", action="store_true", help="Skip news fetching")
    parser.add_argument("--detect-new", action="store_true", help="Run new product detection")
    parser.add_argument("--enrich-brands", action="store_true", help="Run brand enrichment")
    parser.add_argument("--limit", type=int, default=100, help="Max products to process (default: 100)")
    args = parser.parse_args()

    if not args.no_import:      # dataset-seed mode skips live scraping
        step("import_specs.py")
    if not args.skip_content:
        content_args = []
        if args.limit != 100:
            content_args = ["--limit", str(args.limit)]
        step("content_agent.py", args=content_args)
    step("price_job.py")
    if not args.skip_news:
        step("news_fetch.py")
    # Optional stages (only run when explicitly requested)
    if args.detect_new:
        step("new_product_detector.py")
    if args.enrich_brands:
        step("brand_enricher.py")
    step("build.py")

    if failures:
        print("\n[run_all] === Failure Summary ===")
        for script, code in failures:
            print(f"  [WARN] {script} exited with code {code}")
        print(f"[run_all] {len(failures)} optional step(s) failed, but pipeline completed.")
    else:
        print("\n[run_all] done. Open index.html or serve the folder.")


if __name__ == "__main__":
    main()
