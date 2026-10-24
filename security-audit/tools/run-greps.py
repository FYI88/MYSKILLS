#!/usr/bin/env python3
"""
run-greps.py — the security-audit grep blitz, made deterministic.

Reads the pattern arsenal from tools/greps.json, runs every group against a
codebase, and writes hits.json (pattern, file, line, snippet) plus a per-group
hit/no-hit summary. The summary is the evidence for "N/A — confirmed via grep"
claims in the audit report; hits.json feeds Phase 8 re-audits (run before and
after fixes, diff the hit lists).

Usage:
    python tools/run-greps.py --root <app-dir> [--output hits.json]
    python tools/run-greps.py --root <app-dir> --group webrtc-p2p
    python tools/run-greps.py --root <app-dir> --engine rg|re --no-ignore

Engine: ripgrep (rg) is used when available (fast, respects .gitignore, robust
on Windows paths via --json output). Falls back to Python's re module
line-scanning otherwise. The output is identical either way.

Exit code is always 0 unless the tool itself fails; a clean scan (no hits) is
a legitimate, reportable result.
"""

import argparse
import datetime
import json
import os
import re
import shutil
import subprocess
import sys
import time

DEFAULT_IGNORE_DIRS = {
    ".git", "node_modules", "dist", "build", "coverage", ".next", ".nuxt",
    ".venv", "venv", "__pycache__", ".cache", ".freebuff", "vendor",
}
DEFAULT_IGNORE_GLOBS = [
    "!**/node_modules/**", "!**/dist/**", "!**/build/**", "!**/.git/**",
    "!**/coverage/**", "!**/.next/**", "!**/.nuxt/**", "!**/.venv/**",
    "!**/__pycache__/**", "!**/.cache/**", "!**/.freebuff/**",
]
MAX_LINE_BYTES = 1_000_000  # skip files that look binary / are huge
SNIPPET_CAP = 240


def load_greps(path):
    with open(path, "r", encoding="utf-8") as fh:
        data = json.load(fh)
    return data["groups"]


def walk_files(root, ignore):
    """Yield text files under root, skipping hidden dirs and ignore dirs."""
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [
            d for d in dirnames
            if not d.startswith(".") and d not in ignore
        ]
        for name in filenames:
            if name.startswith("."):
                continue
            yield os.path.join(dirpath, name)


def run_with_rg(pattern, root, ci, ignore_globs):
    """Return list of (file, line_no, snippet) via `rg --json`."""
    cmd = ["rg", "--json", "-n", "--no-config"]
    if ci:
        cmd.append("-i")
    for g in ignore_globs:
        cmd += ["--glob", g]
    cmd += ["-e", pattern, root]
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
    except (subprocess.TimeoutExpired, OSError) as exc:
        raise RuntimeError(f"rg failed for {pattern!r}: {exc}") from exc
    if proc.returncode not in (0, 1):  # 1 = no matches, that's fine
        raise RuntimeError(
            f"rg exited {proc.returncode} for {pattern!r}: {proc.stderr[:300]}"
        )
    hits = []
    for line in proc.stdout.splitlines():
        try:
            obj = json.loads(line)
        except json.JSONDecodeError:
            continue
        if obj.get("type") != "match":
            continue
        data = obj["data"]
        path = data.get("path", {}).get("text", "?")
        line_no = data.get("line_number", 0)
        text = data.get("lines", {}).get("text", "").rstrip("\n")
        hits.append((path, line_no, text[:SNIPPET_CAP]))
    return hits


def run_with_re(pattern, root, ci, ignore):
    """Python fallback: line-scan files with the re module."""
    try:
        rx = re.compile(pattern, re.IGNORECASE if ci else 0)
    except re.error as exc:
        raise RuntimeError(f"invalid regex {pattern!r}: {exc}") from exc
    hits = []
    for fpath in walk_files(root, ignore):
        try:
            if os.path.getsize(fpath) > MAX_LINE_BYTES:
                continue
            with open(fpath, "r", encoding="utf-8", errors="ignore") as fh:
                for line_no, line in enumerate(fh, 1):
                    if rx.search(line):
                        hits.append((fpath, line_no, line.rstrip("\n")[:SNIPPET_CAP]))
        except OSError:
            continue
    return hits


def main():
    ap = argparse.ArgumentParser(description="Run the security-audit grep blitz")
    ap.add_argument("--root", default=".", help="codebase root to scan (default: .)")
    ap.add_argument("--output", default="hits.json", help="output file (default: hits.json)")
    ap.add_argument("--group", default=None, help="run only one group id (e.g. webrtc-p2p)")
    ap.add_argument("--time-budget", type=float, default=300.0,
                    help="wall-clock budget in seconds (default 300); scan truncates beyond it")
    ap.add_argument("--engine", choices=["auto", "rg", "re"], default="auto")
    ap.add_argument("--no-ignore", action="store_true", help="also scan ignored dirs")
    args = ap.parse_args()

    script_dir = os.path.dirname(os.path.abspath(__file__))
    greps_path = os.path.join(script_dir, "greps.json")
    groups = load_greps(greps_path)

    ignore = set() if args.no_ignore else DEFAULT_IGNORE_DIRS
    ignore_globs = [] if args.no_ignore else DEFAULT_IGNORE_GLOBS

    if args.engine == "rg" or (args.engine == "auto" and shutil.which("rg")):
        engine = "rg"
        run = lambda p: run_with_rg(p, args.root, True, ignore_globs)
    else:
        engine = "re"
        run = lambda p: run_with_re(p, args.root, True, ignore)

    if args.group:
        groups = [g for g in groups if g["id"] == args.group]
        if not groups:
            sys.exit(f"unknown group id: {args.group}")

    all_hits = []
    group_summary = []
    skipped_patterns = []
    start = time.monotonic()
    timed_out = False
    for g in groups:
        group_hits = []
        for pattern in g["patterns"]:
            if time.monotonic() - start > args.time_budget:
                timed_out = True
                skipped_patterns.append(f"{g['id']}: {pattern}")
                continue
            try:
                hits = run(pattern)
            except RuntimeError as exc:
                print(f"  !! group {g['id']}: {exc}", file=sys.stderr)
                continue
            for fpath, line_no, snippet in hits:
                all_hits.append({
                    "group": g["id"],
                    "pattern": pattern,
                    "file": fpath,
                    "line": line_no,
                    "snippet": snippet,
                })
            group_hits.extend(hits)
        files_hit = {h[0] for h in group_hits}
        group_summary.append({
            "id": g["id"],
            "name": g["name"],
            "patterns": len(g["patterns"]),
            "hits": len(group_hits),
            "files": len(files_hit),
        })

    # Keep output deterministic: sort by group, file, line.
    all_hits.sort(key=lambda h: (h["group"], h["file"], h["line"]))

    report = {
        "tool": "security-audit/run-greps.py",
        "engine": engine,
        "scanned_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "root": os.path.abspath(args.root),
        "groups": group_summary,
        "hits": all_hits,
        "summary": {
            "groups_checked": len(groups),
            "groups_with_hits": sum(1 for g in group_summary if g["hits"] > 0),
            "total_hits": len(all_hits),
        },
    }
    if timed_out:
        report["summary"]["truncated"] = True
        report["summary"]["skipped_patterns"] = skipped_patterns

    with open(args.output, "w", encoding="utf-8") as fh:
        json.dump(report, fh, indent=2, ensure_ascii=False)
        fh.write("\n")

    # Human-readable summary
    print(f"engine: {engine}   root: {report['root']}")
    print(f"output: {args.output}")
    print(f"{'group':<28} {'patterns':>8} {'hits':>6} {'files':>6}")
    print("-" * 52)
    for g in group_summary:
        flag = "  <-- HITS" if g["hits"] else ""
        print(f"{g['id']:<28} {g['patterns']:>8} {g['hits']:>6} {g['files']:>6}{flag}")
    s = report["summary"]
    print("-" * 52)
    print(f"{s['groups_checked']} groups checked, {s['groups_with_hits']} with hits, "
          f"{s['total_hits']} total hits")
    if timed_out:
        print("!! time budget exceeded — scan truncated; skipped patterns are listed in "
              "hits.json under summary.skipped_patterns. Coverage is partial: say so "
              "in the report under Tooling gaps.", file=sys.stderr)


if __name__ == "__main__":
    main()
