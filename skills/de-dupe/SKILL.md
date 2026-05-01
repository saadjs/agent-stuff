---
name: de-dupe
description: Remove duplicated code and tech debt by keeping code DRY. Use when asked to de-duplicate logic, extract shared utilities, or refactor repeated patterns ("keep code DRY", "remove duplicated code", "extract common functions", "reduce tech debt"). Include checks for uncommitted changes before refactors.
---

# De-dupe and DRY Refactor

Follow a safe, repeatable workflow to find duplicated code, extract shared helpers, and reduce maintenance burden while preserving behavior.

## Workflow

1. Check for uncommitted changes before refactor.
   - Run `git status -sb` and note touched files.
   - If the tree is dirty, prefer working incrementally and avoid mixing unrelated changes.

2. Identify duplication targets.
   - Scan for obvious repeats in the touched files.
   - Use `rg` to find similar blocks or repeated strings.

3. Decide if extraction is warranted.
   - Extract when logic is repeated 2+ times and the abstraction is stable.
   - Do not extract when it makes call sites harder to read or behavior diverges.

4. Extract shared utilities.
   - Create a small function with a focused signature.
   - Place in an existing shared module or create a new `utils`/`shared` file.

5. Replace duplicates and remove redundant code.

6. Verify behavior — run relevant tests or linters if available.

## Heuristics

- Extract constants for repeated literals (strings, regexes, numbers).
- If duplication is across layers, move logic to the lowest shared layer.
- Prefer simple helpers over deep class refactors.

## Guardrails

- Avoid introducing new dependencies for small refactors.
- Do not change public APIs unless explicitly requested.
- Keep the diff small and focused; do not mix refactors with unrelated changes.
