---
title: Publish GreenRay repository to GitHub
description: Create the private GitHub repository from this checkout and push main safely using GitHub CLI.
---

# /publish-github

1. Read `AGENTS.md`.
2. Verify the working tree contains no `.env`, secrets, database dumps, backups, or credentials.
3. Run `./scripts/validate.sh`.
4. Verify GitHub CLI exists with `gh --version` and is authenticated with `gh auth status`.
5. Set the intended repository to `greenray-erpnext` unless the user explicitly supplies another name.
6. If no remote repository exists, create a **private** repository under the authenticated account with:
   `gh repo create greenray-erpnext --private --source=. --remote=origin --push`
7. If `origin` already exists, verify its owner/name before pushing. Do not overwrite an unrelated remote.
8. Ensure the default branch is `main` and push it.
9. Report the GitHub repository URL and latest commit SHA.
