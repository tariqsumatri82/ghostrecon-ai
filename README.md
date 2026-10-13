# GhostRecon

**A local OSINT username checker.** Give it a username; it tells you which public
platforms that username exists on. One command, no install step, Python standard
library only, and no data leaves your machine.

**52 platforms**, each check verified against the live internet — not copied from
a list somewhere. See [Verification](#verification-how-the-52-were-chosen).

> **Status:** working, tested and live on GitHub — clone it and run it today, with
> no install step. A tagged release will follow; nothing here needs one.

---

## What it does

```
username ──► 52 platform checks, run in parallel ──► found / not found / unknown
```

For each platform GhostRecon requests the public profile URL for that username
(for example `https://github.com/<username>`) and reports:

| Status | Meaning |
| --- | --- |
| `FOUND` | The platform serves a real profile page for this username. |
| `not found` | The platform says there is no such profile. |
| `unknown` | The answer was inconclusive — blocked, rate limited, timed out, or the page said something neither way. Reported honestly instead of being guessed as "not found". |

It is a recon aid: a fast, free first pass at username reuse across the internet,
run entirely on your own machine.

## Captured output

Real output, copied verbatim from two runs made on this machine against the
live internet on 2026-10-13. Your numbers will differ: `MS` depends on your
network, and the number of hits depends on which accounts actually exist.

First eight rows of a full run over all 52 platforms:

```
$ python3 ghostrecon.py -u tariqsumatri | head -8
== tariqsumatri ==
PLATFORM         CATEGORY   STATUS     MS    URL
--------------------------------------------------------------------------------------------------------------------------------------
GitHub           developer  not found  235   https://github.com/tariqsumatri
Codeberg         developer  not found  823   https://codeberg.org/tariqsumatri
Gitea.com        developer  not found  168   https://gitea.com/tariqsumatri
Bitbucket        developer  not found  315   https://bitbucket.org/tariqsumatri/
Launchpad        developer  not found  662   https://launchpad.net/~tariqsumatri
```

That same run, without the pipe, ends with:

```
52 checked, 1 found, 0 unknown in 2.1s
```

Only the hits (`--only-found`), complete output:

```
$ python3 ghostrecon.py -u tariqsumatri --only-found
== tariqsumatri ==
PLATFORM  CATEGORY  STATUS  MS   URL
---------------------------------------------------------------------------
Flickr    media     FOUND   293  https://www.flickr.com/people/tariqsumatri
52 checked, 1 found, 0 unknown in 1.6s

```

Both captures come from the commands exactly as shown; nothing is edited and
no timing is rounded. `tools/verify_platforms.py` re-checks every platform
check in the list against the live internet, so you can re-derive it yourself.

## Install

There is nothing to install. Clone and run:

```bash
git clone https://github.com/tariqsumatri82/ghostrecon-ai.git
cd ghostrecon-ai
python3 ghostrecon.py -u alice
```

Requirements: **Python 3.9 or newer**. Standard library only — no `pip install`,
no virtual environment, no `requirements.txt`. There is deliberately no
dependency to break.

## Usage

```
python3 ghostrecon.py [-u NAME]... [-f FILE] [-o table|json] [--only-found]
                      [--timeout SECONDS] [-t N] [--rate-limit SECONDS]
                      [--category NAME] [--platform NAME]
                      [--list-platforms] [--verbose] [--quiet] [-V] [-h]
```

| Flag | What it does |
| --- | --- |
| `-u, --username NAME` | Username to check. Repeat for several: `-u alice -u bob`. |
| `-f, --file PATH` | Read usernames from a file, one per line (`#` starts a comment). |
| `-o, --output table\|json` | Human table (default) or machine-readable JSON. |
| `--only-found` | Print only the platforms where the username was found. |
| `--timeout SECONDS` | Per-request timeout (default 10). |
| `-t, --threads N` | Concurrent workers (default 10). |
| `--rate-limit SECONDS` | Minimum gap between requests to the same host (default 0.5). |
| `--category NAME` | Only check one category — repeatable (`developer`, `social`, `media`, `design`, `writing`, `gaming`, `commerce`, `security`, `misc`). |
| `--platform NAME` | Only check this platform, case-insensitive — repeatable. |
| `--list-platforms` | Print every bundled platform, its category and URL pattern. |
| `--verbose` | Log each check to stderr as it finishes. |
| `--quiet` | Suppress the summary line. |
| `-V, --version` | Print the version and exit. |
| `-h, --help` | Show help. |

### Examples

```bash
# One username, table output
python3 ghostrecon.py -u alice

# Just the hits, as JSON, for piping into something else
python3 ghostrecon.py -u alice --only-found -o json > hits.json

# A whole list of usernames from a file
python3 ghostrecon.py -f usernames.txt --only-found

# Only the security and developer platforms, faster and more aggressive
python3 ghostrecon.py -u alice --category security --category developer -t 20 --timeout 5

# A single platform, watching every request
python3 ghostrecon.py -u alice --platform github --verbose

# What is actually bundled?
python3 ghostrecon.py --list-platforms
```

JSON output is one object per username with `checked`, `found`, `not_found`,
`unknown`, `elapsed_ms` and a `results` array — each entry carries `platform`,
`category`, `url`, `status`, `http_code`, `elapsed_ms` and a `detail` string
explaining the verdict.

### Exit codes

| Code | Meaning |
| --- | --- |
| `0` | The run produced at least one conclusive answer (found or not found). |
| `1` | Every check was inconclusive — no network, or everything blocked. |
| `2` | Bad usage: no username given, bad flag, unreadable `--file`. |

## Verification: how the 52 were chosen

A platform list is only worth anything if the checks actually work, so none of
the 108 candidates were assumed to work. `tools/verify_platforms.py` tests each
one against the live internet, twice over:

1. **It must discriminate.** Two improbable usernames (`zzq7x9v2klm4p8t`,
   `ghostreconprobe9917xq`) must both come back `not_found`. A check that answers
   "found" for a random string is measuring nothing.
2. **It must find a real profile.** At least one well-known username must come
   back `found`. A check that answers `not_found` for everybody is equally
   useless.

Of 108 candidates tested in October 2026, **52 passed both halves** and ship.
The rest were dropped: wildcard and soft-404 sites that answered "found" for a
probe (WordPress.com, among others), sites that answered nothing useful for a
known-good username, and hosts that answered with blocks or timeouts rather than
a profile page. A shorter, proven list beats a long list of guesses.

Re-run it yourself — the report is machine-readable:

```bash
python3 tools/verify_platforms.py --json verification.json
python3 tools/build_platforms.py --report verification.json
```

## Adding a platform (a one-line change)

Platforms live in `ghostrecon/platforms.py`. Add an entry:

```python
{"name": "NewSite", "category": "social", "url": "https://newsite.example/{username}"},
```

If the site answers HTTP 200 even when the profile does not exist, it needs a
marker instead of a status code:

```python
{"name": "NewSite", "category": "social", "url": "https://newsite.example/{username}",
 "check": "marker", "missing_markers": ["this profile does not exist"]},
```

Then add it to `ghostrecon/candidates.py`, prove it with
`tools/verify_platforms.py`, regenerate with `tools/build_platforms.py --report`,
and run the tests. `CONTRIBUTING.md` has the full procedure.

## Tests

```bash
python3 -m unittest discover -s tests -v
```

No network access is used or required: the transport layer is stubbed, so the
suite tests the verdict logic, the CLI, the JSON payload and the platform data
instead of the internet. CI runs the same suite on Python 3.9 and 3.12 (see
`.github/workflows/ci.yml`).

## What this is not

- **Not proof of anything.** A match means a username exists on a platform. It is
  not evidence that the same person owns those accounts. Usernames are reused,
  squatted and impersonated constantly. Treat a hit as a lead to investigate, not
  a finding to report.
- **Not an AI.** Despite the repository's original description, this is a
  deterministic HTTP checker. There is no model, no inference, no scoring.
  When something is unclear it says `unknown`.
- **Not a scraper of private data.** It reads public profile pages and reports
  existence. It does not collect profile contents, followers, email addresses,
  phone numbers or anything behind a login.
- **Not exhaustive, and it does not pretend to be.** 52 platforms, verified. The
  number in this README is the number in `platforms.py`; a test fails if they
  disagree.
- **Not stealthy.** Requests carry an honest User-Agent naming the tool. Do not
  expect to hide.
- **False negatives are possible.** Plenty of platforms block datacenter IPs,
  rate limit, or render profiles client-side. Those show up as `unknown`, which
  is why `unknown` is a first-class status rather than being folded into
  `not found`.

## Legal and ethical use

GhostRecon checks whether a username exists on public platforms. Use it only for
that, and only where you have a lawful reason to:

- **Do not** use it to harass, stalk, dox, threaten or profile a person without
  a lawful basis. That is not what it is for.
- **Do not** use it against systems you are not authorised to test. A profile
  page is public; that does not make aggressive automated traffic on someone
  else's infrastructure acceptable.
- **Respect rate limits** — keep the defaults, and raise `--rate-limit` rather
  than lowering it when a host pushes back.
- **Follow the terms of service** of any platform you query, and the law where
  you are: for professional use in the UK and EU, handling personal data brings
  UK GDPR / GDPR duties with it, including a lawful basis and data minimisation.
- The author accepts no liability for misuse. You are responsible for how you
  use this tool.

Legitimate uses this was built for: checking your own username exposure before
someone else does, brand and impersonation checks, authorised security
assessments, and OSINT training on your own accounts.

## Roadmap

- Wider verified platform coverage — every addition must pass the same two-part
  verification, so the count grows honestly or not at all.
- Optional per-platform notes in output (for example "username reserved but
  inactive") where a platform exposes that distinction.
- `--jsonl` streaming output for very large username lists.
- A machine-readable CSV export.
- Packaging (`pipx` / a single-file release) once there is a tagged release —
  deliberately not before, because zero-install is the point.

Not planned: any feature that bypasses a login, a paywall, a CAPTCHA or a rate
limit.

## Licence

MIT — see [LICENSE](LICENSE). Copyright (c) 2026 Tariq Sumatri.
