# Preregistered pilot protocol

**Freeze time:** 2026-07-24 (Asia/Taipei)  
**Study type:** exploratory pilot benchmark.

## Research question

Among the first 20 papers displayed in JOSS issue 122 (June 2026), what proportion of GitHub-hosted repositories with both a root `CITATION.cff` and a statically resolvable supported package manifest have disagreeing top-level software versions, and can a deterministic checker recover the manual labels?

## Hypotheses

- **H1:** At least 20% of eligible repositories contain actionable top-level CFF/manifest version drift; the checker reaches precision >= 0.90 and recall >= 0.80.
- **H0:** Fewer than 20% contain actionable drift, or the checker fails either performance threshold.
- **H2:** Apparent disagreements are mainly non-actionable scope differences, dynamic/development-version policies, or normalization artifacts.

## Operational definitions

- **Screened repository:** software repository linked from one of the first 20 issue-122 papers.
- **GitHub-hosted:** canonical JOSS repository link resolves to `github.com`.
- **CFF present:** root `CITATION.cff` is readable at the default branch.
- **Supported manifest:** root `pyproject.toml`, `DESCRIPTION`, `Cargo.toml`, `Project.toml`, `package.json`, or `pubspec.yaml` contains a statically resolvable project/package version.
- **Eligible:** GitHub-hosted + CFF present + one unambiguous supported manifest representing the same software scope.
- **Exact match:** trimmed strings match after removing one leading `v`/`V`.
- **Core-version match:** numeric release core matches after removing a leading `v`, local/build metadata, and trailing zero components.
- **Actionable drift:** exact and core versions differ and repository evidence does not document intentionally different scopes.
- **Non-actionable disagreement:** repository-level CFF describes a paper, monorepo, or software scope different from the compared manifest, or the manifest explicitly declares a development/dynamic version.
- **Missingness:** no CFF, no supported manifest, or no static version; reported separately and never counted as drift prevalence.

## Sample and exclusions

The ordered sampling frame is the first 20 papers displayed in JOSS issue 122. All 20 are screened; no replacement is made for non-GitHub repositories. Repositories are excluded from the primary prevalence denominator for non-GitHub hosting, missing CFF, unsupported/dynamic manifest, or ambiguous multi-package scope.

No personal data are collected. Stored data are public repository metadata, source file paths, blob hashes, extracted versions, and labels. Full third-party source files are not redistributed; only short metadata values and hashes are retained.

## Baseline

A **schema-presence baseline** reports success when `CITATION.cff` contains the required top-level citation fields and a syntactically non-empty `version`. It does not compare external metadata. Its expected drift recall is therefore zero unless it treats every CFF as suspicious, which would destroy precision.

## Procedure

1. Freeze and record the ordered 20-paper sampling frame.
2. Resolve the canonical software repository from each JOSS paper page.
3. Record hosting platform and default branch.
4. Read root `CITATION.cff` when present and record its blob hash.
5. Search the supported manifest paths in fixed priority order: `pyproject.toml`, `DESCRIPTION`, `Cargo.toml`, `Project.toml`, `package.json`, `pubspec.yaml`.
6. Extract static top-level package/project versions using deterministic parsers.
7. Two-pass manual labeling by the same reviewer: first from extracted fields, then from repository scope evidence for disagreements. Any unresolved case is `AMBIGUOUS`, not forced into match/drift.
8. Run the CLI checker over frozen machine-readable records.
9. Compare predictions with manual labels and calculate prevalence, precision, recall, F1, Wilson intervals, runtime, memory, and output hashes.
10. Repeat the analysis twice and compare SHA-256 hashes.

## Metrics

- screening counts and exclusion reasons;
- eligible fraction;
- actionable-drift prevalence with Wilson 95% interval;
- precision, recall, F1, false-positive and false-negative counts;
- parser coverage;
- wall-clock runtime and peak resident memory;
- deterministic result-file SHA-256;
- sensitivity under exact versus core-version matching and inclusion/exclusion of ambiguous cases.

## Stopping and decision rules

- Stop after all 20 prespecified papers are screened.
- If fewer than 10 repositories are eligible, the prevalence result is **INCONCLUSIVE**.
- H1 is supported only if: eligible n >= 10, observed actionable drift >= 20%, precision >= 0.90, and recall >= 0.80.
- H1 is not supported if eligible n >= 10 and observed actionable drift < 20%, or the checker misses its quality thresholds.
- Cases requiring package execution, network package-index resolution, or repository-history reconstruction are excluded rather than guessed.
- The criteria are frozen before version values are extracted.
