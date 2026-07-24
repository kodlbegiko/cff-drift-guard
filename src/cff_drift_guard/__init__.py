"""Cross-file software citation version consistency checks."""

from .analyzer import Analysis, analyze_repository
from .versions import core_version, exact_version

__all__ = ["Analysis", "analyze_repository", "core_version", "exact_version"]
__version__ = "0.1.0"
