#!/usr/bin/env python3
"""Live verification harness for the bundled platform checks.

A platform definition only earns a place in `ghostrecon/platforms.py` if it
passes both halves of this test, against the real internet:

  phase 1 (discriminates)  two improbable usernames must both come back
                           `not_found` — a check that answers "found" for a
                           random string is measuring nothing;
  phase 2 (positive path)  at least one well-known username must come back
                           `found` — a check that answers "not_found" for
                           everybody is equally useless.

Anything that cannot be shown to do both is dropped.

Usage:
    python3 tools/verify_platforms.py                      # full report
    python3 tools/verify_platforms.py --json verification.json
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from concurrent.futures import ThreadPoolExecutor
from typing import Dict, List

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ghostrecon.candidates import CANDIDATES  # noqa: E402
from ghostrecon.engine import FOUND, NOT_FOUND, Engine  # noqa: E402

#: Improbable usernames. Both must return "not found" for a check to be trusted.
PROBES = ["zzq7x9v2klm4p8t", "ghostreconprobe9917xq"]

#: Well-known usernames. One "found" is enough to prove the positive path works.
KNOWN = [
    "torvalds", "sindresorhus", "kevinmitnick", "tariqsumatri",
    "gvanrossum", "nasa", "test", "john", "admin", "hello",
]

KNOWN_ATTEMPTS = 6


def probe_phase(engine: "Engine", platform: Dict) -> Dict:
    row = {
        "name": platform["name"],
        "category": platform["category"],
        "url": platform["url"],
        "probes": {},
        "discriminates": True,
        "verdict": "",
        "positive_with": "",
    }
    for probe in PROBES:
        result = engine.check_platform(platform, probe)
        row["probes"][probe] = {
            "status": result.status,
            "code": result.http_code,
            "detail": result.detail,
        }
        if result.status != NOT_FOUND:
            row["discriminates"] = False
    return row


def positive_phase(engine: "Engine", platform: Dict, row: Dict) -> Dict:
    for username in KNOWN[:KNOWN_ATTEMPTS]:
        result = engine.check_platform(platform, username)
        if result.status == FOUND:
            row["verdict"] = "verified"
            row["positive_with"] = username
            return row
    row["verdict"] = "no positive probe"
    return row


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", metavar="PATH", help="write the full report as JSON")
    parser.add_argument("--threads", type=int, default=24)
    parser.add_argument("--timeout", type=float, default=12.0)
    args = parser.parse_args()

    engine = Engine(timeout=args.timeout, threads=1, rate_limit=0.2)

    def say(message: str) -> None:
        print(message, flush=True)

    say("phase 1/2: %d candidates x %d improbable probes" % (len(CANDIDATES), len(PROBES)))
    report: List[Dict] = []
    with ThreadPoolExecutor(max_workers=args.threads) as pool:
        for row in pool.map(lambda p: probe_phase(engine, p), CANDIDATES):
            report.append(row)
            if not row["discriminates"]:
                say("  FAIL %s (probe answered %s)" % (
                    row["name"], "/".join(r["status"] for r in row["probes"].values())))

    survivors = [row for row in report if row["discriminates"]]
    by_name = {p["name"]: p for p in CANDIDATES}
    say("\nphase 1 survived: %d of %d" % (len(survivors), len(CANDIDATES)))
    say("phase 2/2: looking for a real profile on each survivor")

    with ThreadPoolExecutor(max_workers=args.threads) as pool:
        futures = [pool.submit(positive_phase, engine, by_name[row["name"]], row)
                   for row in survivors]
        done = 0
        for future in futures:
            row = future.result()
            done += 1
            if row["verdict"] == "verified":
                say("  verified %-22s as %s" % (row["name"], row["positive_with"]))
            else:
                say("  DROP     %-22s (no known profile found)" % row["name"])
            print("\rprogress %d/%d" % (done, len(survivors)), end="", file=sys.stderr, flush=True)

    verified = [row for row in report if row["verdict"] == "verified"]
    say("\nverified: %d of %d candidates" % (len(verified), len(CANDIDATES)))
    say("names: %s" % ", ".join(sorted(r["name"] for r in verified)))

    if args.json:
        with open(args.json, "w", encoding="utf-8") as handle:
            json.dump({"probes": PROBES, "known": KNOWN, "report": report}, handle, indent=2)
        say("wrote %s" % args.json)
    return 0


if __name__ == "__main__":
    sys.exit(main())
