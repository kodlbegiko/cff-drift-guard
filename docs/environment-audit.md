# Environment capability audit

Audit date: 2026-07-24, Asia/Taipei.

| Capability | Status | Evidence / consequence |
|---|---|---|
| Public web search | AVAILABLE | Current JOSS, CFF, GitHub, and technical documentation retrieved. |
| Academic/technical documents | AVAILABLE | HTML and public PDFs can be read; PDF visual analysis would require screenshots. |
| Public downloads | AVAILABLE | Public files can be downloaded through the provided download service. |
| Python execution | AVAILABLE | CPython 3.13.5, five logical CPUs visible to the container. |
| Node.js/TypeScript | AVAILABLE | Node.js 22 available; not needed for the selected study. |
| Install open-source dependencies | PARTIALLY AVAILABLE | Internal package index is reachable for some packages; the core tool therefore uses the standard library only. |
| File/chart/test creation | AVAILABLE | Local writable workspace and pytest/coverage available. |
| GPU | UNAVAILABLE | No GPU; irrelevant to the selected metadata study. |
| GitHub read/write | AVAILABLE | Authenticated as `kodlbegiko`; existing repositories, branches, files, PRs, merges, Actions status and logs are accessible. |
| Create new GitHub repository | UNAVAILABLE | Connector exposes no repository-creation action. Existing empty `kodlbegiko/cff-drift-guard` selected. |
| GitHub tag/release | UNAVAILABLE | Connector exposes no tag or Release creation action; exact owner actions are documented. |
| `gh` CLI | UNAVAILABLE | Publication uses the connected GitHub application. |
| Resources | PARTIALLY AVAILABLE | ~5.9 GiB RAM, ~39 GiB free disk, no swap; CPU-only pilot chosen. |
