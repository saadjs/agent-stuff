---
name: continue-claude-session
description: Continue work from a local Claude Code session transcript. Use when the user asks to resume, continue, reconstruct, or pick up a Claude Code session, optionally with a session id or session title, before Codex takes further action.
---

# Continue Claude Session

## Inputs

- Accept an optional Claude session id, session title, or project name from the user prompt.
- If omitted, infer the project from the current workspace and use the most recent matching Claude transcript.

## Locate Transcript

1. Look under `~/.claude/projects/-Users-saad-<project-name>`.
2. If a session id or title is provided, find the matching transcript.
3. Otherwise, find the most recent transcript for the inferred project.
4. Read the full transcript before editing files, running tests, or continuing implementation.

## Reconstruct Context

- Summarize the session goal.
- Identify completed tasks.
- Determine the exact stopping point.
- Extract explicit TODO lists, checklists, and implicit unfinished tasks.
- Classify each task as:
  - `DONE`
  - `PARTIALLY DONE` with the missing part
  - `NOT DONE`

## Continue Work

- Resume from the last unfinished step.
- Avoid repeating completed work.
- Prefer continuing existing edits over restarting the solution.
- Follow the established approach, style, decisions, and constraints from the transcript.
- Inspect related files when transcript context is missing or ambiguous.
- Ask questions only when progress is blocked.

## Output

- Brief context summary.
- Task status breakdown.
- Clear next action.
- Continue execution immediately.
