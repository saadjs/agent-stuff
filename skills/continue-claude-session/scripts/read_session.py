#!/usr/bin/env python3
"""Read local Claude transcripts without dumping metadata or binary payloads."""

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path.home() / ".claude" / "projects"
OUTCOME = re.compile(
    r"(?i)(test.*(?:passed|failed|succeeded)|executed \d+ tests|exit code|error:|TEST (?:SUCCEEDED|FAILED))"
)


def records(path):
    with path.open(encoding="utf-8") as stream:
        for line, raw in enumerate(stream, 1):
            if not raw.strip():
                continue
            try:
                record = json.loads(raw)
                if not isinstance(record, dict):
                    raise ValueError("expected an object")
            except ValueError as error:
                print(
                    f"Warning: {path}:{line}: skipped invalid record ({error})",
                    file=sys.stderr,
                )
                continue
            yield line, record


def safe(value):
    """Remove encoded attachments, including those nested in tool results."""
    if isinstance(value, list):
        return [safe(item) for item in value]
    if isinstance(value, dict):
        if value.get("type") in ("image", "document", "image_url"):
            return {"omitted": value["type"] + " payload"}
        if value.get("type") == "base64":
            return {"omitted": "base64 payload"}
        return {key: safe(item) for key, item in value.items()}
    return value


def content_text(value):
    if isinstance(value, str):
        return value
    if isinstance(value, list):
        return "\n".join(content_text(item) for item in value)
    if isinstance(value, dict):
        return value.get("text") or json.dumps(safe(value), ensure_ascii=False)
    return str(value)


def compact(text, limit=350):
    flat = " ".join(text.split())
    if len(flat) <= limit:
        return flat
    return (
        flat[:limit]
        + f" … [condensed; {len(flat) - limit} characters omitted; expand by line or tool ID]"
    )


def metadata(rows, path):
    cwds = list(dict.fromkeys(r["cwd"] for _, r in rows if r.get("cwd")))
    branches = list(
        dict.fromkeys(r["gitBranch"] for _, r in rows if r.get("gitBranch"))
    )
    title = next(
        (r["customTitle"] for _, r in reversed(rows) if r.get("customTitle")), ""
    )
    first = ""
    for _, row in rows:
        if row.get("type") == "user":
            value = row.get("message", {}).get("content", [])
            blocks = (
                [{"type": "text", "text": value}] if isinstance(value, str) else value
            )
            first = "\n".join(
                b.get("text", "") for b in blocks if b.get("type") == "text"
            )
            if first:
                break
    dates = [r["timestamp"] for _, r in rows if r.get("timestamp")]
    return dict(
        id=path.stem,
        title=title,
        cwds=cwds,
        branches=branches,
        first=first,
        updated=max(dates, default=""),
    )


def events(rows, reasoning=False):
    for line, row in rows:
        kind = row.get("type")
        if kind == "system" and row.get("subtype") == "compact_boundary":
            yield dict(
                line=line, kind="COMPACTION", id="", text=json.dumps(safe(row)), name=""
            )
        if kind not in ("user", "assistant"):
            continue
        blocks = row.get("message", {}).get("content", [])
        if isinstance(blocks, str):
            blocks = [{"type": "text", "text": blocks}]
        for block in blocks:
            t = block.get("type")
            event = dict(line=line, kind=kind.upper(), id="", name="", text="")
            if t == "text":
                event["text"] = block.get("text", "")
            elif t == "thinking":
                if not reasoning:
                    continue
                event.update(kind="REASONING", text=block.get("thinking", ""))
            elif t == "tool_use":
                event.update(
                    kind="CALL",
                    id=block.get("id", ""),
                    name=block.get("name", ""),
                    text=json.dumps(safe(block.get("input", {})), ensure_ascii=False),
                )
            elif t == "tool_result":
                event.update(
                    kind="ERROR RESULT" if block.get("is_error") else "RESULT",
                    id=block.get("tool_use_id", ""),
                    text=content_text(block.get("content", "")),
                )
            else:
                event["text"] = f"[{t or 'unknown'} block omitted]"
            yield event


def locate(args):
    if args.file:
        return Path(args.file).expanduser()
    # Top-level transcripts only; subagent and tool-result files are not sessions.
    files = list(ROOT.glob("*/*.jsonl"))
    if args.session:
        files = [p for p in files if p.stem == args.session]
        if len(files) != 1:
            raise ValueError(
                f"Expected one session with ID {args.session}; found {len(files)}. Use --file PATH."
            )
        return files[0]
    target = Path(args.cwd).expanduser().resolve()
    matches = []
    for path in files:
        info = metadata(list(records(path)), path)
        if not args.all_dirs and not any(
            Path(c).expanduser().resolve() == target for c in info["cwds"]
        ):
            continue
        if (
            args.match
            and args.match.casefold()
            not in (info["title"] + "\n" + info["first"]).casefold()
        ):
            continue
        matches.append((info["updated"], path.stat().st_mtime, path, info))
    matches.sort(key=lambda item: (item[0], item[1], str(item[2])), reverse=True)
    if not matches:
        raise ValueError(
            f"No matching Claude sessions for {'all directories' if args.all_dirs else target}. Use --list, --cwd PATH, or explicitly --all-dirs."
        )
    if args.list:
        for _, _, path, info in matches[: args.limit]:
            print(
                f"{info['updated']}  {info['id']}\n  {info['title'] or compact(info['first'], 120)}\n  cwd: {', '.join(info['cwds'])}\n  {path}"
            )
        return None
    return matches[0][2]


def render(event, expanded=False):
    text = event["text"]
    if not expanded and event["kind"] in ("CALL", "RESULT", "ERROR RESULT"):
        text = compact(text)
    label = " ".join(str(event[k]) for k in ("kind", "name", "id") if event[k])
    return f"L{event['line']} {label}\n{text}"


def essentials(items):
    print(
        "\nContinuation evidence (recorded history; verify current repository state):"
    )
    calls = {e["id"]: e for e in items if e["kind"] == "CALL"}
    results = {e["id"]: e for e in items if "RESULT" in e["kind"]}
    for event in calls.values():
        name = event["name"]
        if name in ("Bash", "Shell"):
            data = json.loads(event["text"])
            command = data.get("command", "")
            if re.search(
                r"(?i)(worktree|git\s+(?:-C\s+\S+\s+)?(?:checkout|switch|branch)|(?:^|[;&\n])\s*cd\s)",
                command,
            ):
                print(
                    f"  L{event['line']} {event['id']} directory/branch command (attempt): {compact(command)}"
                )
        if name in ("Edit", "Write", "MultiEdit", "NotebookEdit"):
            data = json.loads(event["text"])
            result = results.get(event["id"])
            status = (
                "no result recorded"
                if result is None
                else (
                    "error recorded"
                    if result["kind"] == "ERROR RESULT"
                    else "result recorded; inspect to confirm change"
                )
            )
            print(
                f"  L{event['line']} file operation: {data.get('file_path', data.get('notebook_path', '?'))} ({status})"
            )
        if "task" in name.lower() or "todo" in name.lower():
            print(f"  Task update: {render(event)}")
    for event in items:
        if "RESULT" in event["kind"]:
            evidence = [
                line for line in event["text"].splitlines() if OUTCOME.search(line)
            ]
            if evidence:
                print(
                    f"  L{event['line']} {event['id']} outcome excerpts: {compact(' | '.join(evidence), 600)}"
                )
    if calls:
        last = list(calls.values())[-1]
        print("  Final call: " + render(last))
        result = results.get(last["id"])
        print(
            "  Matching result: "
            + (render(result) if result else "none recorded; completion unknown")
        )
    pending = [e for key, e in calls.items() if key not in results]
    if pending:
        print(
            "  Calls without results: "
            + ", ".join(f"L{e['line']} {e['id']}" for e in pending)
        )
    print(
        "  A call is an attempt. A returned result may still describe a running command.\n"
        "  File operations above exclude changes made through shell commands; inspect those as needed."
    )


def line_range(value):
    try:
        bounds = [int(x) for x in value.split(":")]
        start, end = (bounds * 2) if len(bounds) == 1 else bounds
        if not 1 <= start <= end:
            raise ValueError()
        return start, end
    except ValueError:
        raise argparse.ArgumentTypeError(
            "use positive inclusive line numbers, e.g. 42 or 42:60"
        )


def positive(value):
    number = int(value)
    if number < 1:
        raise argparse.ArgumentTypeError("must be positive")
    return number


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    source = parser.add_mutually_exclusive_group()
    source.add_argument(
        "session", nargs="?", help="exact session ID (searches all project directories)"
    )
    source.add_argument("--file", help="explicit transcript path")
    parser.add_argument(
        "--cwd",
        default=str(Path.cwd()),
        help="project directory; defaults to current directory",
    )
    parser.add_argument("--all-dirs", action="store_true")
    parser.add_argument(
        "--match", help="case-insensitive title or first user message substring"
    )
    parser.add_argument("--list", action="store_true")
    parser.add_argument(
        "--limit", type=positive, default=20, help="maximum listed sessions"
    )
    view = parser.add_mutually_exclusive_group()
    view.add_argument(
        "--search",
        help="search full conversation and tool text, with matching excerpts",
    )
    view.add_argument("--tail", type=positive, help="last N visible blocks")
    view.add_argument(
        "--lines", type=line_range, help="expand original JSONL lines START:END"
    )
    view.add_argument("--tool", help="expand a tool call and its results by exact ID")
    parser.add_argument(
        "--reasoning", action="store_true", help="include recorded reasoning"
    )
    args = parser.parse_args()
    if (args.session or args.file) and (args.list or args.match or args.all_dirs):
        parser.error(
            "explicit session/file cannot be combined with --list, --match, or --all-dirs"
        )
    try:
        path = locate(args)
        if path is None:
            return
        rows = list(records(path))
        info = metadata(rows, path)
        items = list(events(rows, args.reasoning))
        print(
            f"Claude session: {info['id']}\nTitle: {info['title'] or '(none)'}\nSource: {path}\n"
            f"Recorded directories: {', '.join(info['cwds']) or 'unknown'}\n"
            f"Recorded branches: {', '.join(info['branches']) or 'unknown'}"
        )
        print(
            "Metadata and binary attachments omitted; reasoning omitted unless --reasoning.\n"
            "L numbers refer to original JSONL lines. Tool text is condensed unless expanded."
        )
        if args.lines:
            start, end = args.lines
            selected = [e for e in items if start <= e["line"] <= end]
            visible = {e["line"] for e in selected}
            for line, row in rows:
                if start <= line <= end and line not in visible:
                    print(
                        f"L{line} {row.get('type', 'unknown')} [metadata or reasoning omitted]"
                    )
        elif args.tool:
            selected = [e for e in items if e["id"] == args.tool]
        elif args.search:
            selected = [
                e
                for e in items
                if args.search.casefold() in e["text"].casefold()
                or args.search.casefold() in e["name"].casefold()
            ]
        else:
            selected = items[-args.tail :] if args.tail else items
        if not (args.lines or args.tool or args.search or args.tail):
            essentials(items)
        print(
            "\nTranscript"
            + (" (filtered)" if len(selected) != len(items) else "")
            + ":"
        )
        for event in selected:
            if args.search:
                text = event["text"]
                pos = text.casefold().find(args.search.casefold())
                excerpt = text[max(0, pos - 120) : max(0, pos) + len(args.search) + 300]
                event = dict(
                    event,
                    text="[search excerpt; expand by line or tool ID]\n" + excerpt,
                )
            print(render(event, expanded=bool(args.lines or args.tool or args.search)))
        if not selected:
            print("(no matching visible blocks)")
    except (OSError, ValueError) as error:
        parser.exit(1, f"Error: {error}\n")


if __name__ == "__main__":
    main()
