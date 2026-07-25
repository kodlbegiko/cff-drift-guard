# Environment capability audit — 2026-07-26

## AVAILABLE

- Public web search and retrieval through the hosted research tool.
- Reading public academic papers, technical documentation, and GitHub metadata.
- Python 3.13.5, Node.js 22.16.0, npm 10.9.2, Git 2.47.3, GCC, Make, jq, and SHA-256 tools.
- Local file creation, deterministic scripts, tests, JSON/CSV generation, and static reports.
- GitHub Connector access to owned public repositories with admin/push permission.
- Branch creation, file changes, pull requests, Actions status/jobs/logs, and artifact download.
- GitHub-hosted Python 3.11/3.13 CI with PyPI dependency installation.
- Approximately 39 GB free disk and 5.1 GiB available memory at audit time.

## PARTIALLY AVAILABLE

- Package installation: unavailable from the local container because it has no direct DNS/network access, but available in GitHub Actions.
- GitHub operations: repository reads/writes, PRs, and CI are available; repository creation, release/tag creation, and repository-topic/description updates are not exposed by the current connector.
- CI logs: job and step status are directly available; long logs may be truncated, so a bounded diagnostic artifact was used where exact formatter output was required.
- Charts: local generation is available, but the selected experiment is better communicated with exact counts, intervals, and machine-readable tables than a decorative chart.

## UNAVAILABLE

- Direct outbound internet from the local execution container.
- `gh` CLI authentication.
- GPU acceleration and large-model execution; neither is required for this study.
- Creating a new GitHub repository or GitHub Release through the available connector.

## Scope decision

The study uses the already relevant public repository `kodlbegiko/cff-drift-guard`. Public metadata acquisition runs in GitHub Actions; deterministic evaluation runs offline from committed records. Release creation is documented as an owner action rather than falsely claimed as complete.
