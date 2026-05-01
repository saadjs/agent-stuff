---
name: commit
description: Organize uncommitted changes into atomic Git commits using Conventional Commits. Use before opening a PR or merging to produce a clean, reviewable history where each commit represents one logical change.
---

# Git Atomic Commits

Transform all uncommitted changes into **atomic** Conventional Commits. Stop only when `git status` is clean.

## Workflow

1. Check status: `git status -sb`. Stop if clean.

2. Confirm branch: `git branch --show-current`. If detached HEAD, ask the user to create a branch.

3. **Branch safety gate** — if on `main` or `master`, do not commit. Ask the user to create a working branch first, then re-check status.

4. Inspect scope: `git diff --stat` and `git diff` as needed.

5. Identify atomic units (one purpose each):
   - dependencies, config/build/CI, refactor, bug fix, feature slice, tests, docs, formatting

6. Stage only what belongs to one atomic unit. Prefer `git add -p` for mixed files.

7. Commit with a Conventional Commits message.

8. After each commit, run `git status -sb`. Repeat until clean.

## Conventional Commit Rules

- Format: `type(scope): subject` or `type: subject`
- Subject: short, imperative, specific
- Types: `feat`, `fix`, `chore`, `refactor`, `docs`, `test`, `build`, `ci`, `style`
- Examples:
  - `feat(auth): add OAuth login`
  - `fix(api): handle timeout errors`
  - `build(deps): bump react to 19.0.0`
  - `style: format codebase`

## Safety Checks

- Do not mix unrelated changes in one commit.
- If a file mixes unrelated edits and hunk-splitting is ambiguous, ask before proceeding.
- Avoid committing build artifacts (`dist/`, `build/`, `coverage/`) unless the repo intentionally tracks them.
- Ensure deletions and renames are included when relevant.
