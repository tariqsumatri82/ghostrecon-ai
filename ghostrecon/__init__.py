"""GhostRecon — a local, dependency-free username OSINT checker."""

__version__ = "1.0.0"

from .engine import Result, Engine  # noqa: F401
from .platforms import PLATFORMS  # noqa: F401

__all__ = ["Result", "Engine", "PLATFORMS", "__version__"]
