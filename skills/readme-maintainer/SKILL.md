---
name: readme-maintainer
description: Create or update project README.md files by scanning the repository and keeping documentation in sync with the current setup. Use when a README is missing, outdated, or needs updates based on package configs, build/test scripts, env examples, licenses, or changelog files. Include install/usage/env vars/testing/contributing/license/changelog sections only when the repo contains evidence for them.
---

# README Maintainer

## Goal

Create or update `README.md` so it accurately reflects the current project setup. Only include information you can verify from the repository. Ask brief questions if critical information is missing.

## Workflow

1. Scan the repository for sources of truth: package manifests (`package.json`, `pyproject.toml`, `go.mod`, `Cargo.toml`, etc.), lockfiles, build/test scripts (`Makefile`, CI workflows), containers (`Dockerfile`), env samples (`.env.example`), `CONTRIBUTING.md`, `LICENSE`, and `CHANGELOG.md`.

2. Decide what to include. If a section has no evidence, omit it. Preserve existing sections, tone, and badges unless incorrect.

3. Build or update sections using verified data.
   - **Install**: infer package manager from lockfiles (`pnpm-lock.yaml` → `pnpm install`, etc.).
   - **Usage**: derive from package scripts, CLI entry points, or Makefile targets.
   - **Env vars**: list keys from `.env.example`. Add descriptions only if present in comments.
   - **Testing**: use scripts or standard commands (`pytest`, `go test`) only if clearly used in the repo.
   - **Contributing**: link to `CONTRIBUTING.md` if present; otherwise omit.
   - **License**: link to the license file and name it only if the file states the name.
   - **Changelog**: link to `CHANGELOG.md` if present.

4. Validate: ensure commands match actual scripts, remove outdated instructions, keep it concise.

## Output

Update or create `README.md` only. If questions are needed, ask before writing major sections.
