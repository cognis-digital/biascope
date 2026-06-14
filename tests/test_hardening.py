"""Hardening tests — error paths, edge cases, and input validation."""
from __future__ import annotations

import json
import os
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest

from biascope.cli import main
from biascope.core import (
    PROBES,
    load_completions,
    run_probes,
    score_text,
)


# ---------------------------------------------------------------------------
# load_completions — file I/O and parse validation
# ---------------------------------------------------------------------------

def test_load_missing_file_raises():
    """Non-existent path raises FileNotFoundError."""
    with pytest.raises(FileNotFoundError):
        load_completions("/tmp/does_not_exist_biascope_xyz.json")


def test_load_not_a_dict_raises():
    """JSON array at top-level raises ValueError."""
    with tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False) as fh:
        json.dump(["demo_a", "demo_b"], fh)
        path = fh.name
    try:
        with pytest.raises(ValueError, match="JSON object"):
            load_completions(path)
    finally:
        os.unlink(path)


def test_load_non_string_value_raises():
    """Numeric completion value raises ValueError."""
    with tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False) as fh:
        json.dump({"demo_a": 42}, fh)
        path = fh.name
    try:
        with pytest.raises(ValueError, match="must be a string"):
            load_completions(path)
    finally:
        os.unlink(path)


def test_load_malformed_json_raises():
    """Truncated / invalid JSON raises json.JSONDecodeError."""
    with tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False) as fh:
        fh.write("{bad json{{")
        path = fh.name
    try:
        with pytest.raises(json.JSONDecodeError):
            load_completions(path)
    finally:
        os.unlink(path)


def test_load_empty_object_raises():
    """Empty JSON object raises ValueError."""
    with tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False) as fh:
        json.dump({}, fh)
        path = fh.name
    try:
        with pytest.raises(ValueError, match="empty"):
            load_completions(path)
    finally:
        os.unlink(path)


def test_load_directory_raises():
    """Passing a directory path raises IsADirectoryError."""
    with tempfile.TemporaryDirectory() as d:
        with pytest.raises((IsADirectoryError, OSError)):
            load_completions(d)


# ---------------------------------------------------------------------------
# run_probes — threshold and input guards
# ---------------------------------------------------------------------------

def test_run_probes_bad_threshold_raises():
    """threshold=0 or negative raises ValueError."""
    completions = {pid: "text" for pid in PROBES}
    with pytest.raises(ValueError, match="threshold"):
        run_probes(completions, threshold=0)
    with pytest.raises(ValueError, match="threshold"):
        run_probes(completions, threshold=-5)


def test_run_probes_non_dict_raises():
    """Passing a list instead of dict raises TypeError."""
    with pytest.raises(TypeError):
        run_probes(["demo_a"], threshold=3)  # type: ignore[arg-type]


def test_run_probes_all_missing_gives_no_scores():
    """When none of the probe IDs appear, report has no scores and all missing."""
    report = run_probes({"unknown_probe": "some text"}, threshold=3)
    assert report.scores == []
    assert set(PROBES.keys()).issubset(set(report.missing_probes))


# ---------------------------------------------------------------------------
# score_text — edge cases
# ---------------------------------------------------------------------------

def test_score_empty_string():
    """Empty string produces zero score and no hits."""
    result = score_text("")
    assert result["favorability"] == 0
    assert result["pos_hits"] == []
    assert result["neg_hits"] == []
    assert result["gender_lean"] is None
    assert result["refusal"] is False


def test_score_whitespace_only():
    """Whitespace-only string is treated as empty."""
    result = score_text("   \t\n  ")
    assert result["favorability"] == 0


# ---------------------------------------------------------------------------
# CLI — exit codes for bad inputs
# ---------------------------------------------------------------------------

def _write_tmp_json(data) -> str:
    fh = tempfile.NamedTemporaryFile(
        mode="w", suffix=".json", delete=False)
    json.dump(data, fh)
    fh.close()
    return fh.name


def test_cli_missing_file_exits_2(capsys):
    """scan with a non-existent file → exit code 2, error on stderr."""
    rc = main(["scan", "/tmp/no_such_file_biascope_xyz.json"])
    assert rc == 2
    err = capsys.readouterr().err
    assert "error" in err.lower()


def test_cli_malformed_json_exits_2(capsys):
    """scan with a malformed JSON file → exit code 2, error on stderr."""
    with tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False) as fh:
        fh.write("{not valid json")
        path = fh.name
    try:
        rc = main(["scan", path])
        assert rc == 2
        err = capsys.readouterr().err
        assert "error" in err.lower()
    finally:
        os.unlink(path)


def test_cli_non_dict_json_exits_2(capsys):
    """scan with a JSON array instead of object → exit code 2."""
    path = _write_tmp_json(["a", "b"])
    try:
        rc = main(["scan", path])
        assert rc == 2
        err = capsys.readouterr().err
        assert "error" in err.lower()
    finally:
        os.unlink(path)


def test_cli_bad_threshold_exits_nonzero(capsys):
    """--threshold 0 should be rejected by argparse (non-zero exit)."""
    # argparse calls sys.exit(2) on bad argument type/value; main() converts
    # that to a return code via SystemExit; here we just check it doesn't
    # succeed with rc=0.
    with pytest.raises(SystemExit) as exc_info:
        main(["scan", "irrelevant.json", "--threshold", "0"])
    assert exc_info.value.code != 0


def test_cli_no_command_exits_zero(capsys):
    """Calling biascope with no subcommand prints help and returns 0."""
    rc = main([])
    assert rc == 0
    out = capsys.readouterr().out
    assert "scan" in out or "probes" in out or "BIASCOPE" in out.upper()
