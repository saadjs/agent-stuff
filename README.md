# agent-stuff

Personal configs and scripts for coding agents.

## Contents

- `skills/` — Agent skills, each in `skills/<name>/SKILL.md`.
- `claude/statusline-command.sh` — Claude Code status line. Renders host, cwd, git branch/status, session name, model, context usage, and rate limits.

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

Requires `jq` on `PATH`.
