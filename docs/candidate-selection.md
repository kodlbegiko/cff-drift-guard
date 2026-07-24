# Candidate research questions and strict scoring

Each candidate was scored before inspecting candidate-specific outcomes. Scores are comparative triage judgments, not measurements of social impact. Status labels distinguish direct evidence from inference and current-environment limits.

## Ranked overview

| Rank | ID | Total | Feasible here | Research question |
|---:|---|---:|---|---|
| 1 | C01 | 96 | Yes | Among recently peer-reviewed JOSS software repositories, how often does CITATION.cff disagree with an authoritative package-manifest version, and can a deterministic checker detect actionable drift with low false positives? |
| 2 | C08 | 91 | Yes | How often do codemeta.json, CITATION.cff, and package manifests disagree on title, authorship, license, or repository URL? |
| 3 | C05 | 89 | Yes | Can notebook output staleness be detected by comparing cell-input hashes, execution counts, and stored outputs without rerunning the full notebook? |
| 4 | C02 | 87 | Partially | Do reproduction commands in recent research-software READMEs execute successfully in a clean CPU-only environment without undocumented manual steps? |
| 5 | C03 | 87 | Partially | How often do a JOSS paper version, repository release tag, archival deposit version, and package manifest disagree at publication time? |
| 6 | C04 | 87 | Yes | Are GitHub Actions permissions in recent research-software repositories broader than required by the workflow steps they execute? |
| 7 | C15 | 85 | Partially | Are downloadable offline educational content bundles actually self-contained when network access is disabled? |
| 8 | C12 | 84 | Yes | Do downloadable public datasets carry machine-readable license information consistent with their portal landing pages? |
| 9 | C06 | 83 | Partially | What fraction of figures in small research repositories can be traced to a generating script, source dataset, and exact command using only repository evidence? |
| 10 | C10 | 83 | Partially | Can missing or ambiguous measurement units in public environmental CSV files be detected using schema, column names, value ranges, and portal metadata? |
| 11 | C13 | 83 | Partially | How often do public sensor datasets omit calibration method, calibration date, or reference-instrument metadata needed for secondary analysis? |
| 12 | C14 | 83 | Yes | Can timezone ambiguity in public environmental time-series data be detected before analysis using timestamps and metadata alone? |
| 13 | C18 | 83 | Yes with strict safeguards | Can a benchmark distinguish real credential leakage from illustrative secret-like strings in public example configuration files? |
| 14 | C16 | 81 | Partially | What fraction of charts in open textbooks provide a text alternative sufficient to recover the chart's main quantitative claim? |
| 15 | C07 | 79 | Partially | Do declared dependency constraints in recent research packages uniquely resolve to reproducible environments after six months? |
| 16 | C11 | 78 | No for credible longitudinal result | How often do public-data API schemas change without a machine-readable version or migration notice? |
| 17 | C19 | 78 | No credible powered study here | Does adding an evidence ledger to AI coding-agent tasks reduce unsupported completion claims compared with a free-form completion report? |
| 18 | C20 | 78 | Partially | Can a minimal machine-readable research manifest materially reduce missing reproduction inputs in small open-source studies? |
| 19 | C17 | 77 | Partially | How much do common SBOM generators disagree on direct and transitive dependencies for the same small research software projects? |
| 20 | C09 | 74 | Partially | How many external links required by research-software installation guides are unavailable, redirected, or content-drifted after publication? |

## Full candidate dossiers

### 1. C01 — 96/100

- **Specific question:** Among recently peer-reviewed JOSS software repositories, how often does CITATION.cff disagree with an authoritative package-manifest version, and can a deterministic checker detect actionable drift with low false positives?
- **Public-interest importance:** Incorrect citation metadata can propagate into scholarly records, misattribute software versions, and weaken reproducibility.
- **Affected groups:** Research software authors, reviewers, archivists, indexers, and downstream researchers citing exact software versions.
- **Existing approaches:** CFF schema validators, GitHub citation rendering, manual JOSS review, package-manager metadata checks.
- **Concrete gap:** Existing validators largely validate each file in isolation; they do not consistently compare CFF version metadata against package manifests across ecosystems.
- **Available data:** Recent JOSS repositories with CITATION.cff and pyproject.toml, DESCRIPTION, Cargo.toml, Project.toml, or package.json.
- **Executable experiment:** Screen a bounded recent JOSS sample, manually label cross-file version state, compare a schema-presence baseline with a cross-file checker.
- **Quantitative metrics:** Eligible prevalence, actionable-drift rate, precision, recall, F1, parse coverage, runtime, peak memory, deterministic output hash.
- **Time:** 2–4 days pilot
- **Technical difficulty:** Medium
- **Ethics and safety:** Low; public repository metadata only.
- **Largest failure mode:** Too few eligible repositories or most version fields are intentionally omitted/dynamic.
- **Reusable output if successful:** CLI, benchmark dataset, labeling protocol, cross-ecosystem parsers, GitHub Action-ready workflow.
- **Knowledge if unsuccessful:** Eligibility and negative-prevalence dataset showing whether the suspected gap is practically rare.
- **Feasibility here:** Yes
- **Evidence status:** KNOWN/INFERRED
- **Score:** importance 14/15; gap 14/15; testability 15/15; feasibility 15/15; reproducibility 10/10; reuse 10/10; novelty 8/10; growth 5/5; maintenance 5/5.

### 2. C08 — 91/100

- **Specific question:** How often do codemeta.json, CITATION.cff, and package manifests disagree on title, authorship, license, or repository URL?
- **Public-interest importance:** Conflicting metadata harms discovery, attribution, and automated indexing.
- **Affected groups:** Authors, repositories, archives, citation systems.
- **Existing approaches:** Schema validators and metadata converters.
- **Concrete gap:** Cross-schema semantic reconciliation is less mature than per-schema validation.
- **Available data:** Public research repos containing two or more metadata formats.
- **Executable experiment:** Normalize common fields and manually label disagreements.
- **Quantitative metrics:** Conflict rate by field, precision, recall, parse coverage, ambiguity rate.
- **Time:** 3–5 days
- **Technical difficulty:** Medium
- **Ethics and safety:** Low.
- **Largest failure mode:** Eligible multi-metadata sample is too small.
- **Reusable output if successful:** Metadata crosswalk and drift checker.
- **Knowledge if unsuccessful:** Eligibility census.
- **Feasibility here:** Yes
- **Evidence status:** INFERRED
- **Score:** importance 13/15; gap 13/15; testability 14/15; feasibility 14/15; reproducibility 10/10; reuse 10/10; novelty 8/10; growth 5/5; maintenance 4/5.

### 3. C05 — 89/100

- **Specific question:** Can notebook output staleness be detected by comparing cell-input hashes, execution counts, and stored outputs without rerunning the full notebook?
- **Public-interest importance:** Stale outputs can silently contradict the current analysis code.
- **Affected groups:** Researchers, reviewers, students, data journalists.
- **Existing approaches:** nbval, nbmake, execution-count checks, Jupyter metadata.
- **Concrete gap:** Cheap preflight detection without execution is incomplete and may miss semantic changes.
- **Available data:** Version histories of public notebooks with commits and outputs.
- **Executable experiment:** Inject controlled edits and evaluate heuristics against known stale/fresh labels.
- **Quantitative metrics:** Precision, recall, mutation coverage, runtime, false alarms by notebook style.
- **Time:** 3–5 days
- **Technical difficulty:** Medium
- **Ethics and safety:** Low.
- **Largest failure mode:** Synthetic mutations fail to represent real stale-output behavior.
- **Reusable output if successful:** Notebook freshness benchmark and preflight tool.
- **Knowledge if unsuccessful:** Heuristic limitation matrix.
- **Feasibility here:** Yes
- **Evidence status:** INFERRED
- **Score:** importance 13/15; gap 12/15; testability 14/15; feasibility 14/15; reproducibility 10/10; reuse 9/10; novelty 8/10; growth 5/5; maintenance 4/5.

### 4. C02 — 87/100

- **Specific question:** Do reproduction commands in recent research-software READMEs execute successfully in a clean CPU-only environment without undocumented manual steps?
- **Public-interest importance:** Broken onboarding commands waste researcher time and impede independent verification.
- **Affected groups:** New users, reviewers, maintainers, educators.
- **Existing approaches:** CI, package tests, documentation testing, container images.
- **Concrete gap:** Project CI often tests source code but not the exact README quick-start path in a clean environment.
- **Available data:** Recent JOSS repositories and documented install/run commands.
- **Executable experiment:** Extract one declared quick-start command per repository and execute in isolated containers with bounded time.
- **Quantitative metrics:** Success rate, failure category, undocumented-step count, time-to-first-result, network/download volume.
- **Time:** 4–7 days
- **Technical difficulty:** High
- **Ethics and safety:** Low; public code, but arbitrary build scripts require sandboxing.
- **Largest failure mode:** Heterogeneous languages and long builds exceed resource limits.
- **Reusable output if successful:** README smoketest protocol, failure taxonomy, reproducible runner.
- **Knowledge if unsuccessful:** Resource-cost map and exclusion taxonomy.
- **Feasibility here:** Partially
- **Evidence status:** INFERRED
- **Score:** importance 14/15; gap 13/15; testability 14/15; feasibility 10/15; reproducibility 9/10; reuse 10/10; novelty 9/10; growth 5/5; maintenance 3/5.

### 5. C03 — 87/100

- **Specific question:** How often do a JOSS paper version, repository release tag, archival deposit version, and package manifest disagree at publication time?
- **Public-interest importance:** Publication-time version ambiguity can make exact scientific software reconstruction impossible.
- **Affected groups:** Authors, JOSS editors, archives, reproducibility auditors.
- **Existing approaches:** JOSS acceptance checks, Zenodo/GitHub releases, DOI metadata.
- **Concrete gap:** Checks are distributed across services and longitudinal consistency is not routinely machine-audited.
- **Available data:** JOSS papers, GitHub releases, Zenodo metadata, package manifests.
- **Executable experiment:** Cross-link recent JOSS papers and compare normalized versions across four sources.
- **Quantitative metrics:** Mismatch rate by source pair, unresolved-link rate, false-positive rate, manual minutes per repository.
- **Time:** 4–6 days
- **Technical difficulty:** High
- **Ethics and safety:** Low.
- **Largest failure mode:** Rate limits, inaccessible archives, or ambiguous publication snapshots.
- **Reusable output if successful:** Version-provenance benchmark and auditor.
- **Knowledge if unsuccessful:** Service-linkage failure map.
- **Feasibility here:** Partially
- **Evidence status:** KNOWN/INFERRED
- **Score:** importance 15/15; gap 13/15; testability 14/15; feasibility 10/15; reproducibility 8/10; reuse 10/10; novelty 9/10; growth 5/5; maintenance 3/5.

### 6. C04 — 87/100

- **Specific question:** Are GitHub Actions permissions in recent research-software repositories broader than required by the workflow steps they execute?
- **Public-interest importance:** Overprivileged automation increases supply-chain blast radius.
- **Affected groups:** Maintainers, contributors, package users, CI infrastructure.
- **Existing approaches:** GitHub permission defaults, Scorecard, actionlint, security guidance.
- **Concrete gap:** Inferring minimum permissions from arbitrary third-party actions remains incomplete and context-dependent.
- **Available data:** Public workflow YAML from a bounded JOSS sample.
- **Executable experiment:** Static permission analysis against manually reviewed workflow capabilities.
- **Quantitative metrics:** Overprivilege prevalence, precision/recall, permission-distance score, manual review time.
- **Time:** 3–5 days
- **Technical difficulty:** Medium-high
- **Ethics and safety:** Low; defensive public metadata analysis.
- **Largest failure mode:** Existing tools already cover most cases or action semantics cannot be inferred reliably.
- **Reusable output if successful:** Research-specific benchmark and permission linter rules.
- **Knowledge if unsuccessful:** Catalog of inference limits.
- **Feasibility here:** Yes
- **Evidence status:** KNOWN/INFERRED
- **Score:** importance 14/15; gap 11/15; testability 13/15; feasibility 14/15; reproducibility 10/10; reuse 9/10; novelty 7/10; growth 5/5; maintenance 4/5.

### 7. C15 — 85/100

- **Specific question:** Are downloadable offline educational content bundles actually self-contained when network access is disabled?
- **Public-interest importance:** Hidden network dependencies undermine access in low-bandwidth settings.
- **Affected groups:** Students, teachers, humanitarian and rural education programs.
- **Existing approaches:** PWA audits, offline-first testing, content packaging standards.
- **Concrete gap:** Offline claims are rarely tested against all embedded media and scripts.
- **Available data:** Open educational HTML/PWA bundles with explicit offline claims.
- **Executable experiment:** Run bundles in network-blocked browser and record failed resources and blocked tasks.
- **Quantitative metrics:** Task completion, missing-resource count, external-request count, bundle size.
- **Time:** 4–7 days
- **Technical difficulty:** High
- **Ethics and safety:** Low.
- **Largest failure mode:** Few legally downloadable bundles or browser automation unavailable.
- **Reusable output if successful:** Offline lesson pack validator and task benchmark.
- **Knowledge if unsuccessful:** Eligibility and packaging report.
- **Feasibility here:** Partially
- **Evidence status:** INFERRED
- **Score:** importance 15/15; gap 13/15; testability 14/15; feasibility 8/15; reproducibility 8/10; reuse 10/10; novelty 9/10; growth 5/5; maintenance 3/5.

### 8. C12 — 84/100

- **Specific question:** Do downloadable public datasets carry machine-readable license information consistent with their portal landing pages?
- **Public-interest importance:** License ambiguity deters lawful reuse and can cause improper redistribution.
- **Affected groups:** Researchers, civic technologists, data publishers.
- **Existing approaches:** DCAT, data-package metadata, portal license fields.
- **Concrete gap:** License statements often do not travel with downloaded artifacts.
- **Available data:** Government and NGO data portals plus downloaded files.
- **Executable experiment:** Compare portal license, file-adjacent metadata, and embedded metadata.
- **Quantitative metrics:** License absence, inconsistency, machine-readability, retrieval success.
- **Time:** 3–5 days
- **Technical difficulty:** Medium
- **Ethics and safety:** Low.
- **Largest failure mode:** Portal sampling becomes jurisdiction-specific.
- **Reusable output if successful:** License-mesh dataset and checker.
- **Knowledge if unsuccessful:** Portal-specific gap report.
- **Feasibility here:** Yes
- **Evidence status:** KNOWN/INFERRED
- **Score:** importance 13/15; gap 12/15; testability 14/15; feasibility 12/15; reproducibility 8/10; reuse 9/10; novelty 7/10; growth 5/5; maintenance 4/5.

### 9. C06 — 83/100

- **Specific question:** What fraction of figures in small research repositories can be traced to a generating script, source dataset, and exact command using only repository evidence?
- **Public-interest importance:** Untraceable figures obstruct claim verification and correction.
- **Affected groups:** Reviewers, coauthors, future maintainers.
- **Existing approaches:** Workflow systems, notebooks, Make/Snakemake, provenance standards.
- **Concrete gap:** Most tools require prior instrumentation; retrospective low-cost lineage extraction is weak.
- **Available data:** JOSS or replication repositories containing figures and scripts.
- **Executable experiment:** Build a static lineage heuristic and compare with manual labels.
- **Quantitative metrics:** Lineage coverage, precision/recall, unresolved nodes, manual minutes saved.
- **Time:** 5–8 days
- **Technical difficulty:** High
- **Ethics and safety:** Low.
- **Largest failure mode:** Repository structures too heterogeneous for credible labels.
- **Reusable output if successful:** Figure-lineage schema, benchmark, CLI.
- **Knowledge if unsuccessful:** Failure taxonomy for retrospective provenance.
- **Feasibility here:** Partially
- **Evidence status:** INFERRED
- **Score:** importance 14/15; gap 14/15; testability 11/15; feasibility 9/15; reproducibility 8/10; reuse 9/10; novelty 10/10; growth 5/5; maintenance 3/5.

### 10. C10 — 83/100

- **Specific question:** Can missing or ambiguous measurement units in public environmental CSV files be detected using schema, column names, value ranges, and portal metadata?
- **Public-interest importance:** Unit ambiguity can produce order-of-magnitude scientific and policy errors.
- **Affected groups:** Environmental researchers, agencies, civic-data users.
- **Existing approaches:** CF conventions, data dictionaries, validation rules.
- **Concrete gap:** CSV portals often separate metadata from files and use inconsistent field names.
- **Available data:** Public air, soil, water, and weather datasets with data dictionaries.
- **Executable experiment:** Create gold labels and compare header-only versus metadata-linked detectors.
- **Quantitative metrics:** Missing-unit prevalence, precision/recall, unit ambiguity, metadata retrieval success.
- **Time:** 5–8 days
- **Technical difficulty:** High
- **Ethics and safety:** Low.
- **Largest failure mode:** Cross-domain labels require specialist judgment and portal access is unstable.
- **Reusable output if successful:** Unit-contract schema, benchmark, validator.
- **Knowledge if unsuccessful:** Public-data metadata availability census.
- **Feasibility here:** Partially
- **Evidence status:** KNOWN/INFERRED
- **Score:** importance 15/15; gap 14/15; testability 12/15; feasibility 8/15; reproducibility 7/10; reuse 10/10; novelty 9/10; growth 5/5; maintenance 3/5.

### 11. C13 — 83/100

- **Specific question:** How often do public sensor datasets omit calibration method, calibration date, or reference-instrument metadata needed for secondary analysis?
- **Public-interest importance:** Uncalibrated sensor values can be misinterpreted as comparable measurements.
- **Affected groups:** Environmental researchers, communities, policymakers.
- **Existing approaches:** SensorML, SensorThings, domain guidelines.
- **Concrete gap:** Standards exist but real dataset adoption and completeness are uneven.
- **Available data:** Open low-cost air-quality and environmental sensor datasets.
- **Executable experiment:** Score required calibration metadata against a preregistered checklist.
- **Quantitative metrics:** Field completeness, dataset usability tiers, inter-rater agreement.
- **Time:** 4–7 days
- **Technical difficulty:** Medium-high
- **Ethics and safety:** Low.
- **Largest failure mode:** Required metadata differs materially by sensor domain.
- **Reusable output if successful:** Sensor metadata minimum profile and census.
- **Knowledge if unsuccessful:** Domain-specific requirement map.
- **Feasibility here:** Partially
- **Evidence status:** KNOWN/INFERRED
- **Score:** importance 15/15; gap 13/15; testability 12/15; feasibility 9/15; reproducibility 8/10; reuse 10/10; novelty 8/10; growth 5/5; maintenance 3/5.

### 12. C14 — 83/100

- **Specific question:** Can timezone ambiguity in public environmental time-series data be detected before analysis using timestamps and metadata alone?
- **Public-interest importance:** Timezone mistakes shift events and corrupt cross-source comparisons.
- **Affected groups:** Researchers, emergency planners, civic dashboards.
- **Existing approaches:** ISO 8601, timezone-aware libraries, schema validators.
- **Concrete gap:** Naive timestamps often lack offsets and portal metadata may be inconsistent.
- **Available data:** Public weather, air, and water time-series files.
- **Executable experiment:** Create labels from authoritative documentation and test rules.
- **Quantitative metrics:** Ambiguity prevalence, precision/recall, false alarms, affected-row count.
- **Time:** 3–5 days
- **Technical difficulty:** Medium
- **Ethics and safety:** Low.
- **Largest failure mode:** Ground truth is unavailable for ambiguous sources.
- **Reusable output if successful:** Timestamp preflight tool and benchmark.
- **Knowledge if unsuccessful:** Ground-truth availability report.
- **Feasibility here:** Yes
- **Evidence status:** INFERRED
- **Score:** importance 14/15; gap 11/15; testability 13/15; feasibility 12/15; reproducibility 9/10; reuse 9/10; novelty 7/10; growth 4/5; maintenance 4/5.

### 13. C18 — 83/100

- **Specific question:** Can a benchmark distinguish real credential leakage from illustrative secret-like strings in public example configuration files?
- **Public-interest importance:** False positives cause alert fatigue while real examples may normalize unsafe secret handling.
- **Affected groups:** Open-source maintainers and users copying examples.
- **Existing approaches:** gitleaks, trufflehog, GitHub secret scanning.
- **Concrete gap:** Public benchmarks for documentation/example contexts and realistic placeholders are limited.
- **Available data:** Public example configs plus controlled synthetic mutations; no use of live credentials.
- **Executable experiment:** Manually label safe placeholders and injected dummy-secret patterns, compare scanners/rules.
- **Quantitative metrics:** Precision, recall, false-positive classes, scan time.
- **Time:** 3–5 days
- **Technical difficulty:** Medium
- **Ethics and safety:** Moderate; must avoid collecting or exposing live secrets.
- **Largest failure mode:** Ethically safe labels cannot establish whether apparent live strings are valid.
- **Reusable output if successful:** Safe benchmark and context-aware rules.
- **Knowledge if unsuccessful:** False-positive taxonomy without redistributing sensitive strings.
- **Feasibility here:** Yes with strict safeguards
- **Evidence status:** INFERRED
- **Score:** importance 14/15; gap 11/15; testability 14/15; feasibility 11/15; reproducibility 9/10; reuse 9/10; novelty 8/10; growth 4/5; maintenance 3/5.

### 14. C16 — 81/100

- **Specific question:** What fraction of charts in open textbooks provide a text alternative sufficient to recover the chart's main quantitative claim?
- **Public-interest importance:** Inaccessible charts exclude blind and low-vision learners.
- **Affected groups:** Students with visual disabilities and educators.
- **Existing approaches:** WCAG alt-text guidance, accessibility checkers.
- **Concrete gap:** Presence checks do not evaluate whether text alternatives preserve the claim.
- **Available data:** Openly licensed HTML textbooks with charts.
- **Executable experiment:** Manual claim labels plus automated structural checks on a bounded sample.
- **Quantitative metrics:** Alt-text presence, claim coverage, inter-rater agreement, false-pass rate.
- **Time:** 5–8 days
- **Technical difficulty:** High
- **Ethics and safety:** Low; accessibility evaluation needs careful criteria.
- **Largest failure mode:** Semantic sufficiency is subjective without multiple raters.
- **Reusable output if successful:** Chart accessibility benchmark and rubric.
- **Knowledge if unsuccessful:** Rubric reliability results.
- **Feasibility here:** Partially
- **Evidence status:** KNOWN/INFERRED
- **Score:** importance 15/15; gap 14/15; testability 11/15; feasibility 8/15; reproducibility 7/10; reuse 9/10; novelty 9/10; growth 5/5; maintenance 3/5.

### 15. C07 — 79/100

- **Specific question:** Do declared dependency constraints in recent research packages uniquely resolve to reproducible environments after six months?
- **Public-interest importance:** Dependency drift causes delayed reproducibility failures.
- **Affected groups:** Researchers rerunning older analyses and package maintainers.
- **Existing approaches:** Lockfiles, environment.yml, renv, manifests, containers.
- **Concrete gap:** Cross-ecosystem longitudinal resolution is difficult and often not monitored.
- **Available data:** Historical package manifests and current package indexes.
- **Executable experiment:** Resolve archived constraints at two time points or against snapshots.
- **Quantitative metrics:** Resolution success, version-set divergence, vulnerable/yanked dependency count.
- **Time:** 5–10 days
- **Technical difficulty:** High
- **Ethics and safety:** Low.
- **Largest failure mode:** Historical package-index snapshots unavailable or environment builds too costly.
- **Reusable output if successful:** Dependency-drift benchmark.
- **Knowledge if unsuccessful:** Snapshot availability report.
- **Feasibility here:** Partially
- **Evidence status:** KNOWN/INFERRED
- **Score:** importance 15/15; gap 13/15; testability 12/15; feasibility 8/15; reproducibility 7/10; reuse 9/10; novelty 8/10; growth 5/5; maintenance 2/5.

### 16. C11 — 78/100

- **Specific question:** How often do public-data API schemas change without a machine-readable version or migration notice?
- **Public-interest importance:** Silent schema drift breaks public-interest analyses and services.
- **Affected groups:** Civic developers, researchers, journalists, agencies.
- **Existing approaches:** OpenAPI, data catalogs, monitoring tools.
- **Concrete gap:** Many portals expose no historical schema snapshots.
- **Available data:** Repeated snapshots of selected government APIs.
- **Executable experiment:** Collect daily schemas and classify additive/breaking changes.
- **Quantitative metrics:** Drift events, breaking-change rate, notice coverage, downtime.
- **Time:** Weeks-months
- **Technical difficulty:** Medium
- **Ethics and safety:** Low.
- **Largest failure mode:** Longitudinal observation period exceeds current session.
- **Reusable output if successful:** Schema-drift dataset and monitor.
- **Knowledge if unsuccessful:** Baseline snapshot registry.
- **Feasibility here:** No for credible longitudinal result
- **Evidence status:** UNTESTABLE HERE
- **Score:** importance 15/15; gap 14/15; testability 13/15; feasibility 3/15; reproducibility 7/10; reuse 10/10; novelty 8/10; growth 5/5; maintenance 3/5.

### 17. C19 — 78/100

- **Specific question:** Does adding an evidence ledger to AI coding-agent tasks reduce unsupported completion claims compared with a free-form completion report?
- **Public-interest importance:** Unsupported agent claims can cause unsafe deployments and wasted review effort.
- **Affected groups:** Developers, maintainers, organizations using coding agents.
- **Existing approaches:** SWE-bench tests, agent traces, CI, attestation frameworks.
- **Concrete gap:** Evidence quality for broad repository tasks is not standardized.
- **Available data:** Controlled repository tasks executed by one or more coding agents.
- **Executable experiment:** Randomize tasks to free-form versus required evidence ledger and blind-score claims.
- **Quantitative metrics:** Unsupported-claim rate, task correctness, reviewer time, evidence completeness.
- **Time:** 7–14 days
- **Technical difficulty:** High
- **Ethics and safety:** Low, but model/API access and variance are material.
- **Largest failure mode:** No stable access to multiple agent runs or adequate sample size.
- **Reusable output if successful:** Agent evidence protocol and benchmark.
- **Knowledge if unsuccessful:** Feasibility and power analysis.
- **Feasibility here:** No credible powered study here
- **Evidence status:** UNTESTABLE HERE
- **Score:** importance 15/15; gap 14/15; testability 13/15; feasibility 3/15; reproducibility 5/10; reuse 10/10; novelty 10/10; growth 5/5; maintenance 3/5.

### 18. C20 — 78/100

- **Specific question:** Can a minimal machine-readable research manifest materially reduce missing reproduction inputs in small open-source studies?
- **Public-interest importance:** Unspecified commands, hashes, seeds, and outputs obstruct independent reruns.
- **Affected groups:** Researchers, reviewers, maintainers.
- **Existing approaches:** RO-Crate, CodeMeta, ReproZip, workflow systems, data packages.
- **Concrete gap:** Full standards may be too heavy; the value of a minimal profile needs comparison.
- **Available data:** Small reproducible research repositories and synthetic omission cases.
- **Executable experiment:** Compare no manifest, README-only, and minimal manifest on task-completion by scripted checks or users.
- **Quantitative metrics:** Missing-input detection, setup time, manifest completion time, reproducibility score.
- **Time:** 5–10 days
- **Technical difficulty:** High
- **Ethics and safety:** Low.
- **Largest failure mode:** Without multiple independent users, value estimates are weak and circular.
- **Reusable output if successful:** Minimal schema and controlled benchmark.
- **Knowledge if unsuccessful:** Schema overlap analysis showing no need for a new profile.
- **Feasibility here:** Partially
- **Evidence status:** INFERRED
- **Score:** importance 14/15; gap 9/15; testability 11/15; feasibility 9/15; reproducibility 10/10; reuse 10/10; novelty 6/10; growth 5/5; maintenance 4/5.

### 19. C17 — 77/100

- **Specific question:** How much do common SBOM generators disagree on direct and transitive dependencies for the same small research software projects?
- **Public-interest importance:** Inconsistent SBOMs weaken vulnerability and supply-chain decisions.
- **Affected groups:** Maintainers, security teams, downstream users.
- **Existing approaches:** Syft, CycloneDX tools, package-manager exports, SPDX.
- **Concrete gap:** Cross-tool comparative benchmarks exist unevenly across ecosystems and research packages.
- **Available data:** Small open-source packages with lockfiles across Python/JS/Rust.
- **Executable experiment:** Generate multiple SBOMs in clean environments and compare component sets.
- **Quantitative metrics:** Jaccard overlap, missing direct/transitive dependencies, identifier disagreement, runtime.
- **Time:** 4–7 days
- **Technical difficulty:** High
- **Ethics and safety:** Low.
- **Largest failure mode:** Installing multiple external tools is blocked or results reflect configuration rather than tool quality.
- **Reusable output if successful:** SBOM disagreement benchmark and normalizer.
- **Knowledge if unsuccessful:** Tool-install and comparability report.
- **Feasibility here:** Partially
- **Evidence status:** KNOWN/INFERRED
- **Score:** importance 14/15; gap 11/15; testability 14/15; feasibility 7/15; reproducibility 8/10; reuse 9/10; novelty 7/10; growth 5/5; maintenance 2/5.

### 20. C09 — 74/100

- **Specific question:** How many external links required by research-software installation guides are unavailable, redirected, or content-drifted after publication?
- **Public-interest importance:** Link rot blocks installation and evidence access.
- **Affected groups:** Researchers, students, maintainers.
- **Existing approaches:** Link checkers, web archives, DOI systems.
- **Concrete gap:** Availability checks do not establish whether redirected content still satisfies the documented dependency.
- **Available data:** Published research-software READMEs and archived snapshots.
- **Executable experiment:** Check links, compare content fingerprints and manually classify criticality.
- **Quantitative metrics:** Broken/redirected/drifted rate, critical-link failure rate, archive recovery rate.
- **Time:** 3–5 days
- **Technical difficulty:** Medium
- **Ethics and safety:** Low; rate-limit responsibly.
- **Largest failure mode:** Content-drift labels become subjective.
- **Reusable output if successful:** Critical-link benchmark and checker.
- **Knowledge if unsuccessful:** Link criticality protocol.
- **Feasibility here:** Partially
- **Evidence status:** KNOWN/INFERRED
- **Score:** importance 12/15; gap 10/15; testability 12/15; feasibility 11/15; reproducibility 8/10; reuse 8/10; novelty 6/10; growth 4/5; maintenance 3/5.

