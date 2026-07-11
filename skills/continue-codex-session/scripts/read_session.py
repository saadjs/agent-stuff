#!/usr/bin/env python3
"""Distill a Codex CLI session (~/.codex/sessions/**/rollout-*.jsonl) into a
readable transcript. Raw rollout files are huge (hundreds of response_items);
this folds them to the narrative plus one-line tool calls so the session can be
reconstructed without blowing context.

By default only sessions whose Codex `cwd` matches the current working directory
are considered, so the skill resumes the session belonging to the repo it was
invoked from. Do not `cd` into the skill directory before running it — invoke it
by path so the current directory stays the target repo.

Usage:
  read_session.py                 # newest session for the current directory
  read_session.py --match "goal"  # newest current-dir session whose first user message matches
  read_session.py --cwd PATH      # target a different directory
  read_session.py --all-dirs      # consider sessions from every directory
  read_session.py --file PATH     # a specific rollout file
  read_session.py --list          # list recent sessions (date, cwd, first message)
  read_session.py --verbose       # also include agent reasoning traces
"""
import argparse, glob, json, os, sys

ROOT = os.path.expanduser("~/.codex/sessions")


def sessions_newest_first():
    files = glob.glob(os.path.join(ROOT, "**", "rollout-*.jsonl"), recursive=True)
    return sorted(files, key=os.path.getmtime, reverse=True)


def records(path):
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            try:
                yield json.loads(line)
            except json.JSONDecodeError:
                continue


def meta_and_first_user(path):
    """Return (cwd, start_ts, first_user_message) reading only until found."""
    cwd = start = first = None
    for o in records(path):
        p = o.get("payload") or {}
        if o.get("type") == "session_meta" and cwd is None:
            cwd, start = p.get("cwd"), p.get("timestamp")
        if o.get("type") == "event_msg" and p.get("type") == "user_message" and first is None:
            first = (p.get("message") or "").strip()
        if cwd and first:
            break
    return cwd, start, first


def sessions_for(target_cwd, all_dirs):
    """Newest-first sessions, filtered to target_cwd unless all_dirs is set."""
    out = []
    for f in sessions_newest_first():
        cwd, _, first = meta_and_first_user(f)
        if all_dirs or (cwd and os.path.realpath(cwd) == target_cwd):
            out.append((f, first))
    return out


def locate(args):
    if args.file:
        return os.path.expanduser(args.file)
    target = os.path.realpath(os.path.expanduser(args.cwd) if args.cwd else os.getcwd())
    files = sessions_for(target, args.all_dirs)
    if not files:
        where = "any directory" if args.all_dirs else target
        sys.exit(f"No Codex sessions found for {where}. "
                 f"Try --all-dirs, --cwd PATH, or --list.")
    if args.match:
        needle = args.match.lower()
        for f, first in files:
            if first and needle in first.lower():
                return f
        sys.exit(f"No session for that directory whose first user message matches {args.match!r}")
    return files[0][0]


def snippet(text, n=200):
    text = " ".join((text or "").split())
    return text[:n] + ("…" if len(text) > n else "")


def output_text(output):
    if isinstance(output, str):
        return output
    if isinstance(output, list):
        return "".join(c.get("text", "") for c in output if isinstance(c, dict))
    return ""


def do_list(target_cwd, all_dirs):
    scope = "all directories" if all_dirs else target_cwd
    print(f"# Recent Codex sessions ({scope})\n")
    for f, _ in sessions_for(target_cwd, all_dirs)[:20]:
        cwd, start, first = meta_and_first_user(f)
        print(f"{start or '?':24}  {cwd or '?'}")
        print(f"    {os.path.relpath(f, ROOT)}")
        print(f"    “{snippet(first, 120)}”\n")


def do_read(path, verbose):
    cwd, start, _ = meta_and_first_user(path)
    print(f"# Codex session: {os.path.basename(path)}")
    print(f"cwd:   {cwd}")
    print(f"start: {start}\n" + "-" * 60)
    for o in records(path):
        t, p = o.get("type"), o.get("payload") or {}
        pt = p.get("type")
        if t == "event_msg" and pt == "user_message":
            print(f"\n### USER\n{(p.get('message') or '').strip()}")
        elif t == "event_msg" and pt == "agent_message":
            print(f"\n### CODEX\n{(p.get('message') or '').strip()}")
        elif t == "event_msg" and pt == "agent_reasoning" and verbose:
            print(f"\n_(reasoning)_ {snippet(p.get('text'), 300)}")
        elif t == "response_item" and pt in ("custom_tool_call", "function_call"):
            arg = p.get("input") if pt == "custom_tool_call" else p.get("arguments")
            print(f"  $ {p.get('name')}: {snippet(arg, 160)}")
        elif t == "response_item" and pt in ("custom_tool_call_output", "function_call_output"):
            out = output_text(p.get("output"))
            if out.strip():
                print(f"    -> {snippet(out, 160)}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--match")
    ap.add_argument("--file")
    ap.add_argument("--cwd")
    ap.add_argument("--all-dirs", action="store_true")
    ap.add_argument("--list", action="store_true")
    ap.add_argument("--verbose", action="store_true")
    args = ap.parse_args()
    if args.list:
        target = os.path.realpath(os.path.expanduser(args.cwd) if args.cwd else os.getcwd())
        do_list(target, args.all_dirs)
        return
    do_read(locate(args), args.verbose)


if __name__ == "__main__":
    main()
