import hashlib
import json
from pathlib import Path

from cff_drift_guard.experiment import run_experiment

ROOT = Path(__file__).parents[1]
SOURCE = ROOT / "data" / "raw" / "source-records.json"


def test_source_has_20_records():
    assert len(json.loads(SOURCE.read_text())) == 20


def test_prespecified_order_unique():
    records = json.loads(SOURCE.read_text())
    assert [r["order"] for r in records] == list(range(1, 21))


def test_run_primary_counts(tmp_path):
    result = run_experiment(SOURCE, tmp_path)
    assert result["sample_n"] == 20
    assert result["github_n"] == 19
    assert result["cff_present_n"] == 14
    assert result["cff_version_present_n"] == 5
    assert result["eligible_n"] == 2
    assert result["drift_n"] == 2


def test_run_verdict_inconclusive(tmp_path):
    result = run_experiment(SOURCE, tmp_path)
    assert result["stopping_rule_triggered"] is True
    assert result["primary_verdict"] == "INCONCLUSIVE"


def test_checker_perfect_on_tiny_eligible_set(tmp_path):
    result = run_experiment(SOURCE, tmp_path)
    assert result["checker_exact"]["precision"] == 1.0
    assert result["checker_exact"]["recall"] == 1.0


def test_baseline_zero_recall(tmp_path):
    result = run_experiment(SOURCE, tmp_path)
    assert result["baseline_presence_only"]["recall"] == 0.0


def test_sensitivity_stable(tmp_path):
    result = run_experiment(SOURCE, tmp_path)
    assert result["sensitivity"]["exact_drift_n"] == result["sensitivity"]["core_drift_n"] == 2


def test_outputs_machine_readable(tmp_path):
    run_experiment(SOURCE, tmp_path)
    assert json.loads((tmp_path / "pilot-results.json").read_text())["sample_n"] == 20
    assert (tmp_path / "screening.csv").read_text().startswith("order,doi,title")


def test_deterministic_output_repeat(tmp_path):
    first = tmp_path / "first"
    second = tmp_path / "second"
    run_experiment(SOURCE, first)
    run_experiment(SOURCE, second)
    a = hashlib.sha256((first / "pilot-results-deterministic.json").read_bytes()).hexdigest()
    b = hashlib.sha256((second / "pilot-results-deterministic.json").read_bytes()).hexdigest()
    assert a == b
