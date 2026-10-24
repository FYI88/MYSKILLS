#!/usr/bin/env python3
"""Validate every SKILL.md in the repository.

Checks performed:
  - the file starts with YAML frontmatter delimiters
  - required keys `name` and `description` are present and non-empty
  - `name` matches the containing directory (warning only)
  - the description is not excessively long (warning only)

Usage:
    python scripts/validate_skills.py [--root .]
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None

MAX_DESCRIPTION_LENGTH = 1024


def parse_frontmatter(text: str) -> tuple[dict | None, str]:
    match = re.match(r"^---\s*\n(.*?)\n---\s*(?:\n|$)", text, re.DOTALL)
    if not match:
        return None, "missing YAML frontmatter block (expected '---' delimiters at the top)"
    block = match.group(1)
    if yaml is None:
        data = {}
        for line in block.splitlines():
            if ":" in line and not line.startswith(" "):
                key, _, value = line.partition(":")
                data[key.strip()] = value.strip()
        return data, ""
    try:
        data = yaml.safe_load(block)
    except Exception as error:
        return None, f"invalid YAML frontmatter: {error}"
    if not isinstance(data, dict):
        return None, "frontmatter did not parse into a mapping"
    return data, ""


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate SKILL.md files.")
    parser.add_argument("--root", default=".", help="Repository root")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    errors: list[str] = []
    warnings: list[str] = []
    checked = 0

    for skill_file in sorted(root.rglob("SKILL.md")):
        relative = skill_file.relative_to(root)
        if any(part in (".git", "node_modules") for part in relative.parts):
            continue
        checked += 1
        location = str(relative).replace("\\", "/")

        text = skill_file.read_text(encoding="utf-8", errors="replace")
        data, error = parse_frontmatter(text)
        if error:
            errors.append(f"{location}: {error}")
            continue

        name = str(data.get("name") or "").strip()
        description = str(data.get("description") or "").strip()

        if not name:
            errors.append(f"{location}: missing required 'name'")
        if not description:
            errors.append(f"{location}: missing required 'description'")

        if name and len(relative.parts) > 1:
            folder = relative.parts[0]
            if folder != name and folder not in ("auditme", "watermarks-remover"):
                warnings.append(f"{location}: name '{name}' differs from folder '{folder}'")

        if description and len(description) > MAX_DESCRIPTION_LENGTH:
            warnings.append(
                f"{location}: description is {len(description)} characters "
                f"(recommended maximum {MAX_DESCRIPTION_LENGTH})"
            )

    for warning in warnings:
        print(f"warning: {warning}")
    for error in errors:
        print(f"error: {error}", file=sys.stderr)

    print(f"\nchecked {checked} skill(s): {len(errors)} error(s), {len(warnings)} warning(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
