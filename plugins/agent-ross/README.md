# Agent Ross Plugin

> Release Manager agent — CI/CD, Docker, cloud deploy, and release tagging.

Named after Bob Ross — calm and methodical, "happy little deployments."

Agent Ross is the release manager of the development team. Ross owns the full release
lifecycle from commit messages through deployment. This plugin absorbs the former
`git-committer` plugin and adds CI/CD, Docker, cloud deploy, and release tagging.

**This role is optional** — if not installed, agent-smith handles basic git merge only.

## Installation

Install via the wisdom marketplace:

```bash
/plugin install agent-ross
```

## Role in the Team

| Agent             | Role           | Ross's Relationship                   |
| ----------------- | -------------- | ------------------------------------- |
| **agent-smith**   | Project Leader | Assigns release and commit tasks      |
| **agent-page**    | SRE            | Provides ops verdict before release   |
| **changelog-gen** | Support Tool   | Generates changelogs from git history |
| **test-runner**   | Support Tool   | Runs pre-release test verification    |

## How It Works

1. **Commit** — Generates conventional commit messages (replaces git-committer)
2. **Pre-Release** — Verifies tests, CI status, clean branch
3. **Tag** — Semantic versioning, changelog generation
4. **Deploy** — Docker build, K8s apply, Terraform, cloud platforms
5. **Verify** — Post-deploy health checks, smoke tests

## Supported Environments

- Docker / Docker Compose
- Kubernetes
- Terraform
- AWS / GCP / Azure
- GitHub Releases

## Usage

### Magic Words

- `release it` → Ross runs the full release pipeline
- `deploy it` → Ross deploys to target environment
- `commit it` → Ross generates a commit message (replaces git-committer)
- `ross` → Direct invocation

## License

MIT
