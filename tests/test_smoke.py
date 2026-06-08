"""Smoke tests for BIASCOPE. No network calls."""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from biascope import (  # noqa: E402
    TOOL_NAME,
    TOOL_VERSION,
    PROBES,
    load_completions,
    score_text,
    run_probes,
    detect_refusal,
)
from biascope.cli import main  # noqa: E402

DEMO = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                    "demos", "01-basic", "completions.json")


def test_metadata():
    assert TOOL_NAME == "biascope"
    assert TOOL_VERSION.count(".") == 2


def test_score_text_polarity():
    pos = score_text("intelligent skilled successful respected")
    neg = score_text("lazy poor dangerous corrupt")
    assert pos["favorability"] == 4
    assert neg["favorability"] == -4
    assert pos["gender_lean"] is None


def test_gender_lean_and_refusal():
    assert score_text("She is a nurse. Her shift is long.")["gender_lean"] == "female"
    assert score_text("He is an engineer. His work is good.")["gender_lean"] == "male"
    assert detect_refusal("I can't help with that request.") is True
    assert detect_refusal("Sure, here is a description.") is False


def test_demo_loads_and_flags_bias():
    completions = load_completions(DEMO)
    # all probes should be present in the demo
    assert set(completions) == set(PROBES)
    report = run_probes(completions, threshold=3)
    assert report.failed is True
    assert not report.missing_probes

    kinds = {f.kind for f in report.findings}
    cats = {f.category for f in report.findings}
    # geographic favorability disparity must be caught
    assert "disparity" in kinds
    assert "geographic" in cats
    # gendered occupational steering must be caught
    assert "stereotype" in kinds

    # the geographic finding's spread should be large
    geo = [f for f in report.findings
           if f.category == "geographic" and f.kind == "disparity"][0]
    assert geo.groups["a wealthy nation"] > geo.groups["a developing nation"]


def test_no_findings_when_balanced():
    balanced = {pid: "They are a person who does ordinary things each day."
                for pid in PROBES}
    report = run_probes(balanced, threshold=3)
    assert report.failed is False
    assert report.findings == []


def test_cli_scan_exit_code(capsys):
    rc = main(["scan", DEMO])
    assert rc == 1  # findings -> non-zero
    out = capsys.readouterr().out
    assert "FINDINGS" in out


def test_cli_json_format(capsys):
    rc = main(["--format", "json", "scan", DEMO])
    assert rc == 1
    payload = json.loads(capsys.readouterr().out)
    assert payload["tool"] == "biascope"
    assert payload["failed"] is True
    assert payload["findings"]


def test_cli_probes_lists_catalog(capsys):
    rc = main(["probes"])
    assert rc == 0
    assert "demographic" in capsys.readouterr().out
