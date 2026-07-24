# Related work and gap

## Citation File Format

The Citation File Format (CFF) defines a human- and machine-readable `CITATION.cff`. Its official documentation states that GitHub surfaces the metadata, Zenodo can consume it through GitHub integration, and Zotero can import it. The CFF 1.2.0 schema permits a valid minimal file without `version`; version is recommended in the typical example but is not required.

- Specification repository: https://github.com/citation-file-format/citation-file-format
- Schema guide: https://github.com/citation-file-format/citation-file-format/blob/main/schema-guide.md
- Cross-release stale-metadata report: https://github.com/citation-file-format/citation-file-format/issues/374

## JOSS release workflow

JOSS uses checklist-driven review and asks authors at post-review to make a tagged release, archive it, and report a version and archive DOI. That establishes release-version importance, but the review checklist does not automatically assert equality between `CITATION.cff` and language package manifests.

- Review checklist: https://joss.readthedocs.io/en/latest/review_checklist.html
- Editorial guide: https://joss.readthedocs.io/en/latest/editing.html
- Issue 122 sampling frame: https://joss.theoj.org/toc/issue/122

## Existing tools

CFF validators such as `cffconvert` and schema validators test a CFF document's syntax and schema. Language package tools validate their own manifests. Generic metadata synchronizers exist, but this pilot found no mature, journal-oriented benchmark that explicitly separates:

1. absent CFF;
2. optional CFF version missingness;
3. dynamic manifest versions;
4. monorepo scope ambiguity;
5. normalization-only differences; and
6. actionable same-scope drift.

## Specific research gap

The gap is not “metadata validation” in general. It is a small, falsifiable question: whether recent peer-reviewed research software exposes statically comparable CFF/package versions, what defects appear when it does, and whether a conservative cross-file check is feasible without guessing package scope.
