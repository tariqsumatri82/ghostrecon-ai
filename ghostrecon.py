#!/usr/bin/env python3
"""GhostRecon entry point.

Usage:
    python3 ghostrecon.py -u <username>

Runs on the Python standard library alone (Python 3.9+): no pip install step.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ghostrecon.cli import main  # noqa: E402

if __name__ == "__main__":
    sys.exit(main())
