# agent-stuff

Personal configs, prompts, scripts, and skills for coding agents.

## Contents

- `skills/` — Agent skills, each in `skills/<name>/SKILL.md`.
- `claude/settings.json` — Claude Code settings.
- `claude/statusline-command.sh` — Claude Code status line. Renders host, cwd, git branch/status, session name, model/effort, context usage, rate limits, and output style.
- `pi/keybindings.json` — Pi keybindings.

## Installing Skills

```sh
skillctl add saadjs/agent-stuff --tool agents --scope global
skillctl add saadjs/agent-stuff --tool codex --scope global
skillctl add saadjs/agent-stuff --tool claude --scope project
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
