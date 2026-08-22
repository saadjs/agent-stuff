#!/usr/bin/env bash
# Poll the booted simulator for screenshots, keeping only frames that differ from every frame seen so far.
set -euo pipefail

OUT_DIR=${1:?usage: capture_loop.sh <out-dir> [interval-sec] [duration-sec] [prefix]}
INTERVAL=${2:-1.5}
DURATION=${3:-120}
PREFIX=${4:-f}

mkdir -p "$OUT_DIR"
tmp="$OUT_DIR/.tmp.png"
seen_file="$OUT_DIR/.hashes"
: >"$seen_file"

n=0
end=$(python3 -c "import time,sys; print(time.time()+float(sys.argv[1]))" "$DURATION")
while python3 -c "import time,sys; sys.exit(0 if time.time()<float(sys.argv[1]) else 1)" "$end"; do
  if xcrun simctl io booted screenshot "$tmp" >/dev/null 2>&1; then
    h=$(md5 -q "$tmp")
    if ! grep -qx "$h" "$seen_file"; then
      echo "$h" >>"$seen_file"
      n=$((n + 1))
      mv "$tmp" "$(printf '%s/%s%02d.png' "$OUT_DIR" "$PREFIX" "$n")"
      echo "captured $PREFIX$n"
    fi
  fi
  sleep "$INTERVAL"
done
rm -f "$tmp"
echo "done: $n unique frames in $OUT_DIR"
