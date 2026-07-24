# Owner actions blocked by the current GitHub interface

The connected GitHub application can write files, branches, pull requests, merges, and inspect Actions, but it does not expose repository metadata, tag, or Release creation in this environment.

After the merged commit is confirmed green:

1. Set repository description to: `Pilot benchmark and CI checker for CITATION.cff/package-manifest version drift.`
2. Add topics: `research-software`, `citation`, `cff`, `reproducibility`, `metadata`, `github-actions`.
3. Create annotated tag `v0.1.0` at the merged commit.
4. Create GitHub Release `v0.1.0` using `CHANGELOG.md`; attach the generated source distribution and wheel from CI if desired.
5. Optionally archive the release with Zenodo and replace the placeholder citation guidance with the versioned DOI.

These actions are not marked complete in the research report.
