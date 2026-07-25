from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

SCRIPT = Path(__file__).parents[1] / "scripts" / "evaluate_issue_121_specificity.py"
spec = importlib.util.spec_from_file_location("evaluate_issue121", SCRIPT)
assert spec and spec.loader
module = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = module
spec.loader.exec_module(module)


def write_fixture(tmp_path: Path, statuses: list[tuple[str, bool | None, bool]]) -> tuple[Path, Path]:
    source_records = []
    labels = []
    for order, (status, prediction, truth) in enumerate(statuses, 1):
        repository = f"owner/repo-{order}"
        source_records.append(
            {
                "order": order,
                "repository": repository,
                "host": "github",
                "status": status,
                "specificity_gap": prediction,
                "cff_version": None,
                "manifest": None,
            }
        )
        labels.append(
            {
                "order": order,
                "repository": repository,
                "primary_denominator": status != "CFF_MISSING",
                "manual_gap": truth if status != "CFF_MISSING" else None,
                "adjudication": "fixture",
                "notes": "fixture",
            }
        )
    source = tmp_path / "source.json"
    adjudications = tmp_path / "adjudications.json"
    source.write_text(json.dumps({"records": source_records}))
    adjudications.write_text(json.dumps({"records": labels}))
    return source, adjudications


def test_wilson_empty() -> None:
    assert module.wilson_interval(0, 0) == [None, None]


def test_metrics_perfect() -> None:
    metrics = module.classification_metrics([True, False], [True, False])
    assert metrics["precision"] == 1.0
    assert metrics["recall"] == 1.0
    assert metrics["accuracy"] == 1.0


def test_metrics_false_positive_and_negative() -> None:
    metrics = module.classification_metrics([True, False], [False, True])
    assert metrics["fp"] == 1
    assert metrics["fn"] == 1
    assert metrics["f1"] == 0.0


def test_metrics_reject_length_mismatch() -> None:
    try:
        module.classification_metrics([True], [])
    except ValueError as exc:
        assert "equal length" in str(exc)
    else:
        raise AssertionError("expected ValueError")


def test_load_rejects_repository_mismatch(tmp_path: Path) -> None:
    source, adjudications = write_fixture(tmp_path, [("MATCH", False, False)])
    payload = json.loads(adjudications.read_text())
    payload["records"][0]["repository"] = "other/repo"
    adjudications.write_text(json.dumps(payload))
    try:
        module.load_records(source, adjudications)
    except ValueError as exc:
        assert "mismatch" in str(exc)
    else:
        raise AssertionError("expected ValueError")


def test_supported_when_all_gates_pass(tmp_path: Path) -> None:
    statuses = [("VERSION_MISSING", True, True)] * 4 + [("MATCH", False, False)] * 6
    source, adjudications = write_fixture(tmp_path, statuses)
    result, _ = module.evaluate(source, adjudications)
    assert result["primary_verdict"] == "SUPPORTED"


def test_not_supported_below_rate_threshold(tmp_path: Path) -> None:
    statuses = [("VERSION_MISSING", True, True)] * 2 + [("MATCH", False, False)] * 8
    source, adjudications = write_fixture(tmp_path, statuses)
    result, _ = module.evaluate(source, adjudications)
    assert result["primary_verdict"] == "NOT SUPPORTED"


def test_inconclusive_below_minimum_sample(tmp_path: Path) -> None:
    statuses = [("VERSION_MISSING", True, True)] * 3 + [("MATCH", False, False)] * 6
    source, adjudications = write_fixture(tmp_path, statuses)
    result, _ = module.evaluate(source, adjudications)
    assert result["primary_verdict"] == "INCONCLUSIVE"


def test_false_positive_fails_precision_gate(tmp_path: Path) -> None:
    statuses = [("VERSION_MISSING", True, True)] * 4 + [("MATCH", True, False)] * 6
    source, adjudications = write_fixture(tmp_path, statuses)
    result, _ = module.evaluate(source, adjudications)
    assert result["gates"]["precision_at_least_0_80"] is False
    assert result["primary_verdict"] == "NOT SUPPORTED"


def test_false_negative_fails_recall_gate(tmp_path: Path) -> None:
    statuses = [("VERSION_MISSING", False, True)] * 4 + [("MATCH", False, False)] * 6
    source, adjudications = write_fixture(tmp_path, statuses)
    result, _ = module.evaluate(source, adjudications)
    assert result["gates"]["recall_at_least_0_80"] is False


def test_write_outputs_and_hashes(tmp_path: Path) -> None:
    result = {"primary_verdict": "SUPPORTED"}
    rows = [{"repository": "owner/repo", "manual_gap": True}]
    hashes = module.write_outputs(tmp_path, result, rows)
    assert set(hashes) == {"external-validation-results.json", "screening.csv"}
    assert json.loads((tmp_path / "SHA256SUMS.json").read_text())["files"] == hashes


def test_real_frozen_study_reproduces_supported(tmp_path: Path) -> None:
    root = Path(__file__).parents[1]
    result, joined = module.evaluate(
        root / "data/issue-121/acquisition-deterministic.json",
        root / "data/issue-121/adjudications.json",
    )
    assert result["sample_n"] == 39
    assert result["cff_present_n"] == 22
    assert result["confirmed_specificity_gap_n"] == 14
    assert result["primary_verdict"] == "SUPPORTED"
    assert len(joined) == 39
