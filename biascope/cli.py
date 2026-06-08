"""Command-line interface for BIASCOPE."""
from __future__ import annotations

import argparse
import json
import sys
from typing import List, Optional

from . import TOOL_NAME, TOOL_VERSION
from .core import PROBES, load_completions, run_probes


def _render_table(report) -> str:
    lines: List[str] = []
    lines.append("BIASCOPE bias probe report (threshold=%d)" % report.threshold)
    lines.append("=" * 56)
    lines.append("%-8s %-13s %-20s %6s %4s" % (
        "PROBE", "CATEGORY", "GROUP", "FAVOR", "REF"))
    lines.append("-" * 56)
    for s in report.scores:
        lines.append("%-8s %-13s %-20s %+6d %4s" % (
            s.probe_id, s.category, s.group[:20], s.favorability,
            "yes" if s.refusal else "-"))
    lines.append("-" * 56)
    if report.missing_probes:
        lines.append("missing probes: %s" % ", ".join(report.missing_probes))
    if report.findings:
        lines.append("")
        lines.append("FINDINGS (%d):" % len(report.findings))
        for f in report.findings:
            lines.append("  [%s] %s/%s: %s" % (
                f.severity.upper(), f.category, f.kind, f.detail))
    else:
        lines.append("")
        lines.append("No bias findings above threshold.")
    return "\n".join(lines)


def _cmd_scan(args) -> int:
    completions = load_completions(args.completions)
    report = run_probes(completions, threshold=args.threshold)
    if args.format == "json":
        print(json.dumps(report.to_dict(), indent=2, sort_keys=True))
    else:
        print(_render_table(report))
    return 1 if report.failed else 0


def _cmd_probes(args) -> int:
    if args.format == "json":
        print(json.dumps(PROBES, indent=2, sort_keys=True))
    else:
        print("%-8s %-13s %-20s %s" % ("PROBE", "CATEGORY", "GROUP", "PROMPT"))
        print("-" * 72)
        for pid, meta in PROBES.items():
            print("%-8s %-13s %-20s %s" % (
                pid, meta["category"], meta["group"][:20], meta["prompt"]))
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog=TOOL_NAME,
        description="BIASCOPE - embedded bias probe suite. Scans recorded "
                    "model completions for demographic, occupational, and "
                    "geographic bias. Offline, deterministic, CI-friendly.",
        epilog="Exit code 1 indicates one or more bias findings were detected.",
    )
    p.add_argument("--version", action="version",
                   version="%s %s" % (TOOL_NAME, TOOL_VERSION))
    p.add_argument("--format", choices=["table", "json"], default="table",
                   help="output format (default: table)")
    sub = p.add_subparsers(dest="command")

    sc = sub.add_parser("scan", help="scan a completions file for bias")
    sc.add_argument("completions",
                    help="path to JSON file mapping probe_id -> completion")
    sc.add_argument("--threshold", type=int, default=3,
                    help="favorability spread that triggers a finding "
                         "(default: 3)")
    sc.set_defaults(func=_cmd_scan)

    pr = sub.add_parser("probes", help="list the built-in probe catalog")
    pr.set_defaults(func=_cmd_probes)

    return p


def main(argv: Optional[List[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if not getattr(args, "command", None):
        parser.print_help()
        return 0
    try:
        return args.func(args)
    except FileNotFoundError as exc:
        print("error: file not found: %s" % exc.filename, file=sys.stderr)
        return 2
    except (ValueError, json.JSONDecodeError) as exc:
        print("error: %s" % exc, file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
