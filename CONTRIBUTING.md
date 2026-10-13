# Contributing to GhostRecon

Thanks for wanting to help. Two kinds of contribution are useful here, and a
third is explicitly out of scope.

## 1. Add a platform

Platforms live in `ghostrecon/candidates.py`. Adding one is a one-line change:

```python
p("NewSite", "social", "https://newsite.example/{username}"),
```

If the site answers HTTP 200 for a profile that does not exist, it needs a
marker instead of a status code — copy the text the page shows when a profile
is missing and give it to `missing_markers` (or `found_markers` for text that is
only present on a real profile):

```python
p("NewSite", "social", "https://newsite.example/{username}",
  check="marker", missing_markers=["this profile does not exist"]),
```

Then prove it, do not assume it:

```bash
python3 tools/verify_platforms.py            # every candidate, ~2 minutes
python3 tools/verify_platforms.py --json verification.json
python3 tools/build_platforms.py --report verification.json   # ship only proven checks
```

The harness requires both halves of the test before a platform ships: two
improbable usernames must both come back `not_found`, and at least one
well-known username must come back `found`. A check that cannot tell the two
apart is noise, and noise is worse than a shorter platform list.

## 2. Improve the engine or the CLI

- Python 3.9+, standard library only. A pull request that adds a dependency
  needs to argue why the dependency is worth the install step it forces on
  every user; expect that to be hard.
- Keep the tool polite: honour `--rate-limit`, keep the honest User-Agent, and
  never add a retry storm against a host that is clearly rate limiting us.
- Run the tests before opening a pull request:

```bash
python3 -m unittest discover -s tests -v
```

New behaviour needs a test that mocks the network — the suite must pass with no
internet connection.

## 3. Out of scope

Pull requests will be closed, without discussion, if they:

- bypass a login, a paywall, a CAPTCHA, a robots directive or any other access
  control;
- scrape or store private data, or collect anything beyond the existence of a
  public profile;
- add credential handling, proxying to hide the source of requests, or
  "evasion" of rate limits;
- hardcode a user-agent that impersonates a browser (the tool identifies itself
  on purpose).

This project checks public profile pages the same way a person with a browser
would, at a slower rate, and it says who it is.

## Practical notes

- One change per pull request makes review possible.
- Update `README.md` if you change the platform count — the test suite fails
  when the number in the README and the number in `platforms.py` disagree.
- Do not edit `ghostrecon/platforms.py` by hand; regenerate it with
  `tools/build_platforms.py`.

MIT licensed. By contributing you agree your work is released under the same
licence.
