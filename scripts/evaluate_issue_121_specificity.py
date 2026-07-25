#!/usr/bin/env python3
"""Evaluate the frozen JOSS issue-121 CFF version-specificity study."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import resource
import time
import tracemalloc
from pathlib import Path
from typing import Any


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def wilson_interval(successes: int, total: int, z: float = 1.959963984540054) -> list[float | None]:
    if total == 0:
        return [None, None]
    p = successes / total
    denominator = 1 + z * z / total
    center = (p + z * z / (2 * total)) / denominator
    margin = z * ((p * (1 - p) / total + z * z / (4 * total * total)) ** 0.5) / denominator
    return [max(0.0, center - margin), min(1.0, center + margin)]


def classification_metrics(truth: list[bool], predictions: list[bool]) -> dict[str, float | int]:
    if len(truth) != len(predictions):
        raise ValueError("truth and predictions must have equal length")
    tp = sum(t and p for t, p in zip(truth, predictions, strict=True))
    fp = sum((not t) and p for t, p in zip(truth, predictions, strict=True))
    tn = sum((not t) and (not p) for t, p in zip(truth, predictions, strict=True))
    fn = sum(t and (not p) for t, p in zip(truth, predictions, strict=True))

    def ratio(numerator: int, denominator: int) -> float:
        return numerator / denominator if denominator else 0.0

    return {
        "tp": tp,
        "fp": fp,
        "tn": tn,
        "fn": fn,
        "precision": ratio(tp, tp + fp),
        "recall": ratio(tp, tp + fn),
        "specificity": ratio(tn, tn + fp),
        "accuracy": ratio(tp + tn, len(truth)),
        "f1": ratio(2 * tp, 2 * tp + fp + fn),
    }


def load_records(
    source_path: Path, adjudication_path: Path
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    source_payload = json.loads(source_path.read_text(encoding="utf-8"))
    adjudication_payload = json.loads(adjudication_path.read_text(encoding="utf-8"))
    source_records = source_payload["records"]
    adjudications = adjudication_payload["records"]
    source_repositories = {row["repository"] for row in source_records}
    adjudicated_repositories = {row["repository"] for row in adjudications}
    if source_repositories != adjudicated_repositories:
        missing = sorted(source_repositories - adjudicated_repositories)
        extra = sorted(adjudicated_repositories - source_repositories)
        raise ValueError(f"adjudication repository mismatch: missing={missing}, extra={extra}")
    if len(source_records) != len(source_repositories):
        raise ValueError("source contains duplicate repositories")
    if len(adjudications) != len(adjudicated_repositories):
        raise ValueError("adjudications contain duplicate repositories")
    return source_records, adjudications


def evaluate(
    source_path: Path, adjudication_path: Path
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    source_records, adjudications = load_records(source_path, adjudication_path)
    labels = {row["repository"]: row for row in adjudications}
    joined: list[dict[str, Any]] = []
    for source in source_records:
        label = labels[source["repository"]]
        joined.append(
            {
                "order": source["order"],
                "repository": source["repository"],
                "host": source["host"],
                "acquisition_status": source["status"],
                "cff_version": source.get("cff_version"),
                "manifest_path": (source.get("manifest") or {}).get("path"),
                "manifest_version": (source.get("manifest") or {}).get("version"),
                "predicted_gap": source.get("specificity_gap"),
                "primary_denominator": label["primary_denominator"],
                "manual_gap": label["manual_gap"],
                "adjudication": label["adjudication"],
                "notes": label["notes"],
            }
        )
    primary = [row for row in joined if row["primary_denominator"]]
    if any(row["manual_gap"] is None for row in primary):
        raise ValueError("primary denominator contains an unadjudicated record")
    truth = [bool(row["manual_gap"]) for row in primary]
    predictions = [row["predicted_gap"] is True for row in primary]
    checker = classification_metrics(truth, predictions)
    baseline = classification_metrics(truth, [False] * len(primary))
    gap_n = sum(truth)
    cff_missing_n = sum(row["acquisition_status"] == "CFF_MISSING" for row in joined)
    github_n = sum(row["host"] == "github" for row in joined)
    version_missing_n = sum(row["acquisition_status"] == "VERSION_MISSING" for row in primary)
    drift_n = sum(row["acquisition_status"] == "DRIFT" for row in primary)
    comparable = [
        row
        for row in primary
        if row["acquisition_status"] in {"MATCH", "NORMALIZED_MATCH", "DRIFT"}
    ]
    adjudication_coverage = len(primary) / len(primary) if primary else 0.0
    gates = {
        "minimum_cff_present": len(primary) >= 10,
        "gap_rate_at_least_0_30": gap_n / len(primary) >= 0.30 if primary else False,
        "precision_at_least_0_80": checker["precision"] >= 0.80,
        "recall_at_least_0_80": checker["recall"] >= 0.80,
        "complete_primary_adjudication": adjudication_coverage == 1.0,
    }
    if not gates["minimum_cff_present"] or not gates["complete_primary_adjudication"]:
        verdict = "INCONCLUSIVE"
    elif all(gates.values()):
        verdict = "SUPPORTED"
    else:
        verdict = "NOT SUPPORTED"
    result: dict[str, Any] = {
        "study_type": "preregistered out-of-sample exploratory validation",
        "research_question": (
            "Among JOSS issue-121 GitHub repositories with a root CITATION.cff, how often "
            "is software-version specificity missing or inconsistent with a unique static root "
            "package manifest?"
        ),
        "sample_n": len(joined),
        "github_n": github_n,
        "cff_present_n": len(primary),
        "cff_coverage": len(primary) / github_n if github_n else None,
        "confirmed_specificity_gap_n": gap_n,
        "confirmed_specificity_gap_rate": gap_n / len(primary) if primary else None,
        "confirmed_specificity_gap_wilson_95": wilson_interval(gap_n, len(primary)),
        "version_missing_n": version_missing_n,
        "confirmed_cross_file_drift_n": drift_n,
        "comparable_n": len(comparable),
        "drift_rate_among_comparable": drift_n / len(comparable) if comparable else None,
        "checker": checker,
        "baseline_all_specific": baseline,
        "adjudication_coverage": adjudication_coverage,
        "gates": gates,
        "sensitivity": {
            "missing_version_only_rate_among_cff": version_missing_n / len(primary)
            if primary
            else None,
            "drift_only_rate_among_cff": drift_n / len(primary) if primary else None,
            "drift_rate_among_comparable": drift_n / len(comparable) if comparable else None,
            "broader_missing_cff_or_specificity_gap_rate_among_github": (
                (cff_missing_n + gap_n) / github_n if github_n else None
            ),
            "broader_missing_cff_or_specificity_gap_n": cff_missing_n + gap_n,
        },
        "primary_verdict": verdict,
        "verdict_statement": {
            "SUPPORTED": (
                "SUPPORTED — The pilot evidence supports the stated hypothesis within the "
                "documented scope and limitations."
            ),
            "NOT SUPPORTED": "NOT SUPPORTED — The pilot evidence does not support the stated hypothesis.",
            "INCONCLUSIVE": (
                "INCONCLUSIVE — The available evidence is insufficient to distinguish among "
                "the competing explanations."
            ),
        }[verdict],
        "source_sha256": sha256_file(source_path),
        "adjudications_sha256": sha256_file(adjudication_path),
    }
    return result, joined


def write_outputs(
    output_dir: Path, result: dict[str, Any], joined: list[dict[str, Any]]
) -> dict[str, Any]:
    output_dir.mkdir(parents=True, exist_ok=True)
    deterministic_path = output_dir / "external-validation-results.json"
    deterministic_path.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    csv_path = output_dir / "screening.csv"
    with csv_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(joined[0]))
        writer.writeheader()
        writer.writerows(joined)
    hashes = {
        "external-validation-results.json": sha256_file(deterministic_path),
        "screening.csv": sha256_file(csv_path),
    }
    (output_dir / "SHA256SUMS.json").write_text(
        json.dumps({"files": hashes}, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    return hashes


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="evaluate-issue-121-specificity")
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--adjudications", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    started = time.perf_counter()
    tracemalloc.start()
    try:
        result, joined = evaluate(args.source, args.adjudications)
        hashes = write_outputs(args.output_dir, result, joined)
    except (OSError, ValueError, KeyError, json.JSONDecodeError) as exc:
        print(f"evaluation failed: {exc}")
        return 2
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    observation = {
        "runtime_seconds": time.perf_counter() - started,
        "tracemalloc_peak_bytes": peak,
        "peak_rss_kib": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
        "deterministic_files": hashes,
    }
    (args.output_dir / "performance-observation.json").write_text(
        json.dumps(observation, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
