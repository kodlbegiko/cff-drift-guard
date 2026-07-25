# Frontier research candidate assessment — 2026-07-26

This assessment was completed before observing the JOSS issue-121 acquisition results. Scores use the mission rubric: importance 15, research-gap credibility 15, testability 15, current-environment feasibility 15, reproducibility 10, open-source reuse 10, innovation 10, growth 5, and maintenance 5.

## Ranked candidates

| Rank | Candidate question | Score | Feasible here | Primary failure risk |
|---:|---|---:|---|---|
| 1 | Among recent JOSS research-software repositories with a root CITATION.cff, how often is software-version specificity missing or inconsistent with a unique static root package manifest? | **93** | Yes; connector-backed GitHub acquisition and CPU-only deterministic analysis. | Too few root CFF files or too many dynamic/ambiguous manifests to support a credible denominator. |
| 2 | How often do research-software GitHub Actions workflows request write permissions that are not exercised by their jobs? | **84** | Partially; credible necessity labels need deeper action inspection and possibly sandbox execution. | Action internals and runtime branches make necessity difficult to prove without execution. |
| 3 | What fraction of recently published research PDFs fail machine-checkable accessibility prerequisites such as tagged structure, language metadata, bookmarks, and extractable reading order? | **79** | Partially; tool installation and manual reading-order evaluation are substantial. | PDF/UA conformance cannot be established reliably from lightweight checks alone. |
| 4 | How often do selected Taiwanese high-value public CSV datasets change schema or semantic units without machine-readable change notices? | **78** | Partially; current mission cannot wait for a meaningful prospective window. | Insufficient historical snapshots and too-short observation window. |
| 5 | For small open-source packages, how much do leading SBOM generators disagree on direct components, versions, and package identifiers when run from the same frozen source tree? | **78** | Partially; container/network and multi-ecosystem dependency acquisition are constrained. | Installing and normalizing many fast-moving tools dominates the research. |
| 6 | Do downloadable open educational content packs remain usable when all network access is removed? | **78** | Partially; browser automation and licensed package collection are required. | Licensing and acquisition heterogeneity limit a representative sample. |
| 7 | Can notebook execution-count and dependency evidence reliably detect figures or tables that are stale relative to source cells? | **78** | Partially; heterogeneous notebook environments limit full ground truth. | Notebook metadata is too weak to distinguish stale from intentionally preserved outputs. |
| 8 | Can source-level checks identify high-confidence accessibility failures in charts embedded in research websites without judging visual quality? | **76** | Partially. | Meaningful equivalence cannot be determined without human semantic review. |
| 9 | How often do public soil and water datasets expose measurement columns without machine-readable units or with units that conflict across metadata and files? | **75** | Partially; expert adjudication is the bottleneck. | Domain semantics and implicit laboratory conventions require experts. |
| 10 | How often do public-data portal license labels conflict with downloadable file metadata or linked terms? | **75** | Yes for a narrow pilot, but legal ambiguity limits strong conclusions. | Custom legal text resists deterministic equivalence decisions. |
| 11 | Do open low-cost environmental-sensor datasets provide enough calibration provenance to interpret reported values? | **73** | Partially; single-reviewer limitations are material. | The key evidence may be in papers or institutional records outside the dataset package. |
| 12 | Do research-software release tags, source archives, package manifests, and checksums agree on version identity? | **73** | Partially; large artifact downloads and registries increase complexity. | Ecosystem-specific version semantics create false conflicts. |
| 13 | How often do documentation examples contain token-shaped strings that are mistaken for live secrets or encourage unsafe credential handling? | **72** | Not preferred because of avoidable security-handling risk. | Detection could expose live credentials or create harmful redistribution. |
| 14 | Can repositories demonstrate a machine-traceable path from published figure files to generating scripts and source data? | **71** | Low for a credible multi-repository study. | Ground truth requires domain-specific execution and author knowledge. |
| 15 | Can a dependency-light validator catch high-confidence structural defects in small RO-Crate research packages while avoiding profile-specific false positives? | **70** | Partially; external validator installation is needed. | The proposed tool adds no value over maintained validators. |
| 16 | What proportion of dataset landing pages retain a downloadable artifact and stable checksum six months after citation? | **69** | No for the stated longitudinal question. | Mission duration cannot establish longitudinal decay. |
| 17 | Can a small bilingual benchmark reveal systematic errors in AI explanations of soil and environmental measurement units for Taiwanese learners? | **69** | No for a credible expert-validated benchmark. | Requires domain experts, multiple stable model endpoints, and a larger annotation budget. |
| 18 | Does a narrowly specified Agent Skill improve issue-report completeness over the same model without the skill on a frozen task set? | **67** | No credible controlled model access in the current environment. | No stable paid-API/model execution environment and strong model-version dependence. |
| 19 | Do public humanitarian HXL spreadsheets preserve tag validity and semantic consistency across updates? | **63** | Not preferred because of domain and sensitivity constraints. | Safety and context constraints outweigh marginal technical novelty. |
| 20 | Do repository FAIR badges or self-descriptions correspond to machine-observable findability, accessibility, interoperability, and reuse evidence? | **62** | Not advisable under the mission's narrow-test requirement. | The construct is too broad for a fair repository-only score. |

## Selected question

**Among recent JOSS research-software repositories with a root CITATION.cff, how often is software-version specificity missing or inconsistent with a unique static root package manifest?**

Selection rationale:

- It directly resolves the previous issue-122 pilot’s documented stopping-rule failure rather than inventing a new tool need.
- The issue-121 sampling frame was frozen in another study before this endpoint was defined, reducing result-driven sample selection.
- Public root metadata are sufficient for a CPU-only, deterministic, non-invasive experiment; no third-party code or personal data are required.
- Both positive and negative outcomes are reusable: a supported result yields a benchmark and conservative check; a null result prevents overinvestment in cross-file linting.
- The contribution is empirical external validation and a precise operational definition, not a claim that version fields are mandatory under the CFF schema.

## Why the other top five were not selected

- **#2 github-actions-permission-overreach (84/100):** Permission necessity cannot be inferred reliably from YAML alone; credible labels would require deeper inspection or controlled execution of third-party actions, increasing security and scope risk.
- **#3 research-pdf-accessibility (79/100):** Automated PDF accessibility preflight cannot establish reading-order or semantic adequacy without expert manual review and a heavier toolchain.
- **#4 public-data-schema-drift (78/100):** A meaningful public-data drift study requires a prospective observation window or reliable archives; the current mission cannot manufacture longitudinal evidence.
- **#5 sbom-generator-divergence (78/100):** A fair SBOM comparison requires multiple current toolchains, containerized ecosystem builds, and hand-built component ground truth, exceeding the available network and execution envelope.

## Evidence-state labels at selection time

- `KNOWN`: CFF and package-manifest validators exist; the prior issue-122 pilot produced only two comparable cases and therefore ended `INCONCLUSIVE`.
- `INFERRED`: Version omissions and cross-file drift may reduce the ability to identify the exact software object used, but omission is not automatically a schema violation or maintainer error.
- `UNKNOWN`: The issue-121 prevalence, the precision of a conservative rule, and whether omissions are deliberate publication choices.
- `DISPROVED`: The premise that a new generic version-checking tool is itself novel; existing tools already perform similar checks.
- `UNTESTABLE HERE`: Population-wide prevalence across journals and ecosystems, downstream citation harm, and maintainer remediation value.

## Full candidate records

The machine-readable companion `frontier-candidates-2026-07-26.json` contains all fifteen required fields and the nine-component score for every candidate.
