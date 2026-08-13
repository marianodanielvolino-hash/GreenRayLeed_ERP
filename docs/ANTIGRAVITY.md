# Using this repository with Google Antigravity

Antigravity agents work inside Projects that can include Git repositories. Open this repository as a Project folder.

The repository includes:

- `AGENTS.md`: codebase-wide engineering instructions.
- `.agents/rules/greenray-architecture.md`: persistent GreenRay architecture rules.
- `.agents/workflows/deploy-greenray.md`: `/deploy-greenray` deployment workflow.

Recommended first task:

> Read AGENTS.md and docs/DEPLOYMENT.md. Validate the repository, inspect the fch_ops custom app, and run /deploy-greenray in a local or UAT environment. Do not alter ERPNext core and do not invent fiscal or opening-balance data.

For risky changes use an isolated Git worktree/project mode and keep deployment credentials outside Git.

## Publishing to GitHub from Antigravity

If the repository has not yet been created remotely, run `/publish-github`. The workflow uses authenticated GitHub CLI, validates the codebase, performs a secrets safety check and creates `greenray-erpnext` as a private repository before pushing `main`.
