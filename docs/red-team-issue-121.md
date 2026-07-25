# Red-team and falsification review — JOSS issue 121

## 1. The problem may not matter

**Evidence/test:** CFF `version` is optional under schema 1.2.0, and many projects prefer an article citation. The study therefore does not call omissions invalid. The narrower public-interest claim is that an omitted version cannot itself identify the exact software release.

**Accepted correction:** The result supports a metadata-specificity gap, not demonstrated scientific harm.

## 2. The sample may be severely biased

**Evidence/test:** All records come from one recent JOSS issue. JOSS projects are unusually documentation-aware and may not represent general GitHub software.

**Accepted correction:** No population-wide prevalence claim is made. The sample frame is published and reusable for replication on other issues.

## 3. Existing tools may already be sufficient

**Evidence/test:** `same-version` already checks `CITATION.cff` and package/version sources; CFF validators and `cffr` also exist.

**Accepted correction:** Tool novelty is disproved. The contribution is the frozen external-validation dataset, operational definition, failure analysis, and conservative benchmark.

## 4. The metric may be wrong

**Evidence/test:** Treating missing versions as gaps could conflate project-level citation with release-level citation.

**Sensitivity:** Missing-version-only rate is 13/22 (59.1%); confirmed drift-only rate is 1/22 (4.5%).

**Accepted correction:** The primary metric is explicitly “version specificity,” not overall citation quality or maintainability.

## 5. The result may be a property of JOSS authoring practice

**Evidence/test:** Several CFF files use `preferred-citation` for the JOSS article. This may encourage article-level rather than software-version metadata.

**Accepted correction:** The report treats this as a plausible alternative explanation and proposes cross-journal replication.

## 6. Information leakage may inflate performance

**Evidence/test:** The parser rule and manual label both inspect the same literal top-level field; extraction precision is therefore not a general predictive-model result. The sample itself was frozen before endpoint selection, but adjudication was not blinded.

**Accepted correction:** Precision/recall are characterized as extraction agreement. The prevalence estimate, not model generalization, is the main empirical result.

## 7. The baseline may be too weak

**Evidence/test:** The all-specific baseline represents presence/schema-only checking but not `same-version` or a release workflow.

**Accepted correction:** Baseline improvement does not establish superiority over mature tools. Future work should compare against `same-version`, `cffr`, and HERMES on the same frozen repositories.

## 8. Numerical processing may be wrong

**Test:** Unit tests cover confusion matrices, thresholds, Wilson intervals, repository-set equality, duplicate detection, output hashes, and the full frozen study. Machine-readable counts tie to the 39-row screening file.

**Result:** No remaining arithmetic discrepancy found.

## 9. Results may not generalize

**Evidence/test:** The 95% Wilson interval for 14/22 is 42.95%–80.27%, but this interval reflects sampling variation under assumptions that do not make one journal issue representative.

**Accepted correction:** The interval is descriptive for the bounded sample, not a license to generalize.

## 10. Maintenance cost may exceed value

**Evidence/test:** Six manifest formats already require parser maintenance, while only four repositories were strictly comparable.

**Accepted correction:** The checker remains conservative and dependency-free. Productization beyond the benchmark is not justified without external adoption or broader replication.

## 11. AI-native metadata reasoning may replace the method

**Evidence/test:** A language model could infer package scope, but that would introduce nondeterminism, cost, privacy questions, and difficult-to-audit false positives.

**Accepted correction:** AI may assist future adjudication, but deterministic literal checks remain useful as a reproducible baseline.

## 12. Maintainers may have no adoption incentive

**Evidence/test:** Only one confirmed same-scope drift case is an obvious correction candidate. Missing versions may be deliberate.

**Accepted correction:** No outreach or remediation-value claim is made. Maintainer intervention remains future work and should be measured rather than assumed.

## Falsification outcome

The main specificity-gap hypothesis survives the preregistered gates. Stronger claims do not survive:

- “Schema validation is failing”: **DISPROVED as framing** — version is optional.
- “Stale cross-file drift is widespread”: **INCONCLUSIVE** — only four comparable repositories and one confirmed drift.
- “A new checker is novel”: **DISPROVED** — overlapping tools exist.
- “Maintainer remediation creates value”: **UNTESTABLE HERE**.
