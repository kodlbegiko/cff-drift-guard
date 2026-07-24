# cff-drift-guard

## Research question

Do software versions in `CITATION.cff` drift from the version in a package manifest, and can a deterministic CI check find unambiguous cases without treating missing or dynamic metadata as errors?

## Why this matters

CFF metadata can be displayed by GitHub and consumed by archival/citation tooling. A stale version can therefore escape the repository. Existing schema validation checks one file; it does not prove that the CFF agrees with `pyproject.toml`, `package.json`, `Cargo.toml`, `DESCRIPTION`, `Project.toml`, or `pubspec.yaml`.

## Pilot design and result

We froze the first 20 papers in JOSS issue 122 (June 2026), screened every linked repository, and compared only same-scope static versions. Of 20 papers, 19 linked to GitHub, 14 repositories had a root CFF, and only 5 CFF files contained a top-level software version. Just 2 repositories met the strict comparison rule; both contained drift.

**Primary verdict: `INCONCLUSIVE`.** The two cases are real, but the preregistered minimum was 10 eligible repositories and the eligible set contained no negative case. Do not interpret 2/2 as a population rate.

```bash
python -m pip install -e .
PYTHONHASHSEED=0 cff-drift-guard benchmark --output-dir reproduced-results
```

The deterministic benchmark output should have SHA-256:

```text
c0a0bf18b1f8064f5fb3ba1c8e9ae6451a0d48d7931edb80d7510e56215a0725
```

## Check a repository

```bash
cff-drift-guard check /path/to/repository
```

Exit codes:

| Code | Meaning |
|---:|---|
| 0 | exact or conservative normalized match |
| 1 | unambiguous actionable drift |
| 2 | missing, dynamic, unsupported, or ambiguous evidence |
| 3 | benchmark blocked (reserved) |

Example JSON:

```json
{
  "status": "DRIFT",
  "actionable": true,
  "cff_version": "1.0.0",
  "manifest_path": "pyproject.toml",
  "manifest_version": "1.1.1"
}
```

## What the tool refuses to guess

- nested monorepo package selection;
- dynamic/VCS-derived package versions;
- publication-time state from current default branches;
- whether a missing CFF version is an error;
- whether different metadata scopes should have equal versions.

These return a non-success informational state instead of a false drift claim.

## Reproduce the study

```bash
python -m pip install -e ".[dev]"
ruff check .
ruff format --check .
mypy src
pytest --cov
python -m build
PYTHONHASHSEED=0 cff-drift-guard benchmark --output-dir /tmp/a
PYTHONHASHSEED=321 cff-drift-guard benchmark --output-dir /tmp/b
diff -u /tmp/a/pilot-results-deterministic.json /tmp/b/pilot-results-deterministic.json
```

The frozen acquisition record is `data/raw/source-records.json`; `scripts/fetch_public_metadata.py` is an optional public GitHub acquisition helper and is not required to reproduce the committed result.

## Repository map

- `RESEARCH.md` — complete report
- `docs/methodology-preregistered.md` — hypotheses, definitions, stopping rule
- `docs/candidate-selection.md` — 20-candidate assessment
- `docs/red-team.md` — twelve adversarial critiques
- `data/raw/` — frozen sample and extraction records
- `results/published/` — JSON/CSV results and red-team output
- `src/` — standard-library checker and benchmark
- `tests/` — parser, metric, CLI, and end-to-end tests
- `research-manifest.yml` — commands, hashes, environment, limitations

## Limitations

This is an exploratory pilot, not a prevalence study. The sample is one JOSS issue, repository branches were observed on 2026-07-24 rather than at publication tags, only two repositories were eligible, and no independent second reviewer labeled cases. See `RESEARCH.md` before reusing the result.

## License and citation

Code and original documentation are MIT licensed. Public source metadata remain subject to their original repositories and are represented here mainly by extracted values and blob hashes. Citation metadata are in `CITATION.cff`.
