# External validation of version specificity in research-software CITATION.cff files

## Abstract

This exploratory study asks whether root `CITATION.cff` files in a frozen sample of recent Journal of Open Source Software repositories identify a software version, and—when a unique static root package manifest exists—whether the two versions agree. The issue-121 sampling frame contained 39 papers, 38 GitHub repositories, and 22 root CFF files. Complete single-reviewer adjudication confirmed 14 version-specificity gaps among those 22 CFF files (63.6%; Wilson 95% interval 43.0%–80.3%): 13 files omitted a top-level software version and one same-scope CFF/manifest pair disagreed. The deterministic rule matched all adjudications in this bounded dataset; a presence-only baseline missed all 14 gaps. However, only four repositories were strictly comparable across CFF and a unique static manifest, and only one had confirmed drift. The primary specificity-gap hypothesis is **SUPPORTED** within scope; a stronger claim that stale cross-file drift is widespread remains **INCONCLUSIVE**.

## Background

Software citation guidance emphasizes identifying the specific software version used. A root `CITATION.cff` is human- and machine-readable and is rendered by GitHub’s citation interface. CFF schema validation establishes structural validity, but the software `version` field is optional and schema validation cannot establish agreement with package manifests. Existing systems already address parts of the workflow: `cffconvert` and `cffr` validate/convert CFF, `same-version` compares version sources, CodeMeta crosswalks metadata vocabularies, and HERMES harvests and publishes research-software metadata in CI.

The prior issue-122 pilot in this repository found two comparable repositories and both drifted, but it stopped as `INCONCLUSIVE` because its preregistered minimum was ten eligible comparisons. The present study changes the primary denominator before issue-121 adjudication: it measures version specificity across every root CFF, then reports strict cross-file drift separately.

## Research question

Among JOSS issue-121 GitHub repositories with a root `CITATION.cff`, how often is software-version specificity missing or inconsistent with a unique static root package manifest?

## Related work

- Smith et al., *Software Citation Principles*, PeerJ Computer Science 2:e86, DOI `10.7717/peerj-cs.86`.
- Katz et al., *Software Citation Implementation Challenges*, arXiv `1905.08674`.
- Schindler et al., *A multi-level analysis of data quality for formal software citation*, arXiv `2306.17535`.
- Citation File Format schema and guidance: `citation-file-format/citation-file-format`.
- `same-version` package, CFF validators/converters, `cffr`, CodeMeta crosswalks, and HERMES publication workflows.

These establish the importance and tooling context but do not provide this frozen out-of-sample prevalence/adjudication result.

## Methods

### Design

Preregistered out-of-sample exploratory validation. The frozen source commit, endpoint, denominator, conservative exclusions, and minimum sample were set before the first successful issue-121 acquisition artifact. Full criteria are in `docs/methodology-issue-121-preregistered.md`.

### Data

The source frame was frozen at commit `5efa7e6b79dbd10b8e8439ca60bea9e43f27a00f` in `kodlbegiko/research-readme-smoketest`. The acquisition script fetched only public root metadata through the GitHub Contents API and recorded blob SHAs. No third-party code was cloned or executed, and no private or personal dataset was assembled.

### Operational labels

A confirmed specificity gap is either:

1. no top-level CFF software `version`; or
2. a manually confirmed same-scope disagreement with a unique static supported root manifest.

Dynamic, ambiguous, unsupported, or missing manifests are not called drift. Missing versions are not called schema violations or proven maintenance errors.

### Baseline and metrics

The baseline predicts that every root CFF is version-specific. Metrics include coverage, confirmed gap prevalence, Wilson interval, confusion matrix, precision/recall, drift among comparable records, resource use, hashes, and deterministic replay.

### Decision rule

`SUPPORTED` requires at least ten root CFF files, complete primary adjudication, gap rate at least 30%, precision at least 80%, and recall at least 80%.

## Results

| Measure | Result |
|---|---:|
| Papers in frozen frame | 39 |
| GitHub repositories | 38 |
| Root `CITATION.cff` files | 22 (57.9% of GitHub repositories) |
| Confirmed specificity gaps | 14/22 (63.6%) |
| Wilson 95% interval | 43.0%–80.3% |
| Missing top-level versions | 13/22 (59.1%) |
| Confirmed same-scope drift | 1/22 (4.5%) |
| Strictly comparable CFF/manifest pairs | 4 |
| Drift among comparable pairs | 1/4 (25.0%) |
| Checker precision / recall | 100% / 100% |
| Presence-only baseline accuracy | 36.4% |
| Primary verdict | **SUPPORTED** |

All five decision gates passed. The published deterministic result file has SHA-256 `abbd9cf74b5defbab20f757a8b878790063a596c96ba95d548aaeb66e1211ec0`.

## Error analysis

The first acquisition incorrectly reported two drift cases. The R `DESCRIPTION` parser did not recognize the valid field name `Authors@R`; continuation lines were appended to the preceding `Version` value, creating a false disagreement for `cwru-sdle/geospatialsuite`. Manual inspection exposed the error. The parser was corrected to accept `@` in field names and a regression test was added. The final result contains one confirmed drift case: `GroupiSP/himap`, whose root CFF reported `v1.3.0` while the static root `pyproject.toml` reported `1.4.0` at acquisition.

This failure is material: without complete adjudication, the uncorrected drift count would have been inflated by 100% (2 instead of 1).

## Sensitivity analysis

- **Missing-version-only:** 13/22 (59.1%). The main effect is not dependent on the one drift case.
- **Drift-only among all root CFFs:** 1/22 (4.5%). This does not support a claim that stale versions are common.
- **Drift among comparable pairs:** 1/4 (25.0%). The denominator is too small for a stable estimate.
- **Broader readiness gap:** 30/38 GitHub repositories (78.9%) either lacked a root CFF or had a confirmed specificity gap. This is secondary and combines two distinct conditions.
- **Presence-only baseline:** zero recall for the 14 gaps, confirming that file presence alone cannot measure version specificity.

## Threats to validity

1. One JOSS issue is not representative of all research software.
2. Default branches were observed at acquisition time, not reconstructed at publication tags.
3. Adjudication had one reviewer and was not blinded.
4. Version omission may be deliberate and may coexist with a valid article or concept-level citation.
5. Supported manifest formats do not cover all ecosystems or nested monorepos.
6. Extraction performance is partly mechanical because the operational label includes a literal top-level field.
7. No downstream citation strings, papers citing the software, or maintainer behavior were measured.

## Ethical and safety considerations

Only public repository metadata were processed. The released screening table excludes copied author contact information. Third-party code was not executed. Repository-level findings are described neutrally; absence of a version is not framed as misconduct, negligence, or invalid CFF.

## Negative results

- A generic version checker is not novel; `same-version` and ecosystem-specific tooling already overlap.
- Widespread actionable drift is not established: only one confirmed drift among 22 root CFFs and four comparable pairs.
- Maintainer intervention value, downstream reproducibility impact, and cross-journal generalization remain untested.
- The original parser produced a real false positive, demonstrating that seemingly simple metadata extraction requires adversarial fixtures and complete review.

## Conclusion

**SUPPORTED — The pilot evidence supports the stated hypothesis within the documented scope and limitations.**

The result supports a narrow claim: version specificity was absent or inconsistent in 14 of 22 root CFF files in this frozen JOSS issue-121 sample, and a conservative deterministic extraction agreed with complete adjudication. It does not show that these CFF files are schema-invalid, that most omissions should be “fixed,” that drift is widespread, or that downstream science was harmed.

## Future work

Replicate the protocol across additional pre-frozen journal issues, add independent adjudicators, reconstruct publication-time tags, compare directly with maintained tools, and measure whether maintainers accept changes and whether resulting citations become more release-specific.
