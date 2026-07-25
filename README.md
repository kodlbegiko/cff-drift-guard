# cff-drift-guard

## Research question

Among recent JOSS repositories with a root `CITATION.cff`, how often is software-version specificity missing or inconsistent with a unique static root package manifest?

## Why this matters

Software citation guidance calls for identifying the specific software version used. GitHub renders root CFF metadata, but schema-valid CFF files may omit the optional software `version`, and schema validation cannot establish agreement with `pyproject.toml`, `package.json`, `Cargo.toml`, `DESCRIPTION`, `Project.toml`, or `pubspec.yaml`.

## External-validation design and result

A frozen JOSS issue-121 frame contained 39 papers, 38 GitHub repositories, and 22 root CFF files. Complete single-reviewer adjudication confirmed **14/22 version-specificity gaps (63.6%; Wilson 95% interval 43.0%–80.3%)**: 13 files omitted a top-level software version and one same-scope CFF/manifest pair disagreed.

**Primary verdict: `SUPPORTED` within this exploratory scope.** All preregistered gates passed. This does **not** mean the files are schema-invalid or that every missing version should be changed. Strict cross-file drift remains underpowered: only 4 repositories were comparable and 1 drifted.

```bash
python scripts/evaluate_issue_121_specificity.py \
  --source data/issue-121/acquisition-deterministic.json \
  --adjudications data/issue-121/adjudications.json \
  --output-dir reproduced-issue-121
```

Expected deterministic result SHA-256:

```text
abbd9cf74b5defbab20f757a8b878790063a596c96ba95d548aaeb66e1211ec0
```

## Earlier issue-122 pilot

The original 20-paper issue-122 pilot found only two comparable repositories and both drifted. It remains **`INCONCLUSIVE`** because the preregistered minimum was ten eligible comparisons. The new issue-121 study does not rewrite that negative stopping-rule outcome; it tests a narrower, better-powered specificity question on an out-of-sample frame.

## Check a local repository

```bash
python -m pip install -e .
cff-drift-guard check /path/to/repository
```

Exit codes:

| Code | Meaning |
|---:|---|
| 0 | exact or conservative normalized match |
| 1 | unambiguous actionable drift |
| 2 | missing, dynamic, unsupported, or ambiguous evidence |
| 3 | benchmark blocked (reserved) |

## What the checker refuses to guess

- nested monorepo package selection;
- dynamic/VCS-derived package versions;
- publication-time state from current default branches;
- whether a missing CFF version is a maintainer error;
- whether different metadata scopes should have equal versions.

These return an informational state instead of a false drift claim.

## Full validation

```bash
python -m pip install -e ".[dev]"
ruff check .
ruff format --check .
mypy src
pytest --cov
python -m build

PYTHONHASHSEED=0 python scripts/evaluate_issue_121_specificity.py \
  --source data/issue-121/acquisition-deterministic.json \
  --adjudications data/issue-121/adjudications.json \
  --output-dir /tmp/issue121-a
PYTHONHASHSEED=321 python scripts/evaluate_issue_121_specificity.py \
  --source data/issue-121/acquisition-deterministic.json \
  --adjudications data/issue-121/adjudications.json \
  --output-dir /tmp/issue121-b
diff -u /tmp/issue121-a/external-validation-results.json \
  /tmp/issue121-b/external-validation-results.json
```

The acquisition script is optional and networked; the primary result reproduces offline from committed files.

## Repository map

- `EXTERNAL-VALIDATION-ISSUE-121.md` — complete external-validation report
- `RESEARCH.md` — original issue-122 pilot report
- `docs/methodology-issue-121-preregistered.md` — hypotheses and stopping rules
- `docs/frontier-candidates-2026-07-26.*` — 20-candidate selection record
- `docs/red-team-issue-121.md` — twelve adversarial critiques
- `docs/environment-audit-2026-07-26.md` — execution-capability audit
- `data/issue-121/` — frozen acquisition and adjudication records
- `results/issue-121/` — JSON/CSV results and hashes
- `research-manifest-issue-121.yml` — commands, hashes, metrics, and limits
- `docs/OWNER-ACTIONS-v0.2.0.md` — release actions unavailable to the connector

## Limitations

This is an exploratory study of one JOSS issue, not a population prevalence estimate. Default branches were observed in July 2026 rather than reconstructed at publication tags; one reviewer adjudicated cases; CFF software version is optional; only six root manifest formats are supported; no downstream citations, maintainer responses, or scientific outcomes were measured.

## License and citation

Code and original documentation are MIT licensed. Public source metadata remain subject to their original repositories and are represented by extracted values and blob hashes. Citation metadata are in `CITATION.cff`.
