---
name: continue-claude-session
description: Resume work from a local Claude Code session transcript.
disable-model-invocation: true
---

# Continue Claude Session

1. Locate the session. Run from the target project directory:

   ```bash
   python3 <skill>/scripts/read_session.py                 # newest current-project session
   python3 <skill>/scripts/read_session.py <session-id>    # exact ID across projects
   python3 <skill>/scripts/read_session.py --match "title"  # title or first user message
   python3 <skill>/scripts/read_session.py --list
   ```

   Use `--cwd PATH` for a named project; `--all-dirs` only when requested. Report missing matches.

2. Read the complete compact transcript. If truncated, save to a temporary file and read in chunks. Expand relevant evidence using `--search "text"`, `--lines START:END`, or `--tool CALL_ID` with the selected session. See `--help` for other options.

3. Verify the recorded worktree, branch, edits, and test results against current state. A command starting does not establish success.

4. Before editing, report the goal, each task’s status (`✅ DONE`, `🟡 PARTIALLY DONE` with missing work, `❌ NOT DONE`), and the next action.

5. Resume the unfinished step, preserving decisions and existing edits. Ask when ambiguity blocks continuation.
