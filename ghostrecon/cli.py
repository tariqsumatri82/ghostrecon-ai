"""Command line interface for GhostRecon."""

from __future__ import annotations

import argparse
import os
import sys
import time
from typing import Dict, List, Optional, Sequence

from . import __version__
from .engine import FOUND, NOT_FOUND, UNKNOWN, Engine, Result, results_to_json
from .platforms import PLATFORMS

EXIT_OK = 0
EXIT_NO_RESULTS = 1
EXIT_USAGE = 2

_STATUS_TEXT = {FOUND: "FOUND", NOT_FOUND: "not found", UNKNOWN: "unknown"}


def _use_colour(stream) -> bool:
    if os.environ.get("NO_COLOR"):
        return False
    return hasattr(stream, "isatty") and stream.isatty()


_COLOURS = {FOUND: "\033[32m", NOT_FOUND: "\033[90m", UNKNOWN: "\033[33m"}


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="ghostrecon",
        description=(
            "Check whether a username exists on public platforms. "
            "Public profile pages only: no login, no paywall bypass, no auth."
        ),
        epilog="Run `ghostrecon --list-platforms` to see every platform and its URL pattern.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "-u", "--username", action="append", metavar="NAME",
        help="username to check (repeat the flag for several usernames)",
    )
    parser.add_argument(
        "-f", "--file", metavar="PATH",
        help="file with one username per line ('#' starts a comment)",
    )
    parser.add_argument(
        "-o", "--output", choices=("table", "json"), default="table",
        help="output format (default: table)",
    )
    parser.add_argument(
        "--only-found", action="store_true",
        help="print only the platforms where the username was found",
    )
    parser.add_argument(
        "--timeout", type=float, default=10.0, metavar="SECONDS",
        help="per-request timeout in seconds (default: 10)",
    )
    parser.add_argument(
        "-t", "--threads", type=int, default=10, metavar="N",
        help="number of concurrent workers (default: 10)",
    )
    parser.add_argument(
        "--rate-limit", type=float, default=0.5, metavar="SECONDS",
        help="minimum gap between requests to the same host (default: 0.5)",
    )
    parser.add_argument(
        "--category", action="append", metavar="NAME",
        help="only check platforms in this category (repeatable)",
    )
    parser.add_argument(
        "--platform", action="append", metavar="NAME",
        help="only check this platform by name (repeatable, case-insensitive)",
    )
    parser.add_argument(
        "--list-platforms", action="store_true",
        help="list the bundled platforms and exit",
    )
    parser.add_argument(
        "--verbose", action="store_true",
        help="log every check to stderr as it finishes",
    )
    parser.add_argument(
        "--quiet", action="store_true", help="suppress the summary line",
    )
    parser.add_argument(
        "-V", "--version", action="version", version="ghostrecon %s" % __version__,
    )
    return parser


def read_usernames(args) -> List[str]:
    names: List[str] = list(args.username or [])
    if args.file:
        try:
            with open(args.file, "r", encoding="utf-8") as handle:
                for line in handle:
                    line = line.split("#", 1)[0].strip()
                    if line:
                        names.append(line)
        except OSError as exc:
            raise SystemExit("ghostrecon: cannot read %s: %s" % (args.file, exc))
    seen, ordered = set(), []
    for name in names:
        name = name.strip()
        if name and name not in seen:
            seen.add(name)
            ordered.append(name)
    return ordered


def select_platforms(args) -> List[Dict]:
    platforms: Sequence[Dict] = PLATFORMS
    if args.platform:
        wanted = {p.lower() for p in args.platform}
        platforms = [p for p in platforms if p["name"].lower() in wanted]
    if args.category:
        wanted = {c.lower() for c in args.category}
        platforms = [p for p in platforms if p["category"].lower() in wanted]
    return list(platforms)


def _visible(results: Sequence[Result], only_found: bool) -> List[Result]:
    if not only_found:
        return list(results)
    return [r for r in results if r.status == FOUND]


def render_table(rows: Sequence[Result], colour: bool = False, show_url: bool = True) -> str:
    if not rows:
        return "No rows to display."
    headers = ("PLATFORM", "CATEGORY", "STATUS", "MS")
    if show_url:
        headers += ("URL",)
    body = []
    for row in rows:
        cells = [
            row.platform,
            row.category,
            _STATUS_TEXT.get(row.status, row.status),
            str(row.elapsed_ms),
        ]
        if show_url:
            cells.append(row.url)
        body.append(cells)
    widths = [len(h) for h in headers]
    for cells in body:
        for index, cell in enumerate(cells):
            widths[index] = max(widths[index], len(cell))
    lines = ["  ".join(h.ljust(widths[i]) for i, h in enumerate(headers)).rstrip()]
    lines.append("-" * (sum(widths) + 2 * (len(widths) - 1)))
    for cells in body:
        text = "  ".join(cell.ljust(widths[i]) for i, cell in enumerate(cells)).rstrip()
        if colour:
            tint = _COLOURS.get(row_status(cells, headers))
            if tint:
                text = "%s%s\033[0m" % (tint, text)
        lines.append(text)
    return "\n".join(lines)


def row_status(cells: Sequence[str], headers: Sequence[str]) -> Optional[str]:
    """Map the rendered status cell back to a status code (keeps colour logic simple)."""
    try:
        label = cells[headers.index("STATUS")]
    except (ValueError, IndexError):
        return None
    for status, text in _STATUS_TEXT.items():
        if text == label:
            return status
    return None


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.list_platforms:
        rows = [
            (p["name"], p["category"], p["url"])
            for p in sorted(PLATFORMS, key=lambda p: (p["category"], p["name"]))
        ]
        width = max(len(r[0]) for r in rows) if rows else 0
        for name, category, url in rows:
            print("%s  %-11s %s" % (name.ljust(width), category, url))
        print("\n%d platforms bundled." % len(PLATFORMS))
        return EXIT_OK

    usernames = read_usernames(args)
    if not usernames:
        parser.error("no username given: use -u/--username or -f/--file")
    platforms = select_platforms(args)
    if not platforms:
        parser.error("no platform matched --platform/--category")
    if args.threads < 1:
        parser.error("--threads must be at least 1")
    if args.timeout <= 0:
        parser.error("--timeout must be greater than 0")

    engine = Engine(
        timeout=args.timeout,
        threads=args.threads,
        rate_limit=args.rate_limit,
        verbose=args.verbose,
        log=lambda message: print(message, file=sys.stderr),
    )

    colour = args.output == "table" and _use_colour(sys.stdout)
    payloads = []
    conclusive = 0
    for username in usernames:
        started = time.monotonic()
        results = engine.run(username, platforms)
        elapsed_ms = int((time.monotonic() - started) * 1000)
        conclusive += sum(1 for r in results if r.status in (FOUND, NOT_FOUND))
        payloads.append((username, results, elapsed_ms))
        if args.output == "table":
            rows = _visible(results, args.only_found)
            print("== %s ==" % username)
            print(render_table(rows, colour=colour))
            if not args.quiet:
                found = [r for r in results if r.status == FOUND]
                unknown = [r for r in results if r.status == UNKNOWN]
                print(
                    "%d checked, %d found, %d unknown in %.1fs"
                    % (len(results), len(found), len(unknown), elapsed_ms / 1000.0)
                )
                print("")
        else:
            print(results_to_json(username, results, elapsed_ms))

    if args.output == "json":
        return EXIT_OK if conclusive else EXIT_NO_RESULTS
    return EXIT_OK if conclusive else EXIT_NO_RESULTS


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
