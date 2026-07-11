---
name: continue-codex-session
description: Reconstruct and continue work from a local Codex CLI session transcript.
disable-model-invocation: true
---

# Continue Codex Session

Pick up where a Codex CLI session left off. Codex stores each session as a raw
JSONL rollout under `~/.codex/sessions/YYYY/MM/DD/rollout-<ts>-<uuid>.jsonl` —
hundreds of records per session, too large to read verbatim. Use the bundled
script to distill one into a readable transcript, then continue the work.

## Locate and read the session

By default the skill resumes the session that belongs to **the current directory**
it was invoked from — not the globally newest session. Invoke the script by path
so the current directory stays the target repo; do not `cd` into any folder.

```bash
python3 <skill>/scripts/read_session.py            # newest session for the current directory
python3 <skill>/scripts/read_session.py --match "<goal or title words>"
python3 <skill>/scripts/read_session.py --list     # browse this directory's sessions
python3 <skill>/scripts/read_session.py --verbose  # include reasoning traces
```

There is no stored session title — `--match` finds the newest current-directory
session whose first user message contains the given words. Match on a session the
user names; otherwise take the most recent. The script folds each
tool call to one line; add `--verbose` only when the narrative alone leaves the
stopping point ambiguous. Read the whole distilled transcript before acting.

If no session matches the current directory, the script says so — surface that
instead of silently widening the search. Only reach elsewhere (`--all-dirs`,
`--cwd PATH`) when the user explicitly asks.

## Checkpoint before continuing

Before editing anything, surface a checkpoint to the user:

- **Goal** — one-line summary of what the session was doing.
- **Task status** — every TODO, checklist item, and implicit task, each classified as:
  - `DONE`
  - `PARTIALLY DONE` — and what's missing
  - `NOT DONE`
- **Next action** — the exact unfinished step to resume from.

## Continue

Resume from the last unfinished step. Follow the approach, style, and decisions
already established in the transcript; open the files it touched rather than
re-deriving context. Don't repeat completed work.
