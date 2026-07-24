#!/usr/bin/env python3
"""Generate machine-readable adversarial checks for the pilot conclusions."""

from __future__ import annotations

import json
from pathlib import Path

SOURCE = Path("data/raw/source-records.json")
OUT = Path("results/published/red-team-results.json")
records = json.loads(SOURCE.read_text(encoding="utf-8"))
eligible = [r for r in records if r["manual_label"] in {"DRIFT", "MATCH"}]
github = [r for r in records if r["host"] == "github"]
cff = [r for r in records if r["cff_present"]]
versioned_cff = [r for r in cff if r["cff_version"]]
drifts = [r for r in eligible if r["manual_label"] == "DRIFT"]

result = {
    "sample_concentration": {
        "journal": "JOSS",
        "issue": 122,
        "month": "2026-06",
        "sample_n": len(records),
    },
    "prevalence_bounds": {
        "eligible_observed": len(drifts) / len(eligible),
        "lower_if_all_other_github_repos_non_drift": len(drifts) / len(github),
        "lower_if_all_other_cff_repos_non_drift": len(drifts) / len(cff),
        "upper_if_all_ineligible_github_repos_drift": 1.0,
    },
    "identifiability": {
        "eligible_n": len(eligible),
        "positive_n": len(drifts),
        "negative_n": len(eligible) - len(drifts),
        "specificity_estimable": (len(eligible) - len(drifts)) > 0,
        "cff_version_optional_and_missing_n": len(cff) - len(versioned_cff),
        "cff_version_present_fraction": len(versioned_cff) / len(cff),
    },
    "stronger_baseline": {
        "description": (
            "A direct two-file raw-string comparator is algorithmically equivalent "
            "to exact-mode checking on eligible records."
        ),
        "consequence": (
            "The contribution is the explicit protocol, exclusions, benchmark records, "
            "CI integration, and audit trail—not a novel comparison algorithm."
        ),
    },
    "maintenance": {
        "supported_manifest_formats": 6,
        "known_unhandled_classes": [
            "nested monorepo package manifests",
            "runtime-derived versions",
            "language-specific version modules",
            "release/tag history",
        ],
    },
    "conclusion_adjustments": [
        "Do not estimate population prevalence from two eligible cases.",
        (
            "Do not claim specificity or false-positive control from an eligible set "
            "with zero negative cases."
        ),
        "Treat the two mismatches as confirmed case findings, not a representative rate.",
        (
            "Treat CFF version missingness as a secondary descriptive result because "
            "version is optional in CFF 1.2.0."
        ),
    ],
}
OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
print(json.dumps(result, indent=2, sort_keys=True))
