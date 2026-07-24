import json
from pathlib import Path

from cff_drift_guard.cli import main

FIX = Path(__file__).parent / "fixtures"


def test_cli_match_exit_zero(capsys):
    assert main(["check", str(FIX / "match")]) == 0
    assert json.loads(capsys.readouterr().out)["status"] == "MATCH"


def test_cli_drift_exit_one(capsys):
    assert main(["check", str(FIX / "mismatch")]) == 1
    assert json.loads(capsys.readouterr().out)["status"] == "DRIFT"


def test_cli_insufficient_exit_two(capsys):
    assert main(["check", str(FIX / "cff_missing")]) == 2
    assert json.loads(capsys.readouterr().out)["status"] == "CFF_MISSING"


def test_cli_json_out(tmp_path, capsys):
    target = tmp_path / "result.json"
    assert main(["check", str(FIX / "match"), "--json-out", str(target)]) == 0
    assert json.loads(target.read_text())["status"] == "MATCH"
    capsys.readouterr()


def test_cli_benchmark(tmp_path, capsys):
    source = Path(__file__).parents[1] / "data" / "raw" / "source-records.json"
    assert main(["benchmark", "--source", str(source), "--output-dir", str(tmp_path)]) == 0
    assert json.loads(capsys.readouterr().out)["primary_verdict"] == "INCONCLUSIVE"
