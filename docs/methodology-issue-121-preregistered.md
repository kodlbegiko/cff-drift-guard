# JOSS issue-121 external validation protocol

## Integrity checkpoint

The sample source, primary endpoint, conservative exclusion rules, and minimum denominator were fixed on branch `research/issue-121-specificity-validation` before the first successful acquisition artifact. The primary threshold (30% specificity-gap rate and at least 80% flag precision) was stated before inspecting the issue-121 output. This formal document was completed after acquisition but before the adjudication file and final evaluation were frozen. The additional 80% recall guardrail was inherited from the original pilot's conservative performance requirement and is reported explicitly.

## Research question

Among JOSS issue-121 GitHub repositories with a root `CITATION.cff`, how often is software-version specificity missing or inconsistent with a unique static root package manifest?

## Hypotheses

- **H1:** At least 30% of repositories in the primary denominator have a confirmed version-specificity gap, and the conservative checker achieves at least 80% precision and 80% recall against complete single-reviewer adjudication.
- **H0:** The confirmed gap rate is below 30%, or the checker fails either the precision or recall guardrail.
- **H2:** Missing versions may be deliberate because maintainers prefer citation of an associated article, use a concept DOI, or derive versions dynamically; therefore a specificity gap is not automatically a schema violation, maintenance defect, or evidence of downstream harm.

## Operational definitions

- **Root CFF:** a file named exactly `CITATION.cff` in the default-branch repository root.
- **Top-level software version:** a non-empty, unindented `version:` scalar in the root CFF. Nested article versions are ignored.
- **Version-specificity gap:** either (a) no top-level software version, or (b) a manually confirmed disagreement between the top-level CFF version and a unique static root manifest describing the same software scope.
- **Cross-file drift:** case (b) only. Dynamic, versionless, unsupported, workspace, or multiple-manifest cases are not labelled drift.
- **Comparable case:** one root CFF version plus exactly one supported, static, same-scope root manifest version.
- **Flag:** the acquisition rule predicts a gap for `VERSION_MISSING` or `DRIFT`.
- **Actionable defect:** not a primary label. Only confirmed same-scope drift is a candidate maintainer correction; missing versions are documented as specificity limitations.

## Dataset

- Sampling frame: 39 papers from JOSS issue 121, already frozen by an independent repository-level study before this endpoint was defined.
- Source commit: `5efa7e6b79dbd10b8e8439ca60bea9e43f27a00f` in `kodlbegiko/research-readme-smoketest`.
- GitHub-hosted papers: 38; one GitLab record is retained but excluded from acquisition.
- Primary denominator: every GitHub repository with a root CFF.
- Supported root manifests: `pyproject.toml`, `DESCRIPTION`, `Cargo.toml`, `Project.toml`, `package.json`, and `pubspec.yaml`.
- No personal data are collected. Public author names or emails inside metadata files are not copied into the published screening table.
- Third-party code is never cloned, installed, imported, or executed.

## Procedure

1. Fetch the frozen sample frame by immutable commit SHA.
2. For each GitHub repository, fetch only root CFF and supported manifest files through the GitHub Contents API.
3. Save repository, default branch, extracted versions, blob SHAs, parser status, and conservative classification.
4. Exclude non-GitHub records from acquisition and repositories without root CFF from the primary denominator.
5. Mark missing top-level CFF versions as candidate specificity gaps.
6. Compare versions only when exactly one static, non-ambiguous supported root manifest exists.
7. Manually adjudicate every repository, including all predicted positives and all primary-denominator negatives.
8. Freeze acquisition records and adjudications with SHA-256 hashes.
9. Run the offline evaluator twice under different `PYTHONHASHSEED` values and compare deterministic outputs.

## Baseline

The presence-only baseline treats every root CFF as version-specific and predicts no gaps. This approximates a workflow that checks only for CFF presence or schema validity without cross-source specificity checks.

## Metrics

- root-CFF coverage among GitHub repositories;
- confirmed specificity-gap count/rate and Wilson 95% interval;
- missing-version count/rate;
- confirmed drift count among all CFFs and comparable cases;
- precision, recall, specificity, accuracy, F1, false positives, and false negatives;
- baseline performance;
- runtime, peak traced memory, peak RSS, output hashes, and deterministic replay;
- adjudication coverage.

## Stopping and decision rules

- Fewer than 10 root-CFF repositories: `INCONCLUSIVE`.
- Incomplete primary-denominator adjudication: `INCONCLUSIVE`.
- All gates pass — gap rate >=30%, precision >=80%, recall >=80%: `SUPPORTED`.
- Minimum sample and adjudication gates pass but any effect/performance gate fails: `NOT SUPPORTED`.
- A specific acquisition or execution barrier that prevents a credible test: `BLOCKED`.

## Scope restrictions

The verdict applies only to this exploratory JOSS issue-121 sample and the stated operational definition. It does not estimate all research software, prove downstream citation errors, or establish that adding a version is always the correct maintainer action.
