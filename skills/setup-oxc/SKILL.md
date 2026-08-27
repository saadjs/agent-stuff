---
name: setup-oxc
description: Set up Oxlint, Oxfmt, Husky hooks; optional anti-slop.
disable-model-invocation: true
---

# Setup Oxc

Default: Oxlint + Oxfmt + Husky. Anti-slop only when explicitly requested; then read [ANTI-SLOP.md](ANTI-SLOP.md).

1. Inspect instructions, `git status`, package manager, scripts, configs, hooks, CI. Preserve existing work/behavior. Find full test command; ask if unclear.

2. Install latest `oxlint`, `oxfmt`, `husky` as dev dependencies. Merge equivalent scripts; keep project paths/flags:

```json
{
  "lint": "oxlint .",
  "format": "oxfmt --write .",
  "format:check": "oxfmt --check ."
}
```

Keep configs. Generate none unless needed.

3. Initialize Husky using current package-manager command. Preserve existing `prepare` and hooks. Add executable hooks using detected runner:

```sh
# .husky/pre-commit
<runner> run lint
<runner> run format:check
```

```sh
# .husky/pre-push
<full-test-command>
```

Format-check only in hook; avoid unstaged rewrites.

4. If requested, add anti-slop. Run lint, format-check, tests. Review diff. Report changes, commands, failures.

Done: dependencies/scripts present; commit checks lint+format; push runs full tests; existing behavior retained; failures reported.
