"""BIASCOPE - Embedded bias probe suite for AI security.

BIASCOPE runs a battery of templated probes against a model's text
completions to surface demographic, occupational, and geographic bias.
It does not call any model itself; instead it consumes a *completions*
file (a record of probe_id -> model output) so it can run fully offline
and deterministically in CI.

The engine computes:
  * sentiment / favorability per group using a built-in lexicon,
  * disparity across the groups within each probe category,
  * stereotype-association hits (e.g. an occupation steered toward one
    gender or region),
  * refusal / evasion detection,

and flags any category whose group disparity exceeds a configurable
threshold as a FINDING.

Standard library only. Zero install.
"""
from .core import (
    PROBES,
    LEXICON,
    Finding,
    Report,
    load_completions,
    score_text,
    run_probes,
    detect_refusal,
)

TOOL_NAME = "biascope"
TOOL_VERSION = "1.0.0"

__all__ = [
    "TOOL_NAME",
    "TOOL_VERSION",
    "PROBES",
    "LEXICON",
    "Finding",
    "Report",
    "load_completions",
    "score_text",
    "run_probes",
    "detect_refusal",
]
