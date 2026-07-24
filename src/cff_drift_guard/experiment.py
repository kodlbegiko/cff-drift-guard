"""Reproduce the frozen exploratory pilot from machine-readable records."""

from __future__ import annotations

import csv
import hashlib
import json
import os
import resource
import time
import tracemalloc
from pathlib import Path
from typing import Any

from .metrics import classification_metrics, exclusion_counts, wilson_interval
from .versions import core_version, exact_version


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _predict(record: dict[str, Any], mode: str = "exact") -> bool:
    cff = record.get("cff_version")
    manifest = record.get("manifest_version")
    if record.get("manual_label") == "INELIGIBLE" or not cff or not manifest:
        return False
    normalizer = exact_version if mode == "exact" else core_version
    return normalizer(str(cff)) != normalizer(str(manifest))


def run_experiment(source: Path, output_dir: Path) -> dict[str, Any]:
    started = time.perf_counter()
    tracemalloc.start()
    records = json.loads(source.read_text(encoding="utf-8"))
    eligible = [record for record in records if record["manual_label"] in {"DRIFT", "MATCH"}]
    drift = [record for record in eligible if record["manual_label"] == "DRIFT"]
    exact_predictions = [_predict(record, "exact") for record in eligible]
    core_predictions = [_predict(record, "core") for record in eligible]
    truth = [record["manual_label"] == "DRIFT" for record in eligible]
    exact_metrics = classification_metrics(truth, exact_predictions)
    core_metrics = classification_metrics(truth, core_predictions)
    baseline_metrics = classification_metrics(truth, [False] * len(eligible))
    low, high = wilson_interval(len(drift), len(eligible))
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    elapsed = time.perf_counter() - started
    peak_rss_kib = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss

    cff_present = sum(bool(record["cff_present"]) for record in records)
    cff_version_present = sum(
        bool(record.get("cff_version")) for record in records if record["cff_present"]
    )
    result: dict[str, Any] = {
        "study_type": "exploratory pilot benchmark",
        "source_sha256": _sha256(source),
        "sample_n": len(records),
        "github_n": sum(record["host"] == "github" for record in records),
        "cff_present_n": cff_present,
        "cff_version_present_n": cff_version_present,
        "cff_version_completeness": cff_version_present / cff_present if cff_present else 0.0,
        "eligible_n": len(eligible),
        "drift_n": len(drift),
        "drift_prevalence": len(drift) / len(eligible) if eligible else None,
        "drift_wilson_95": [low, high],
        "exclusion_counts": exclusion_counts(records),
        "checker_exact": exact_metrics,
        "checker_core": core_metrics,
        "baseline_presence_only": baseline_metrics,
        "sensitivity": {
            "exact_drift_n": sum(exact_predictions),
            "core_drift_n": sum(core_predictions),
            "include_scope_ambiguous_as_non_drift_n": len(eligible)
            + sum(bool(r.get("scope_ambiguous")) for r in records),
        },
        "runtime_seconds": elapsed,
        "tracemalloc_peak_bytes": peak,
        "tracemalloc_current_bytes": current,
        "peak_rss_kib": peak_rss_kib,
        "stopping_rule_triggered": len(eligible) < 10,
        "primary_verdict": "INCONCLUSIVE"
        if len(eligible) < 10
        else (
            "SUPPORTED"
            if len(drift) / len(eligible) >= 0.2
            and exact_metrics["precision"] >= 0.9
            and exact_metrics["recall"] >= 0.8
            else "NOT SUPPORTED"
        ),
        "environment": {"pythonhashseed": os.environ.get("PYTHONHASHSEED", "unset")},
    }

    output_dir.mkdir(parents=True, exist_ok=True)
    result_json = output_dir / "pilot-results.json"
    result_json.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    with (output_dir / "screening.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(records[0]))
        writer.writeheader()
        writer.writerows(records)
    deterministic = dict(result)
    for key in [
        "runtime_seconds",
        "tracemalloc_peak_bytes",
        "tracemalloc_current_bytes",
        "peak_rss_kib",
        "environment",
    ]:
        deterministic.pop(key, None)
    deterministic_path = output_dir / "pilot-results-deterministic.json"
    deterministic_path.write_text(
        json.dumps(deterministic, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    result["deterministic_output_sha256"] = _sha256(deterministic_path)
    result_json.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return result
