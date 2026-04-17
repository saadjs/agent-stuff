#!/usr/bin/env zsh
# Claude Code status line - based on sonicradish zsh theme

input=$(cat)
cwd=$(echo "$input" | jq -r '.workspace.current_dir // .cwd // empty')
model=$(echo "$input" | jq -r '.model.display_name // empty')
used=$(echo "$input" | jq -r 'if (.context_window.used_percentage | type) == "number" then .context_window.used_percentage else empty end')
remaining=$(echo "$input" | jq -r 'if (.context_window.remaining_percentage | type) == "number" then .context_window.remaining_percentage else empty end')
session_name=$(echo "$input" | jq -r '.session_name // empty')
output_style=$(echo "$input" | jq -r '.output_style.name // empty')
rate_5h=$(echo "$input" | jq -r 'if (.rate_limits.five_hour.used_percentage | type) == "number" then .rate_limits.five_hour.used_percentage else empty end')
rate_7d=$(echo "$input" | jq -r 'if (.rate_limits.seven_day.used_percentage | type) == "number" then .rate_limits.seven_day.used_percentage else empty end')

# ANSI color codes
RESET='\033[0m'
BOLD='\033[1m'
CYAN='\033[36m'
YELLOW='\033[33m'
GREEN='\033[32m'
RED='\033[31m'
MAGENTA='\033[35m'
BLUE='\033[34m'
ORANGE='\033[38;5;208m'
GRAY='\033[90m'
DIM='\033[2m'

# Hostname
host=$(hostname -s)

# Current dir basename
if [ -n "$cwd" ]; then
  dir=$(basename "$cwd")
else
  dir=$(basename "$(pwd)")
fi

# Git info (skip optional locks)
git_info=""
if git -C "${cwd:-$(pwd)}" rev-parse --git-dir > /dev/null 2>&1; then
  git_branch=$(git -C "${cwd:-$(pwd)}" symbolic-ref --short HEAD 2>/dev/null || git -C "${cwd:-$(pwd)}" rev-parse --short HEAD 2>/dev/null)
  if [ -n "$git_branch" ]; then
    if git -C "${cwd:-$(pwd)}" status --porcelain 2>/dev/null | grep -q .; then
      git_status_icon="${RED} ✘${RESET}"
    else
      git_status_icon="${GREEN} ✔${RESET}"
    fi
    git_info="${DIM}:${RESET} ${MAGENTA}${git_branch}${RESET}${git_status_icon} ${DIM}:${RESET}"
  fi
fi

# Context usage — gray
ctx_info=""
ctx_color="$GRAY"
if [ -n "$used" ]; then
  if [ -n "$remaining" ]; then
    ctx_info=" ${DIM}[${RESET}${ctx_color}${used}% used${RESET}${DIM} | ${RESET}${ctx_color}${remaining}% left${RESET}${DIM}]${RESET}"
  else
    ctx_info=" ${DIM}[${RESET}${ctx_color}${used}% used${RESET}${DIM}]${RESET}"
  fi
elif [ -n "$remaining" ]; then
  ctx_info=" ${DIM}[${RESET}${ctx_color}${remaining}% left${RESET}${DIM}]${RESET}"
fi

# Model info
model_info=""
if [ -n "$model" ]; then
  model_info=" ${DIM}[${RESET}${ORANGE}${model}${RESET}${DIM}]${RESET}"
fi

# Session name (only when set via /rename)
session_info=""
if [ -n "$session_name" ]; then
  session_info=" ${DIM}[${RESET}${YELLOW}${session_name}${RESET}${DIM}]${RESET}"
fi

# Output style (only when non-default)
style_info=""
if [ -n "$output_style" ] && [ "$output_style" != "default" ]; then
  style_info=" ${DIM}[style: ${output_style}]${RESET}"
fi

# Rate limits (subscription usage — only shown when available)
rate_info=""
rate_parts=""
if [ -n "$rate_5h" ]; then
  pct=$(printf '%.0f' "$rate_5h")
  if [ "$pct" -ge 80 ]; then
    rate_color="$RED"
  elif [ "$pct" -ge 50 ]; then
    rate_color="$YELLOW"
  else
    rate_color="$GREEN"
  fi
  rate_parts="${rate_color}5h:${pct}%${RESET}"
fi
if [ -n "$rate_7d" ]; then
  pct7=$(printf '%.0f' "$rate_7d")
  if [ "$pct7" -ge 80 ]; then
    rate_color7="$RED"
  elif [ "$pct7" -ge 50 ]; then
    rate_color7="$YELLOW"
  else
    rate_color7="$GREEN"
  fi
  if [ -n "$rate_parts" ]; then
    rate_parts="${rate_parts}${DIM} | ${RESET}${rate_color7}7d:${pct7}%${RESET}"
  else
    rate_parts="${rate_color7}7d:${pct7}%${RESET}"
  fi
fi
if [ -n "$rate_parts" ]; then
  rate_info=" ${DIM}[${RESET}${rate_parts}${DIM}]${RESET}"
fi

printf '%b' "${BOLD}${CYAN}${host}${RESET}  ${YELLOW}${dir}${RESET} ${git_info}${session_info}${model_info}${ctx_info}${rate_info}${style_info}"
