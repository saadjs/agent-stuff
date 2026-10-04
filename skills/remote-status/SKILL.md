---
name: remote-status
description: Show the Claude Code status line (model, context, cache, git, rate limits, cost) as plain text, for remote sessions and the mobile app where the terminal status line is not visible.
disable-model-invocation: true
allowed-tools: Bash(zsh:*)
---

!`zsh "${CLAUDE_SKILL_DIR}/scripts/show.sh" "${CLAUDE_SESSION_ID}"`

Reply with the output above inside a plain code block, unchanged, and nothing else.
