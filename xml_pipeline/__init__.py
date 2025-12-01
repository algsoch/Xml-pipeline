"""
xml_pipeline - Tamper-proof XML nervous system for AI agent swarms
"""

from .pipeline import Pipeline
from .bus import MessageBus, Response

__all__ = [
    "Pipeline",
    "MessageBus",
    "Response",
]

# Version is managed by setuptools_scm
try:
    from ._version import version as __version__
except ImportError:
    __version__ = "unknown"
