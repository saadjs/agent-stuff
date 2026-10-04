#!/usr/bin/env zsh
# Re-render the last status line snapshot for a session as plain text

session_id=$1
statusline=${STATUSLINE_SCRIPT:-$HOME/.claude/statusline-command.sh}
snapshot_dir="${TMPDIR:-/tmp}/claude-statusline"

snapshot="$snapshot_dir/$session_id.json"
if [ -z "$session_id" ] || [ ! -f "$snapshot" ]; then
  snapshot=$(ls -t "$snapshot_dir"/*.json 2>/dev/null | head -1)
  [ -n "$snapshot" ] && echo "(no snapshot for this session, showing latest)"
fi

if [ -z "$snapshot" ]; then
  echo "No status line snapshot yet. It is written each time the terminal status line renders."
  exit 0
fi

age=$(( $(date +%s) - $(stat -f %m "$snapshot") ))
STATUSLINE_PLAIN=1 zsh "$statusline" < "$snapshot"
printf '\nsnapshot %ss old\n' "$age"
