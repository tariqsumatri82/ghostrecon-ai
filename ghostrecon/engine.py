"""Threaded, polite, standard-library-only HTTP checking engine.

No third-party dependencies, no authentication, no attempt to get around a
login wall or a paywall. Every check is a plain GET of a public profile page.
"""

from __future__ import annotations

import json
import threading
import time
import urllib.error
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from typing import Dict, Iterable, List, Optional, Sequence

FOUND = "found"
NOT_FOUND = "not_found"
UNKNOWN = "unknown"

#: Honest, contactable User-Agent — the tool identifies itself.
USER_AGENT = (
    "GhostRecon/1.0 (public-username availability checker; "
    "+https://github.com/tariqsumatri82/ghostrecon-ai)"
)

#: Responses above this size are truncated: we only need the markers.
MAX_BODY_BYTES = 200_000

BLOCKING_CODES = (401, 403, 429, 451)


@dataclass
class Result:
    """Outcome of a single platform check."""

    platform: str
    category: str
    url: str
    status: str
    http_code: Optional[int] = None
    elapsed_ms: int = 0
    detail: str = ""
    note: str = ""

    @property
    def found(self) -> bool:
        return self.status == FOUND

    def as_dict(self) -> Dict[str, object]:
        return {
            "platform": self.platform,
            "category": self.category,
            "url": self.url,
            "status": self.status,
            "http_code": self.http_code,
            "elapsed_ms": self.elapsed_ms,
            "detail": self.detail,
            "note": self.note,
        }


class HostPacer:
    """Enforces a minimum gap between requests to the same host.

    Keeps the tool polite on multi-platform runs and keeps one slow site from
    being hammered when several definitions share a host.
    """

    def __init__(self, min_interval: float = 0.5) -> None:
        self.min_interval = max(0.0, float(min_interval))
        self._lock = threading.Lock()
        self._next_start: Dict[str, float] = {}

    def wait(self, host: str) -> None:
        if self.min_interval <= 0:
            return
        while True:
            with self._lock:
                now = time.monotonic()
                nxt = self._next_start.get(host, 0.0)
                if now >= nxt:
                    self._next_start[host] = now + self.min_interval
                    return
                delay = nxt - now
            time.sleep(min(delay, 0.25))


class Engine:
    """Runs platform checks concurrently and classifies each response."""

    def __init__(
        self,
        timeout: float = 10.0,
        threads: int = 10,
        rate_limit: float = 0.5,
        user_agent: str = USER_AGENT,
        verbose: bool = False,
        log=None,
    ) -> None:
        self.timeout = float(timeout)
        self.threads = max(1, int(threads))
        self.rate_limit = float(rate_limit)
        self.user_agent = user_agent
        self.verbose = verbose
        self._log = log
        self.pacer = HostPacer(self.rate_limit)

    # -- logging -----------------------------------------------------------
    def _emit(self, message: str) -> None:
        if self._log is not None:
            self._log(message)

    # -- network -----------------------------------------------------------
    def _fetch(self, url: str):
        """Return (status_code, body_text, final_url). Raises on transport errors."""
        request = urllib.request.Request(
            url,
            headers={
                "User-Agent": self.user_agent,
                "Accept": "text/html,application/json;q=0.9,*/*;q=0.8",
                "Accept-Language": "en-US,en;q=0.9",
            },
        )
        with urllib.request.urlopen(request, timeout=self.timeout) as response:
            raw = response.read(MAX_BODY_BYTES)
            code = getattr(response, "status", 200) or 200
            return code, raw.decode("utf-8", "replace"), response.geturl()

    # -- classification ----------------------------------------------------
    def _classify(self, platform: Dict, code: Optional[int], body: str, error: str):
        if code is None:
            return UNKNOWN, error or "request failed"
        if code in tuple(platform.get("missing_codes", (404,))):
            return NOT_FOUND, "HTTP %d" % code
        if code in tuple(platform.get("found_codes", (200,))):
            low = body.lower()
            for marker in platform.get("missing_markers", ()):  # not-found page
                if marker.lower() in low:
                    return NOT_FOUND, "HTTP %d, page says no such profile" % code
            required = tuple(platform.get("found_markers", ()))
            if required and not any(m.lower() in low for m in required):
                return UNKNOWN, "HTTP %d, expected profile marker absent" % code
            return FOUND, "HTTP %d" % code
        if code in BLOCKING_CODES:
            return UNKNOWN, "HTTP %d, blocked or rate limited" % code
        if code >= 500:
            return UNKNOWN, "HTTP %d, server error" % code
        return UNKNOWN, "HTTP %d, inconclusive" % code

    # -- single check ------------------------------------------------------
    def check_platform(self, platform: Dict, username: str) -> Result:
        url = platform["url"].format(username=urllib.parse.quote(username, safe=""))
        host = urllib.parse.urlsplit(url).hostname or ""
        started = time.monotonic()
        self.pacer.wait(host)
        code: Optional[int] = None
        body = ""
        error = ""
        try:
            code, body, _final = self._fetch(url)
        except urllib.error.HTTPError as exc:
            code = exc.code
            try:
                body = exc.read(MAX_BODY_BYTES).decode("utf-8", "replace")
            except Exception:  # pragma: no cover - body already consumed/closed
                body = ""
        except Exception as exc:
            error = "%s: %s" % (type(exc).__name__, exc)

        status, detail = self._classify(platform, code, body, error)
        elapsed = int((time.monotonic() - started) * 1000)
        result = Result(
            platform=platform["name"],
            category=platform.get("category", "other"),
            url=url,
            status=status,
            http_code=code,
            elapsed_ms=elapsed,
            detail=detail,
            note=platform.get("note", ""),
        )
        if self.verbose:
            self._emit(
                "%-22s %-9s %-4s %5dms  %s"
                % (result.platform, result.status, code if code else "-", elapsed, detail)
            )
        return result

    # -- batch -------------------------------------------------------------
    def run(self, username: str, platforms: Sequence[Dict]) -> List[Result]:
        results: List[Optional[Result]] = [None] * len(platforms)
        if not platforms:
            return []
        with ThreadPoolExecutor(max_workers=self.threads) as pool:
            futures = {
                pool.submit(self.check_platform, platform, username): index
                for index, platform in enumerate(platforms)
            }
            for future in futures:
                pass
            for future, index in list(futures.items()):
                try:
                    results[index] = future.result()
                except Exception as exc:  # pragma: no cover - defensive
                    platform = platforms[index]
                    results[index] = Result(
                        platform=platform["name"],
                        category=platform.get("category", "other"),
                        url=platform["url"].format(username=username),
                        status=UNKNOWN,
                        detail="worker error: %s" % exc,
                    )
        return [r for r in results if r is not None]


def results_to_json(username: str, results: Iterable[Result], elapsed_ms: int = 0) -> str:
    """Serialise a run to JSON, leaving out nothing that the run produced."""
    results = list(results)
    payload = {
        "tool": "ghostrecon",
        "username": username,
        "checked": len(results),
        "found": sum(1 for r in results if r.status == FOUND),
        "not_found": sum(1 for r in results if r.status == NOT_FOUND),
        "unknown": sum(1 for r in results if r.status == UNKNOWN),
        "elapsed_ms": elapsed_ms,
        "results": [r.as_dict() for r in results],
    }
    return json.dumps(payload, indent=2, ensure_ascii=False)
