# Red-team and falsification report

This section assumes the pilot is wrong or overstated and tests twelve ways that could be true.

## 1. The problem may not be important

**Evidence against dismissal:** CFF metadata is consumed by GitHub, Zenodo, and citation tools. The official CFF project documents those integrations, and an open CFF issue describes repeated Zenodo records inheriting stale CFF metadata after new releases. Two sampled repositories contain concrete version discrepancies.

**Accepted limitation:** This pilot did not measure downstream miscitation, archive corruption, or user harm. It establishes a plausible propagation route and two current defects, not quantified impact.

## 2. The sample is biased

**Test:** The sample was the first 20 entries in one JOSS issue and was not random across journals, years, languages, or project maturity.

**Result:** Criticism accepted. The sample is useful for a bounded feasibility study only. It cannot estimate the prevalence of drift in all research software.

## 3. Existing tools may already be sufficient

**Test:** The official CFF schema validator can accept a minimal CFF without `version`; version is optional. A schema-presence baseline therefore cannot identify cross-file disagreement.

**Result:** Existing per-file validators are complementary but do not answer this cross-file consistency question. However, a simple raw-string comparator can perform the central comparison once scope and static-version eligibility are resolved.

## 4. The metric may be wrong

**Test:** Exact and conservative core-version comparisons were run. Dynamic manifests, root workspaces, and differing package scope were excluded before prevalence calculation.

**Result:** Both confirmed cases remain drift under exact and core normalization. Scope exclusions sharply reduce sample size, showing that naive mismatch counting would be misleading.

## 5. The result may be a property of this dataset

**Test:** The evidence is concentrated in one recent JOSS issue. Worst-case bounds were computed: confirmed drift is only 2/19 (10.5%) if every other GitHub repository is treated as non-drift, while the upper bound is uninformative.

**Result:** Criticism accepted. The 2/2 eligible fraction must not be generalized.

## 6. Information leakage may inflate evaluation

**Test:** The checker and manual labels use the same public version fields; no model was trained. Scope labels were decided from repository structure before checker scoring.

**Result:** There is no train/test leakage in the machine-learning sense, but evaluation is not independent human adjudication. Accuracy claims are restricted to deterministic recovery of the frozen labels.

## 7. The baseline may be too weak

**Test:** A stronger baseline—a direct two-file string comparator—is algorithmically equivalent to exact-mode checking for eligible repositories.

**Result:** Criticism accepted. The novel value is not a sophisticated comparison algorithm. It is the eligibility protocol, explicit missingness taxonomy, frozen benchmark, machine-readable evidence, CI integration, and deterministic audit trail.

## 8. Statistical handling may be wrong

**Test:** Wilson 95% interval for 2/2 is 34.2%–100%, and the preregistered minimum eligible sample was 10.

**Result:** The stopping rule is correctly triggered. The prevalence hypothesis is **INCONCLUSIVE**.

## 9. The result may not generalize

**Test:** Manifest support spans six common formats, but the observed eligible cases are both Python projects; monorepos, R, Julia, Rust workspaces, Dart workspaces, and runtime-derived versions are underrepresented or excluded.

**Result:** Criticism accepted. Generalization to other ecosystems is unknown.

## 10. Maintenance cost may exceed value

**Test:** The runtime checker uses only Python's standard library and 280 executable source statements, but every new manifest type and monorepo convention adds policy surface.

**Result:** Maintenance is low for root/static checks and high for universal repository inference. Version 0.1 deliberately refuses ambiguous cases rather than guessing.

## 11. AI-native inspection may replace the method

**Test:** An AI agent can read two files, but deterministic CI requires stable rules, exit codes, repeatable outputs, and no paid API.

**Result:** AI can assist scope adjudication, but does not remove the need for an auditable baseline. Future agents could subsume the interface, not the underlying consistency invariant.

## 12. Maintainers may have no adoption incentive

**Evidence:** CFF `version` is optional, and 9 of 14 CFF-bearing repositories omitted it. Authors may intentionally prefer paper citation metadata or dynamic release workflows.

**Result:** Criticism partly accepted. A blocking CI rule is inappropriate by default. The tool should be opt-in, warn on missingness, and fail only on unambiguous static mismatches.

## Revised conclusion after red-team review

- **Confirmed:** two current, same-scope CFF/manifest version mismatches in the frozen sample.
- **Confirmed:** top-level CFF version completeness was 5/14 (35.7%) in this sample.
- **Not established:** prevalence across JOSS or research software, specificity on true negative repositories, downstream citation harm, or maintainer adoption.
- **Primary verdict remains:** `INCONCLUSIVE`.
