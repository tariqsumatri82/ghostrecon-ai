"""Unit tests. No network access: the transport layer is replaced by a stub."""

import io
import json
import os
import re
import sys
import unittest
import urllib.error
from contextlib import redirect_stdout

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ghostrecon import cli, engine  # noqa: E402
from ghostrecon.engine import FOUND, NOT_FOUND, UNKNOWN, Engine, results_to_json  # noqa: E402
from ghostrecon.platforms import PLATFORMS  # noqa: E402


class StubEngine(Engine):
    """Engine whose transport returns canned responses keyed by URL substring."""

    def __init__(self, responses, **kwargs):
        kwargs.setdefault("rate_limit", 0)
        super().__init__(**kwargs)
        self.responses = responses
        self.calls = []

    def _fetch(self, url):
        self.calls.append(url)
        for needle, value in self.responses.items():
            if needle in url:
                if isinstance(value, int):
                    body = ""
                    raise urllib.error.HTTPError(url, value, "stub", {}, io.BytesIO(body.encode()))
                return value
        return (200, "<html>ok</html>", url)


class ClassifyTests(unittest.TestCase):
    def test_status_check_200_is_found(self):
        platform = {"name": "X", "category": "c", "url": "https://x/{username}"}
        eng = Engine()
        self.assertEqual(eng._classify(platform, 200, "", "")[0], FOUND)

    def test_status_check_404_is_not_found(self):
        platform = {"name": "X", "category": "c", "url": "https://x/{username}"}
        eng = Engine()
        self.assertEqual(eng._classify(platform, 404, "", "")[0], NOT_FOUND)

    def test_blocking_code_is_unknown(self):
        platform = {"name": "X", "category": "c", "url": "https://x/{username}"}
        eng = Engine()
        for code in (401, 403, 429, 451, 503):
            self.assertEqual(eng._classify(platform, code, "", "")[0], UNKNOWN, code)

    def test_transport_error_is_unknown(self):
        platform = {"name": "X", "category": "c", "url": "https://x/{username}"}
        eng = Engine()
        status, detail = eng._classify(platform, None, "", "URLError: boom")
        self.assertEqual(status, UNKNOWN)
        self.assertIn("boom", detail)

    def test_missing_marker_beats_200(self):
        platform = {"name": "X", "category": "c", "url": "https://x/{username}",
                    "check": "marker", "missing_markers": ["no such user"]}
        eng = Engine()
        self.assertEqual(eng._classify(platform, 200, "No Such User", "")[0], NOT_FOUND)
        self.assertEqual(eng._classify(platform, 200, "profile page", "")[0], FOUND)

    def test_required_found_marker_absent_is_unknown(self):
        platform = {"name": "X", "category": "c", "url": "https://x/{username}",
                    "found_markers": ["og:title"]}
        eng = Engine()
        self.assertEqual(eng._classify(platform, 200, "nothing here", "")[0], UNKNOWN)
        self.assertEqual(eng._classify(platform, 200, "<meta og:title=...>", "")[0], FOUND)

    def test_custom_missing_code(self):
        platform = {"name": "X", "category": "c", "url": "https://x/{username}",
                    "missing_codes": (400, 404)}
        eng = Engine()
        self.assertEqual(eng._classify(platform, 400, "", "")[0], NOT_FOUND)


class EngineRunTests(unittest.TestCase):
    platforms = [
        {"name": "Alpha", "category": "dev", "url": "https://alpha.test/{username}"},
        {"name": "Beta", "category": "dev", "url": "https://beta.test/{username}",
         "check": "marker", "missing_markers": ["not found"]},
        {"name": "Gamma", "category": "social", "url": "https://gamma.test/{username}"},
    ]

    def test_run_keeps_platform_order(self):
        eng = StubEngine({
            "alpha.test": (200, "profile", ""),
            "beta.test": (200, "Not Found", ""),
            "gamma.test": 404,
        }, threads=3)
        results = eng.run("tester", self.platforms)
        self.assertEqual([r.platform for r in results], ["Alpha", "Beta", "Gamma"])
        self.assertEqual([r.status for r in results], [FOUND, NOT_FOUND, NOT_FOUND])

    def test_username_is_url_encoded(self):
        eng = StubEngine({"alpha.test": (200, "", "")})
        eng.run("a b/c", self.platforms[:1])
        self.assertIn("a%20b%2Fc", eng.calls[0])

    def test_http_error_becomes_result_not_exception(self):
        eng = StubEngine({"alpha.test": 500})
        results = eng.run("tester", self.platforms[:1])
        self.assertEqual(results[0].status, UNKNOWN)
        self.assertEqual(results[0].http_code, 500)

    def test_empty_platform_list(self):
        eng = StubEngine({})
        self.assertEqual(eng.run("tester", []), [])

    def test_json_payload_counts(self):
        eng = StubEngine({
            "alpha.test": (200, "", ""),
            "beta.test": (200, "not found", ""),
            "gamma.test": 404,
        })
        results = eng.run("tester", self.platforms)
        payload = json.loads(results_to_json("tester", results, 5))
        self.assertEqual(payload["username"], "tester")
        self.assertEqual(payload["checked"], 3)
        self.assertEqual(payload["found"], 1)
        self.assertEqual(payload["not_found"], 2)
        self.assertEqual(payload["unknown"], 0)


class PlatformDataTests(unittest.TestCase):
    def test_names_unique(self):
        names = [p["name"] for p in PLATFORMS]
        self.assertEqual(len(names), len(set(names)))

    def test_every_entry_is_usable(self):
        for platform in PLATFORMS:
            self.assertIn("{username}", platform["url"], platform["name"])
            self.assertTrue(platform["url"].startswith("https://"), platform["name"])
            # "status" is the default when a platform has no explicit check.
            self.assertIn(platform.get("check", "status"), ("status", "marker"), platform["name"])
            self.assertTrue(platform["category"], platform["name"])

    def test_verification_report_agrees_with_the_shipped_list(self):
        """The report's real numbers must match the bundled data.

        The README's honesty claim ("X of Y candidates passed") is only worth
        something if X is the shipped list and Y is the candidate list, so the
        committed report is checked against both.
        """
        root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        with open(os.path.join(root, "tools", "verification_report.txt"),
                  encoding="utf-8") as handle:
            report = handle.read()
        tested = re.search(r"^Candidates tested\s+: (\d+)$", report, re.M)
        verified = re.search(r"^Verified \(shipped\)\s+: (\d+)$", report, re.M)
        self.assertIsNotNone(tested, "report must state how many candidates were tested")
        self.assertIsNotNone(verified, "report must state how many platforms were verified")
        from ghostrecon.candidates import CANDIDATES
        self.assertEqual(int(tested.group(1)), len(CANDIDATES))
        self.assertEqual(int(verified.group(1)), len(PLATFORMS))
        self.assertIn("%d platforms" % len(PLATFORMS), report)

    def test_plateau_count_is_documented(self):
        # The README states a platform count; it must equal the bundled list.
        root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        with open(os.path.join(root, "README.md"), encoding="utf-8") as handle:
            readme = handle.read()
        self.assertIn("%d platforms" % len(PLATFORMS), readme)


class CliTests(unittest.TestCase):
    def test_only_found_filters(self):
        results = [
            engine.Result("A", "dev", "u", FOUND),
            engine.Result("B", "dev", "u", NOT_FOUND),
            engine.Result("C", "dev", "u", UNKNOWN),
        ]
        self.assertEqual([r.platform for r in cli._visible(results, True)], ["A"])
        self.assertEqual(len(cli._visible(results, False)), 3)

    def test_table_renders_all_rows(self):
        results = [engine.Result("Alpha", "dev", "https://a", FOUND)]
        text = cli.render_table(results)
        self.assertIn("Alpha", text)
        self.assertIn("FOUND", text)

    def test_parser_defaults(self):
        args = cli.build_parser().parse_args(["-u", "alice"])
        self.assertEqual(args.output, "table")
        self.assertEqual(args.threads, 10)
        self.assertFalse(args.only_found)

    def test_usernames_are_deduplicated(self):
        args = cli.build_parser().parse_args(["-u", "alice", "-u", "alice", "-u", "bob"])
        self.assertEqual(cli.read_usernames(args), ["alice", "bob"])

    def test_list_platforms_exits_zero(self):
        buffer = io.StringIO()
        with redirect_stdout(buffer):
            code = cli.main(["--list-platforms"])
        self.assertEqual(code, 0)
        self.assertIn("%d platforms bundled." % len(PLATFORMS), buffer.getvalue())

    def test_missing_username_is_usage_error(self):
        with self.assertRaises(SystemExit) as ctx:
            cli.main([])
        self.assertEqual(ctx.exception.code, 2)


if __name__ == "__main__":
    unittest.main(verbosity=2)
