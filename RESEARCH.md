# Research report

## Abstract

This exploratory pilot asked whether top-level software versions in `CITATION.cff` disagree with statically resolvable root package manifests in recently published Journal of Open Source Software (JOSS) repositories, and whether a deterministic checker can recover manually adjudicated cases. The first 20 papers displayed in JOSS issue 122 (June 2026) were frozen before screening. Nineteen linked to GitHub, 14 had a root `CITATION.cff`, and only five of those CFF files contained a top-level software version. After excluding dynamic manifests, versionless workspaces, missing metadata, and scope ambiguity, only two repositories were eligible. Both had same-scope version drift (`1.5.0` vs `1.8.0`; `1.0.0` vs `1.1.1`). The checker recovered both; a CFF-presence baseline recovered neither. Exact and conservative core-version analyses agreed, and deterministic output hashes matched across different hash seeds. Because the preregistered minimum was ten eligible repositories and no eligible negative case existed, prevalence and false-positive performance cannot be estimated credibly. **Verdict: INCONCLUSIVE.** The reusable contribution is a frozen benchmark, explicit exclusion taxonomy, standard-library CLI, CI workflow, machine-readable evidence, and a negative feasibility result showing that optional/missing and dynamic version metadata dominate this narrow sampling frame.

## Background

Software citation metadata can flow beyond a repository. CFF documentation describes integrations with GitHub, Zenodo, and Zotero, while a public CFF issue documents multiple Zenodo releases inheriting identical stale metadata after a CFF file was added. JOSS requires an identifiable release and archive during publication. These facts make cross-file version consistency a plausible integrity concern, but they do not establish its frequency or downstream harm.

## Research question

Among the first 20 papers displayed in JOSS issue 122, what proportion of GitHub-hosted repositories with both a root `CITATION.cff` and one unambiguous, statically resolvable supported root package manifest contain actionable top-level software-version drift? Can a deterministic checker recover the frozen manual labels?

## Hypotheses

- **H1:** at least 20% of eligible repositories have actionable drift, with checker precision ≥0.90 and recall ≥0.80.
- **H0:** drift is below 20%, or checker performance misses either threshold.
- **H2:** most apparent disagreements are non-actionable scope, dynamic-version, development-version, or normalization effects.

## Related work

See `docs/related-work.md`. The important distinction is that schema-valid CFF is not necessarily cross-file-consistent. CFF version is optional, so a valid file may contain no software version to compare.

## Methods

The protocol in `docs/methodology-preregistered.md` was frozen before completing version extraction. The ordered sample was the first 20 papers on the issue-122 table of contents. No replacements were made. The fixed manifest priority was `pyproject.toml`, `DESCRIPTION`, `Cargo.toml`, `Project.toml`, `package.json`, `pubspec.yaml`.

Eligibility required GitHub hosting, root CFF, one unambiguous same-scope root manifest, and static versions in both files. Missingness and ambiguity were reported separately. Exact comparison removed one leading `v`; sensitivity comparison also removed build/local metadata, common prerelease suffixes, and trailing numeric zero components.

Manual adjudication used repository structure and the extracted metadata fields. The checker did not execute package code, query package indexes, infer nested monorepo targets, or reconstruct historical releases.

## Data

The sampling frame and extracted records are in `data/raw/`. Records contain public repository identifiers, file paths, GitHub blob SHAs, extracted version strings, exclusion reasons, and labels. No personal data or private repositories were used. Full third-party files are not redistributed.

Dataset hashes are recorded in `research-manifest.yml`.

## Results

| Measure | Result |
|---|---:|
| Prespecified papers | 20 |
| GitHub repositories | 19 |
| Root CFF present | 14 |
| CFF with top-level version | 5/14 (35.7%) |
| Eligible same-scope static comparisons | 2 |
| Confirmed drift cases | 2 |
| Observed eligible drift | 100% |
| Wilson 95% interval | 34.2%–100% |
| Exact checker precision / recall | 1.00 / 1.00 |
| Presence-only baseline recall | 0.00 |
| Deterministic output hash | `c0a0bf18b1f8064f5fb3ba1c8e9ae6451a0d48d7931edb80d7510e56215a0725` |

### Confirmed cases

1. `bjmorgan/site-analysis`: CFF `1.5.0`, `pyproject.toml` `1.8.0`.
2. `gnaprs/scpviz`: CFF `1.0.0`, `pyproject.toml` `1.1.1`.

### Exclusions

- CFF missing: 5
- CFF top-level version missing: 9
- Dynamic manifest version: 2
- Non-GitHub host: 1
- Scope-ambiguous versionless workspace: 1

Counts sum to 18 exclusions; two repositories were eligible.

## Error analysis

No false negative or false positive occurred among the two eligible records, but both records were positive. Specificity is therefore unidentifiable. The main practical failure mode was not incorrect version comparison; it was inability to make a valid comparison because CFF version was optional/missing, the package version was dynamic, or the repository was a workspace.

The checker deliberately returns exit code 2 for insufficient or ambiguous evidence instead of converting these states into drift.

## Sensitivity analysis

Exact and core normalization both classified the two eligible cases as drift. Treating the single scope-ambiguous workspace as a non-drift denominator case changes the descriptive fraction to 2/3, but this post-hoc denominator violates the preregistered same-scope requirement and is not the primary result. Treating all other GitHub repositories as non-drift yields a conservative confirmed-case lower fraction of 2/19 (10.5%), which is not a prevalence estimate.

## Threats to validity

- **Selection:** one issue, first 20 entries, no randomization.
- **Eligibility attrition:** only two static same-scope comparisons.
- **No negative eligible case:** specificity and false-positive rate cannot be estimated.
- **Temporal mismatch:** repository default branches were inspected after publication; the study measures current branch state on 2026-07-24, not the exact publication snapshot.
- **Manual adjudication:** one reviewer and no independent blinded labeler.
- **Language coverage:** six root manifest formats, but nested monorepos and code-derived versions are excluded.
- **Impact:** no downstream citation or archive records were audited.

## Ethical and safety considerations

Only public metadata were processed. No credentials, personal datasets, behavioral data, vulnerability exploitation, or maintainer contact occurred. Repository names are retained because the findings must be independently verifiable; the report avoids attributing intent or negligence. Findings should be presented as fixable metadata states, not misconduct.

## Negative results

The pilot failed to obtain the preregistered minimum of ten eligible repositories. It therefore did not answer the population prevalence question. It also showed that a universal root-file checker is not credible without explicit handling of dynamic versions and monorepo scope. These are substantive negative feasibility results, not implementation failures.

## Conclusion

`INCONCLUSIVE — The available evidence is insufficient to distinguish among the competing explanations.`

The pilot confirms two current version mismatches and demonstrates a deterministic, low-cost detection workflow for unambiguous static repositories. It does not establish how common drift is, whether missing CFF versions are harmful, or whether the tool has low false-positive rates across ecosystems.

## Future work

A credible next study should preregister a stratified sample large enough to yield at least 30 eligible static comparisons, inspect publication-time tags rather than current default branches, include an independent second reviewer, add true negative repositories, and separately measure downstream Zenodo/GitHub citation propagation. Dynamic-version projects should be studied through release artifacts or tags, not guessed from source manifests.
