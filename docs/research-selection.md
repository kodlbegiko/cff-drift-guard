# Research selection

## SELECTED RESEARCH QUESTION

**Among recently peer-reviewed Journal of Open Source Software (JOSS) repositories that contain both `CITATION.cff` and a supported package manifest, how often does the top-level CFF software version disagree with the manifest version, and can a deterministic cross-file checker identify actionable drift with low false-positive rates?**

This is an **exploratory pilot benchmark**, not a population estimate for all research software.

## Why selected

1. **Direct public-interest mechanism:** a stale software version in citation metadata can be rendered by GitHub and consumed by downstream archival/citation infrastructure.
2. **Concrete evidence of failure:** a public CFF issue documents repeated releases inheriting unchanged CFF metadata.
3. **Narrow, measurable gap:** schema validity and cross-file semantic consistency are different checks. The pilot tests only one field—software version—against explicit manifest authorities.
4. **Executable here:** public text metadata, CPU-only parsing, no personal data, no paid API, bounded sample.
5. **Falsifiable:** the suspected drift may be rare; a negative result remains useful as an eligibility/prevalence benchmark.
6. **Reusable output:** a small CLI, labeled benchmark, version-normalization protocol, machine-readable manifest, and CI example.

## Why the next four were not selected

### C08 — Multi-format metadata conflict (91/100)
Broader and potentially more useful, but title, author, license, and URL equivalence introduce entity-resolution and policy judgments. Starting with version equality creates a lower-ambiguity test and reusable foundation.

### C05 — Notebook output freshness (89/100)
Highly testable on mutations, but real-world ground truth is difficult without rerunning notebooks. A synthetic benchmark could overstate external validity.

### C02 — README clean-room reproduction (87/100)
Important but unsafe and resource-intensive in this environment: arbitrary install scripts, heterogeneous toolchains, large downloads, and long builds would create a biased sample.

### C03 — Publication/release/archive/manifest consistency (87/100)
More comprehensive, but requires robust release and archive API access plus historical publication snapshots. Current connector limitations would produce avoidable missingness and linkage ambiguity.

## Main unknown assumptions

- `UNKNOWN`: The eligible proportion of recent JOSS repositories is large enough for a useful pilot.
- `UNKNOWN`: Actionable version drift is common enough to observe in a bounded sample.
- `UNKNOWN`: A manifest version is always the intended authority for repository-level CFF metadata.
- `INFERRED`: Exact or normalized semantic-version equality is a defensible first-pass operational definition.
- `KNOWN`: CFF allows a top-level `version` field, GitHub renders repository citation metadata, and JOSS publication workflows use explicit software versions/releases.

## Evidence that would undermine the value

- Fewer than 10 eligible repositories after screening 30 recent JOSS repositories.
- All observed disagreements are intentional development-version policies rather than stale metadata.
- A mature maintained cross-ecosystem tool already performs the same semantic cross-check with equivalent evidence and workflow integration.
- The checker cannot achieve at least 0.90 precision and 0.80 recall against the preregistered manual labels.
- Manifest versions are dynamic or absent in most eligible ecosystems, making the proposed authority rule unusable.
