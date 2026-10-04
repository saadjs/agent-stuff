# agent-stuff

Personal configs, scripts, and skills for coding agents.

## Contents

- `skills/` - Agent skills, each in `skills/<name>/SKILL.md`.
- `claude/statusline-command.sh` - Claude Code status line. Renders host, cwd, git branch/status, worktree and PR info, session name, model/effort, context usage, prompt cache state and TTL, rate limits with reset times, session cost, and output style.
- `pi/keybindings.json` - Pi keybindings.

## Installing Skills

```sh
# Pick skills and agents interactively
npx skills add saadjs/agent-stuff

# List available skills
npx skills add saadjs/agent-stuff --list

# Install specific skills globally for Claude Code
npx skills add saadjs/agent-stuff --skill distill --skill create-skill -a claude-code -g
```

## Using the Claude Code status line

Copy the script somewhere stable and point `settings.json` at it:

```json
{
  "statusLine": {
    "type": "command",
    "command": "zsh /path/to/statusline-command.sh"
  }
}
```

Requires `zsh` and `jq` on `PATH`.

Each render also saves its input to `$TMPDIR/claude-statusline/<session_id>.json`. The `remote-status` skill re-renders that snapshot as plain text, so `/remote-status` shows the same info in Remote Control sessions and the Claude mobile app. It expects the script at `~/.claude/statusline-command.sh` (override with `STATUSLINE_SCRIPT`).
