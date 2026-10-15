#!/usr/bin/env python3
"""Generate `ghostrecon/platforms.py` from `ghostrecon/candidates.py`.

With no verification report this tool ships every candidate (development mode).
With `--report report.json` it ships only the candidates that
`tools/verify_platforms.py` proved both discriminate and reach a real profile.
That is the mode used for a release, so the count in the README is true.

Usage:
    python3 tools/build_platforms.py                                  # all candidates
    python3 tools/build_platforms.py --report verification.json        # verified only
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

HEADER = '''"""Platform definitions.

Every entry here was checked against the live internet with
`python3 tools/verify_platforms.py`; tools/verification_report.txt records the raw evidence.
Adding a platform is a one-line change to this list and nothing else.

Fields:
    name, category, url   required; url contains the {username} placeholder
    check                 "status" (default) or "marker"
    found_codes           HTTP codes meaning "profile exists"   (default (200,))
    missing_codes         HTTP codes meaning "no profile"       (default (404,))
    missing_markers       page text meaning "no profile" even on HTTP 200
    found_markers         page text that must appear for 200 to mean "found"
    note                  caveat shown in --verbose and JSON output
"""

PLATFORMS = [
'''


def load_candidates():
    path = os.path.join(ROOT, "ghostrecon", "candidates.py")
    spec = importlib.util.spec_from_file_location("_candidates", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.CANDIDATES


def render(platforms) -> str:
    out = [HEADER]
    for platform in platforms:
        out.append("    {\n")
        for key, value in platform.items():
            if key in ("missing_markers", "found_markers", "note") and not value:
                continue
            if key == "found_codes" and value == [200]:
                continue
            if key == "missing_codes" and value == [404]:
                continue
            if key == "check" and value == "status":
                continue
            out.append("        %r: %r,\n" % (key, value))
        out.append("    },\n")
    out.append("]\n")
    return "".join(out)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--report", help="verification JSON from verify_platforms.py")
    parser.add_argument("--out", default=os.path.join(ROOT, "ghostrecon", "platforms.py"))
    args = parser.parse_args()

    platforms = load_candidates()
    if args.report:
        with open(args.report, encoding="utf-8") as handle:
            report = json.load(handle)["report"]
        verified = {row["name"] for row in report
                    if row["verdict"] == "verified" and row["discriminates"]}
        platforms = [p for p in platforms if p["name"] in verified]
        missing = verified - {p["name"] for p in platforms}
        if missing:
            print("warning: verified but not in candidates.py: %s" % sorted(missing),
                  file=sys.stderr)

    with open(args.out, "w", encoding="utf-8") as handle:
        handle.write(render(platforms))
    print("wrote %s with %d platforms" % (args.out, len(platforms)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
