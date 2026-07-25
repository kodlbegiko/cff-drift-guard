# Owner actions for v0.2.0 release

The current connector cannot create Git tags or Releases. Perform these actions only after PR #2 is merged and all required checks are green.

```bash
git checkout main
git pull --ff-only
git tag -a v0.2.0 -m "v0.2.0 — JOSS issue-121 external validation"
git push origin v0.2.0
```

Create a GitHub Release from tag `v0.2.0` with title:

```text
v0.2.0 — JOSS issue-121 external validation
```

Release notes should state:

- primary specificity-gap verdict: `SUPPORTED` within the documented exploratory scope;
- 14/22 confirmed specificity gaps, including 13 missing versions and one confirmed drift;
- strict drift prevalence remains underpowered;
- deterministic result SHA-256: `abbd9cf74b5defbab20f757a8b878790063a596c96ba95d548aaeb66e1211ec0`;
- no claim of schema invalidity, population prevalence, or maintainer impact.

Do not create the release if the merged commit or hashes differ from the final PR report without regenerating and documenting the outputs.
