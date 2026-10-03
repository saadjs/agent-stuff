#!/usr/bin/env zsh
# Claude Code status line - based on sonicradish zsh theme

input=$(cat)
eval "$(echo "$input" | jq -r '
  def num: if type == "number" then . else "" end;
  def flag: if . == true then "true" else "" end;
  @sh "cwd=\(.workspace.current_dir // .cwd // "")
model=\(.model.display_name // "")
used=\(.context_window.used_percentage | num)
remaining=\(.context_window.remaining_percentage | num)
ctx_total=\(.context_window.context_window_size // "")
ctx_input_tokens=\(.context_window.total_input_tokens // "")
session_name=\(.session_name // "")
output_style=\(.output_style.name // "")
rate_5h=\(.rate_limits.five_hour.used_percentage | num)
rate_7d=\(.rate_limits.seven_day.used_percentage | num)
rate_5h_reset=\(.rate_limits.five_hour.resets_at // "")
rate_7d_reset=\(.rate_limits.seven_day.resets_at // "")
effort_level=\(.effort.level // "")
thinking_enabled=\(.thinking.enabled | flag)
cache_observed=\(.prompt_cache.caching_observed | flag)
cache_warm=\(.prompt_cache.warm | flag)
cache_hit_ratio=\(.prompt_cache.hit_ratio | num)
cache_miss_cause=\(.prompt_cache.last_miss_cause.causes[0] // "")
cache_expires_at=\(.prompt_cache.expires_at // "")
worktree_name=\(.worktree.name // "")
worktree_branch=\(.worktree.branch // "")
pr_number=\(.pr.number // "")
pr_kind=\(.pr.kind // "")
pr_review_state=\(.pr.review_state // "")
repo_owner=\(.workspace.repo.owner // "")
repo_name=\(.workspace.repo.name // "")
added_dirs=\((.workspace.added_dirs // []) | map(split("/") | last) | join(", "))
cost_usd=\(.cost.total_cost_usd // "")
duration_ms=\(.cost.total_duration_ms // "")
claude_lines_added=\(.cost.total_lines_added // 0)
claude_lines_removed=\(.cost.total_lines_removed // 0)"
')"

# Seconds to a compact duration: 42m, 1h20m, 2d14h
fmt_duration() {
  local s=$1
  if [ "$s" -lt 3600 ]; then
    echo "$(( s / 60 ))m"
  elif [ "$s" -lt 86400 ]; then
    echo "$(( s / 3600 ))h$(( s % 3600 / 60 ))m"
  else
    echo "$(( s / 86400 ))d$(( s % 86400 / 3600 ))h"
  fi
}

# ANSI color codes
RESET='\033[0m'
BOLD='\033[1m'
CYAN='\033[36m'
YELLOW='\033[33m'
GREEN='\033[32m'
RED='\033[31m'
MAGENTA='\033[35m'
ORANGE='\033[38;5;208m'
GRAY='\033[90m'
DIM='\033[2m'

# Current dir basename
if [ -n "$cwd" ]; then
  dir=$(basename "$cwd")
else
  dir=$(basename "$(pwd)")
fi

# Git info (skip optional locks) — shown on line 2
git_info=""
export GIT_OPTIONAL_LOCKS=0
git_status_v2=$(git -C "${cwd:-$(pwd)}" status --porcelain=v2 --branch --show-stash 2>/dev/null)
if [ -n "$git_status_v2" ]; then
  read -r git_branch git_dirty git_ahead git_behind git_stashes git_staged git_modified git_untracked <<< "$(printf '%s\n' "$git_status_v2" | awk '
    /^# branch.oid / { oid = substr($3, 1, 7) }
    /^# branch.head / { head = $3 }
    /^# branch.ab / { ahead = substr($3, 2); behind = substr($4, 2) }
    /^# stash / { stash = $3 }
    /^[12u?] / { dirty = 1 }
    /^[12] / { if (substr($2, 1, 1) != ".") staged++; if (substr($2, 2, 1) ~ /[MDT]/) modified++ }
    /^\? / { untracked++ }
    END { if (head == "(detached)") head = oid; print head, dirty + 0, ahead + 0, behind + 0, stash + 0, staged + 0, modified + 0, untracked + 0 }')"
  if [ -n "$git_branch" ]; then
    if [ "$git_dirty" -eq 1 ]; then
      git_status_icon="${RED} ✘${RESET}"
    else
      git_status_icon="${GREEN} ✔${RESET}"
    fi
    read -r git_added git_removed <<< "$(git -C "${cwd:-$(pwd)}" diff HEAD --numstat 2>/dev/null | awk '{a+=$1; r+=$2} END {print a+0, r+0}')"
    git_last_commit=$(git -C "${cwd:-$(pwd)}" log -1 --format=%ct 2>/dev/null)

    git_sync=""
    [ "$git_ahead" -gt 0 ] && git_sync="${GREEN}↑${git_ahead}${RESET}"
    [ "$git_behind" -gt 0 ] && git_sync="${git_sync:+${git_sync} }${RED}↓${git_behind}${RESET}"

    git_stats=""
    [ "$git_staged" -gt 0 ] && git_stats="${GREEN}${git_staged} staged${RESET}"
    [ "$git_modified" -gt 0 ] && git_stats="${git_stats:+${git_stats}${DIM} • ${RESET}}${YELLOW}${git_modified} modified${RESET}"
    [ "$git_untracked" -gt 0 ] && git_stats="${git_stats:+${git_stats}${DIM} • ${RESET}}${GRAY}${git_untracked} untracked${RESET}"
    if [ "$git_added" -gt 0 ] || [ "$git_removed" -gt 0 ]; then
      git_stats="${git_stats:+${git_stats}${DIM} • ${RESET}}${GREEN}+${git_added}${RESET} ${RED}−${git_removed}${RESET}"
    fi
    [ "$git_stashes" -gt 0 ] && git_stats="${git_stats:+${git_stats}${DIM} • ${RESET}}${CYAN}⚑${git_stashes}${RESET}"
    if [ -n "$git_last_commit" ]; then
      age=$(( $(date +%s) - git_last_commit ))
      if [ "$age" -lt 3600 ]; then
        age_label="$(( age / 60 ))m"
      elif [ "$age" -lt 86400 ]; then
        age_label="$(( age / 3600 ))h"
      else
        age_label="$(( age / 86400 ))d"
      fi
      git_stats="${git_stats:+${git_stats}${DIM} • ${RESET}}${GRAY}${age_label}${RESET}"
    fi
    git_info="${MAGENTA}${git_branch}${RESET}${git_status_icon}${git_sync:+ ${git_sync}}${git_stats:+ ${git_stats}}"
  fi
fi

# Context usage — gray
ctx_info=""
ctx_color="$GRAY"
if [ -n "$used" ] || [ -n "$remaining" ]; then
  # Format token counts with k suffix
  tok_used=""
  tok_remaining=""
  if [ -n "$ctx_input_tokens" ] && [ -n "$ctx_total" ]; then
    tok_used=$(awk "BEGIN {printf \"%.1fk\", $ctx_input_tokens/1000}")
    tok_rem_raw=$(( ctx_total - ctx_input_tokens ))
    tok_remaining=$(awk "BEGIN {printf \"%.1fk\", $tok_rem_raw/1000}")
  fi

  used_part=""
  remaining_part=""
  if [ -n "$used" ]; then
    if [ -n "$tok_used" ]; then
      used_part="${ctx_color}${tok_used} (${used}%) used${RESET}"
    else
      used_part="${ctx_color}${used}% used${RESET}"
    fi
  fi
  if [ -n "$remaining" ]; then
    if [ -n "$tok_remaining" ]; then
      remaining_part="${ctx_color}${tok_remaining} (${remaining}%) left${RESET}"
    else
      remaining_part="${ctx_color}${remaining}% left${RESET}"
    fi
  fi

  if [ -n "$used_part" ] && [ -n "$remaining_part" ]; then
    ctx_info=" ${DIM}[${RESET}${used_part}${DIM} | ${RESET}${remaining_part}${DIM}]${RESET}"
  elif [ -n "$used_part" ]; then
    ctx_info=" ${DIM}[${RESET}${used_part}${DIM}]${RESET}"
  elif [ -n "$remaining_part" ]; then
    ctx_info=" ${DIM}[${RESET}${remaining_part}${DIM}]${RESET}"
  fi
fi

# Effort / thinking — folded into the model bracket
effort_part=""
if [ -n "$effort_level" ]; then
  case "$effort_level" in
    low)    effort_color="$GRAY" ;;
    medium) effort_color="$YELLOW" ;;
    high)   effort_color="$ORANGE" ;;
    xhigh)  effort_color="$RED" ;;
    max)    effort_color="${BOLD}${RED}" ;;
    *)      effort_color="$GRAY" ;;
  esac
  effort_part="${effort_color}${effort_level}${RESET}"
elif [ "$thinking_enabled" = "true" ]; then
  effort_part="${CYAN}thinking${RESET}"
fi

# Model info — [model | effort]
model_info=""
if [ -n "$model" ]; then
  if [ -n "$effort_part" ]; then
    model_info=" ${DIM}[${RESET}${ORANGE}${model}${RESET}${DIM} | ${RESET}${effort_part}${DIM}]${RESET}"
  else
    model_info=" ${DIM}[${RESET}${ORANGE}${model}${RESET}${DIM}]${RESET}"
  fi
fi

# Output style (only when non-default)
style_info=""
if [ -n "$output_style" ] && [ "$output_style" != "default" ]; then
  style_info=" ${DIM}[style: ${output_style}]${RESET}"
fi

# Session name (only when set via /rename)
session_info=""
if [ -n "$session_name" ]; then
  session_info=" ${DIM}[${RESET}${YELLOW}${session_name}${RESET}${DIM}]${RESET}"
fi

# Rate limits (subscription usage — only shown when available)
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
  [ -n "$rate_5h_reset" ] && [ "$rate_5h_reset" -gt "$(date +%s)" ] && rate_parts="${rate_parts} ${GRAY}↻$(fmt_duration $(( rate_5h_reset - $(date +%s) )))${RESET}"
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
  [ -n "$rate_7d_reset" ] && [ "$rate_7d_reset" -gt "$(date +%s)" ] && rate_parts="${rate_parts} ${GRAY}↻$(fmt_duration $(( rate_7d_reset - $(date +%s) )))${RESET}"
fi

# Session cost and wall-clock length
session_cost_info=""
if [ -n "$cost_usd" ]; then
  session_cost_info="${GREEN}\$$(printf '%.2f' "$cost_usd")${RESET}"
fi
if [ -n "$duration_ms" ]; then
  session_cost_info="${session_cost_info:+${session_cost_info}${DIM} • ${RESET}}${GRAY}$(fmt_duration $(( duration_ms / 1000 )))${RESET}"
fi

# Prompt cache health — warm/cold, hit ratio, likely miss cause
cache_info=""
cache_ttl=""
if [ "$cache_warm" = "true" ] && [ -n "$cache_expires_at" ] && [ "$cache_expires_at" -gt "$(date +%s)" ]; then
  cache_ttl="${DIM} ${RESET}${GRAY}⏳$(fmt_duration $(( cache_expires_at - $(date +%s) )))${RESET}"
fi
if [ "$cache_observed" = "true" ]; then
  if [ "$cache_warm" = "true" ]; then
    cache_state="${GREEN}warm${RESET}"
  else
    if [ -n "$cache_miss_cause" ]; then
      cache_state="${RED}cold:${cache_miss_cause}${RESET}"
    else
      cache_state="${RED}cold${RESET}"
    fi
  fi
  if [ -n "$cache_hit_ratio" ]; then
    hit_pct=$(awk "BEGIN {printf \"%.0f\", $cache_hit_ratio*100}")
    cache_info=" ${DIM}[${RESET}cache:${cache_state}${DIM} ${RESET}${GRAY}${hit_pct}%${RESET}${cache_ttl}${DIM}]${RESET}"
  else
    cache_info=" ${DIM}[${RESET}cache:${cache_state}${cache_ttl}${DIM}]${RESET}"
  fi
fi

# Worktree (name/branch, only when present)
worktree_info=""
if [ -n "$worktree_name" ]; then
  if [ -n "$worktree_branch" ]; then
    worktree_info="${CYAN}worktree:${worktree_name}${RESET}${DIM}@${RESET}${worktree_branch}"
  else
    worktree_info="${CYAN}worktree:${worktree_name}${RESET}"
  fi
fi

# PR / MR state (only when present)
pr_info=""
if [ -n "$pr_number" ]; then
  if [ "$pr_kind" = "mr" ]; then
    pr_label="!${pr_number}"
  else
    pr_label="#${pr_number}"
  fi
  if [ -n "$pr_review_state" ]; then
    case "$pr_review_state" in
      approved)          pr_color="$GREEN" ;;
      changes_requested)  pr_color="$RED" ;;
      draft)              pr_color="$GRAY" ;;
      pending)             pr_color="$YELLOW" ;;
      *)                  pr_color="$GRAY" ;;
    esac
    pr_info="${pr_color}${pr_label} ${pr_review_state}${RESET}"
  else
    pr_info="${GRAY}${pr_label}${RESET}"
  fi
fi

# Repo owner/name (only when present)
repo_info=""
if [ -n "$repo_owner" ] && [ -n "$repo_name" ]; then
  repo_info="${GRAY}${repo_owner}/${repo_name}${RESET}"
fi

# Added dirs (only when non-empty)
added_dirs_info=""
if [ -n "$added_dirs" ]; then
  added_dirs_info="${DIM}+dirs:${RESET} ${added_dirs}"
fi

# Lines Claude added/removed this session
claude_lines_info=""
if [ "$claude_lines_added" -gt 0 ] || [ "$claude_lines_removed" -gt 0 ]; then
  claude_lines_info="${CYAN}✎${RESET} ${GREEN}+${claude_lines_added}${RESET} ${RED}−${claude_lines_removed}${RESET}"
fi

# Assemble line 2 from non-empty parts, joined by a dim separator
line2=""
for part in "$repo_info" "$worktree_info" "$pr_info" "$git_info" "$claude_lines_info" "$added_dirs_info"; do
  if [ -n "$part" ]; then
    if [ -n "$line2" ]; then
      line2="${line2}${DIM} | ${RESET}${part}"
    else
      line2="${part}"
    fi
  fi
done

line1="${BOLD}${YELLOW}${dir}${RESET}${model_info}${ctx_info}${cache_info}${style_info}${session_info}"

line3=""
for part in "$rate_parts" "$session_cost_info"; do
  if [ -n "$part" ]; then
    if [ -n "$line3" ]; then
      line3="${line3}${DIM} | ${RESET}${part}"
    else
      line3="${part}"
    fi
  fi
done

output="$line1"
[ -n "$line2" ] && output="${output}\n${line2}"
[ -n "$line3" ] && output="${output}\n${line3}"
printf '%b' "$output"
