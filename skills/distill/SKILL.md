---
name: distill
description: Save durable session lessons where future agents will read them.
disable-model-invocation: true
---

# Distill session learnings

1. List candidate lessons from this session: corrections the user made, conventions discovered the hard way, commands/setup that were not obvious, constraints stated in prose. One line each.

2. Drop any candidate that is:
   - already in the target file
   - discoverable from code, tests, git history, or an existing pattern
   - enforceable by a linter, formatter, or hook
   - true only for current task/session

3. Route each survivor:
   - repo-specific → project `CLAUDE.md`, or `AGENTS.md` if that is what the repo uses (follow symlinks; edit the real file)
   - cross-project preference or workflow → `~/.claude/CLAUDE.md` (or the matching global `AGENTS.md`)

4. Show the routed list and wait for the user to confirm before writing.

5. Read the target file. Add each item as its own `<important if="<specific trigger>">` block; extend an existing block only when the trigger already matches exactly.

6. Report `git diff --stat` for project files and the exact paths of global files changed.

Done: every kept lesson lives in one file under a specific trigger; nothing existing was deleted without saying so.
