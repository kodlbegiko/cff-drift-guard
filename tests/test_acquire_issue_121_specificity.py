from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

SCRIPT = Path(__file__).parents[1] / "scripts" / "acquire_issue_121_specificity.py"
spec = importlib.util.spec_from_file_location("acquire", SCRIPT)
assert spec and spec.loader
acquire = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = acquire
spec.loader.exec_module(acquire)


def payload(text: str, sha: str = "a" * 40):
    return acquire.FilePayload(text, sha)


def test_top_level_cff_version_ignores_preferred_citation() -> None:
    text = "cff-version: 1.2.0\npreferred-citation:\n  version: 9.9\n"
    assert acquire.parse_cff_version(text) is None


def test_classify_missing_cff() -> None:
    result = acquire.classify(None, [])
    assert result["status"] == "CFF_MISSING"
    assert result["specificity_gap"] is None


def test_classify_missing_version_is_gap() -> None:
    cff = payload("cff-version: 1.2.0\ntitle: X\n")
    result = acquire.classify(cff, [])
    assert result["status"] == "VERSION_MISSING"
    assert result["specificity_gap"] is True


def test_classify_exact_match() -> None:
    cff = payload("cff-version: 1.2.0\nversion: 1.2.3\n")
    manifest = acquire.Manifest("pyproject.toml", "1.2.3")
    result = acquire.classify(cff, [manifest])
    assert result["status"] == "MATCH"
    assert result["specificity_gap"] is False


def test_classify_normalized_v_prefix_match() -> None:
    cff = payload("cff-version: 1.2.0\nversion: v1.2.3\n")
    manifest = acquire.Manifest("pyproject.toml", "1.2.3")
    assert acquire.classify(cff, [manifest])["status"] == "NORMALIZED_MATCH"


def test_classify_drift() -> None:
    cff = payload("cff-version: 1.2.0\nversion: 1.2.3\n")
    manifest = acquire.Manifest("pyproject.toml", "1.3.0")
    result = acquire.classify(cff, [manifest])
    assert result["status"] == "DRIFT"
    assert result["specificity_gap"] is True


def test_dynamic_manifest_not_called_drift() -> None:
    cff = payload("cff-version: 1.2.0\nversion: 1.2.3\n")
    manifest = acquire.Manifest("pyproject.toml", None, dynamic=True)
    result = acquire.classify(cff, [manifest])
    assert result["status"] == "MANIFEST_DYNAMIC"
    assert result["specificity_gap"] is False


def test_multiple_manifests_are_ambiguous() -> None:
    cff = payload("cff-version: 1.2.0\nversion: 1.2.3\n")
    result = acquire.classify(
        cff,
        [acquire.Manifest("pyproject.toml", "1.2.3"), acquire.Manifest("package.json", "1.2.3")],
    )
    assert result["status"] == "MANIFEST_AMBIGUOUS"


def test_parse_pyproject_static() -> None:
    result = acquire.parse_pyproject('[project]\nname="x"\nversion="2.0"\n', "b" * 40)
    assert result.version == "2.0"
    assert not result.dynamic


def test_parse_pyproject_dynamic() -> None:
    result = acquire.parse_pyproject('[project]\nname="x"\ndynamic=["version"]\n', "b" * 40)
    assert result.version is None
    assert result.dynamic


def test_parse_description() -> None:
    text = 'Package: demo\nVersion: 0.4.1\nAuthors@R: c(\n    person("Ada", "Lovelace")\n)\n'
    result = acquire.parse_description(text, "c" * 40)
    assert result.package_name == "demo"
    assert result.version == "0.4.1"


def test_parse_cargo_workspace_ambiguous() -> None:
    result = acquire.parse_cargo('[workspace]\nmembers=["a"]\n', "d" * 40)
    assert result.ambiguous


def test_summary_threshold_and_counts() -> None:
    records = [
        {"host": "github", "status": "VERSION_MISSING", "specificity_gap": True},
        {"host": "github", "status": "DRIFT", "specificity_gap": True},
        {"host": "github", "status": "MATCH", "specificity_gap": False},
    ] + [
        {"host": "github", "status": "MANIFEST_DYNAMIC", "specificity_gap": False} for _ in range(7)
    ]
    summary = acquire.summarize(records, {"source_sha256": "x"})
    assert summary["cff_present_n"] == 10
    assert summary["specificity_gap_n"] == 2
    assert summary["stopping_rule"]["met"] is True


def test_write_outputs_is_machine_readable(tmp_path: Path) -> None:
    records = [{"host": "github", "status": "MATCH", "specificity_gap": False}]
    summary = acquire.summarize(records, {"source_sha256": "x"})
    acquire.write_outputs(tmp_path, records, summary)
    assert json.loads((tmp_path / "preliminary-summary.json").read_text())["sample_n"] == 1
    assert json.loads((tmp_path / "SHA256SUMS.json").read_text())["files"]
