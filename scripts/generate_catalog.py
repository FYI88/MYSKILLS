#!/usr/bin/env python3
"""Generate CATALOG.md by scanning every SKILL.md in this repository.

Usage:
    python scripts/generate_catalog.py [--root .] [--output CATALOG.md]

The script reads YAML frontmatter from each SKILL.md, groups the skills by
category, and writes a searchable Markdown index. It requires PyYAML
(`pip install pyyaml`); if PyYAML is unavailable a minimal built-in parser is
used instead so the catalog can always be regenerated.
"""

from __future__ import annotations

import argparse
import os
import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None


CATEGORY_BY_FOLDER = {
    "accessibility": "Frontend & Accessibility",
    "adhd": "Output & Communication Style",
    "adhd1": "Output & Communication Style",
    "agent-development": "Agent & Plugin Development",
    "agent-self-scheduling": "Agent & Plugin Development",
    "anti-sleep": "Agent & Plugin Development",
    "ask-matt": "Workflow & Collaboration",
    "ask-then-build": "Workflow & Collaboration",
    "auditme": "Security & Red Teaming",
    "before-building": "Workflow & Collaboration",
    "brain-to-docs": "Documentation & Knowledge",
    "browser-harness": "Integrations & Automation",
    "btw": "Output & Communication Style",
    "build-mcp-app": "Agent & Plugin Development",
    "build-mcp-server": "Agent & Plugin Development",
    "build-mcpb": "Agent & Plugin Development",
    "cardputer-buddy": "Integrations & Automation",
    "cavecrew": "Agent & Plugin Development",
    "caveman": "Output & Communication Style",
    "caveman-commit": "Output & Communication Style",
    "caveman-compress": "Output & Communication Style",
    "caveman-discover": "Output & Communication Style",
    "caveman-evidence-review": "Output & Communication Style",
    "caveman-explore": "Output & Communication Style",
    "caveman-help": "Output & Communication Style",
    "caveman-learn": "Output & Communication Style",
    "caveman-manage": "Output & Communication Style",
    "caveman-optimize": "Output & Communication Style",
    "caveman-review": "Output & Communication Style",
    "caveman-setup": "Output & Communication Style",
    "caveman-stats": "Output & Communication Style",
    "claude-automation-recommender": "Agent & Plugin Development",
    "claude-md-improver": "Documentation & Knowledge",
    "claude-security": "Security & Red Teaming",
    "cmux": "Integrations & Automation",
    "code-review": "Software Engineering",
    "codebase-design": "Software Engineering",
    "codex-subagent": "Agent & Plugin Development",
    "command-development": "Agent & Plugin Development",
    "corral-launch-agents": "Agent & Plugin Development",
    "create-readonly-db-role": "Integrations & Automation",
    "decisions": "Workflow & Collaboration",
    "deep-research": "Research & Analysis",
    "deepapi": "Research & Analysis",
    "diagnosing-bugs": "Software Engineering",
    "discord-access": "Integrations & Automation",
    "discord-configure": "Integrations & Automation",
    "distribute-skill-to-all-agents": "Agent & Plugin Development",
    "domain-modeling": "Documentation & Knowledge",
    "effective-agent-skills": "Agent & Plugin Development",
    "example-command": "Agent & Plugin Development",
    "example-skill": "Agent & Plugin Development",
    "fable-review": "Agent & Plugin Development",
    "fable-safe-prompt": "Agent & Plugin Development",
    "fireflies-transcript": "Research & Analysis",
    "folder-specific-claude-and-agents-md": "Documentation & Knowledge",
    "framer": "Frontend & Accessibility",
    "framer-code-components": "Frontend & Accessibility",
    "frontend-design": "Frontend & Accessibility",
    "frontend-patterns": "Frontend & Accessibility",
    "ghost": "Output & Communication Style",
    "git-guardrails-claude-code": "Integrations & Automation",
    "git-worktree": "Software Engineering",
    "github-outside-sandbox": "Integrations & Automation",
    "global-agent-guardrails": "Integrations & Automation",
    "goal-loop": "Agent & Plugin Development",
    "google-safe-browsing": "Integrations & Automation",
    "gpt-review": "Agent & Plugin Development",
    "grill-me": "Workflow & Collaboration",
    "grill-with-docs": "Workflow & Collaboration",
    "grilling": "Workflow & Collaboration",
    "handoff": "Workflow & Collaboration",
    "herdr": "Agent & Plugin Development",
    "hook-development": "Agent & Plugin Development",
    "imessage-access": "Integrations & Automation",
    "imessage-configure": "Integrations & Automation",
    "implement": "Software Engineering",
    "improve-codebase-architecture": "Software Engineering",
    "investigate-first": "Software Engineering",
    "launch-subagent": "Agent & Plugin Development",
    "lean-build": "Software Engineering",
    "level-up": "Documentation & Knowledge",
    "m5-onboard": "Integrations & Automation",
    "macbook-metrics-setup": "Integrations & Automation",
    "math-olympiad": "Research & Analysis",
    "mcp-integration": "Agent & Plugin Development",
    "migrate-to-shoehorn": "Software Engineering",
    "migration": "Software Engineering",
    "monid": "Research & Analysis",
    "next-decision": "Workflow & Collaboration",
    "nuke-cursor-app": "Integrations & Automation",
    "online-shopping": "Research & Analysis",
    "pi-custom-model": "Agent & Plugin Development",
    "pi-web-search": "Research & Analysis",
    "playground": "Frontend & Accessibility",
    "plugin-settings": "Agent & Plugin Development",
    "plugin-structure": "Agent & Plugin Development",
    "ponytail": "Software Engineering",
    "ponytail-audit": "Software Engineering",
    "ponytail-debt": "Software Engineering",
    "ponytail-gain": "Software Engineering",
    "ponytail-help": "Software Engineering",
    "ponytail-review": "Software Engineering",
    "prod-push": "Integrations & Automation",
    "project-artifact": "Documentation & Knowledge",
    "prompt-me": "Workflow & Collaboration",
    "prototype": "Software Engineering",
    "push-skill-to-github": "Integrations & Automation",
    "read-all-adrs": "Documentation & Knowledge",
    "read-prod-database": "Integrations & Automation",
    "receipts": "Documentation & Knowledge",
    "remind": "Output & Communication Style",
    "remove-ai-marks": "Integrations & Automation",
    "research": "Research & Analysis",
    "research-prompt": "Research & Analysis",
    "resolving-merge-conflicts": "Software Engineering",
    "run-deep-swe": "Research & Analysis",
    "safe-refactor": "Software Engineering",
    "scaffold-exercises": "Documentation & Knowledge",
    "security-audit": "Security & Red Teaming",
    "session-report": "Documentation & Knowledge",
    "setup-help": "Workflow & Collaboration",
    "setup-matt-pocock-skills": "Documentation & Knowledge",
    "setup-pre-commit": "Software Engineering",
    "short": "Output & Communication Style",
    "skill-creator": "Agent & Plugin Development",
    "skill-development": "Agent & Plugin Development",
    "stop-overthinking": "Output & Communication Style",
    "surgical-patch": "Software Engineering",
    "tdd": "Software Engineering",
    "teach": "Documentation & Knowledge",
    "telegram-access": "Integrations & Automation",
    "telegram-configure": "Integrations & Automation",
    "to-questionnaire": "Workflow & Collaboration",
    "to-spec": "Workflow & Collaboration",
    "to-tickets": "Workflow & Collaboration",
    "triage": "Workflow & Collaboration",
    "unlazy": "Workflow & Collaboration",
    "verify-and-stop": "Software Engineering",
    "wait-what": "Output & Communication Style",
    "watermarks-remover": "Integrations & Automation",
    "wayfinder": "Workflow & Collaboration",
    "wizard": "Integrations & Automation",
    "writing-for-agents": "Documentation & Knowledge",
    "writing-rules": "Agent & Plugin Development",
    "youtube-transcript": "Research & Analysis",
}

FALLBACK_CATEGORY = "Other"


def parse_frontmatter(text: str) -> dict:
    """Extract YAML frontmatter from a SKILL.md file."""
    match = re.match(r"^---\s*\n(.*?)\n---\s*(?:\n|$)", text, re.DOTALL)
    if not match:
        return {}
    block = match.group(1)
    if yaml is not None:
        try:
            data = yaml.safe_load(block)
            return data if isinstance(data, dict) else {}
        except Exception:
            pass
    return _minimal_frontmatter(block)


def _minimal_frontmatter(block: str) -> dict:
    """Fallback parser for flat key/value frontmatter with block scalars."""
    data: dict = {}
    key = None
    for line in block.splitlines():
        if key and (line.startswith("  ") or line.startswith("\t") or not line.strip()):
            data[key] = f"{data.get(key, '')} {line.strip()}".strip()
            continue
        if ":" not in line:
            continue
        key, _, value = line.partition(":")
        key = key.strip()
        value = value.strip()
        if value in (">", ">-", "|", "|-"):
            value = ""
        data[key] = value
    return data


def clean_description(value: object) -> str:
    if not isinstance(value, str):
        return ""
    text = " ".join(value.split())
    text = text.replace("|", "\\|")
    return text


def resolve_category(folder: str, metadata: dict) -> str:
    raw = metadata.get("category") or metadata.get("tags")
    if isinstance(raw, str) and raw.strip() and folder not in CATEGORY_BY_FOLDER:
        return raw.strip().title()
    return CATEGORY_BY_FOLDER.get(folder, FALLBACK_CATEGORY)


def discover_skills(root: Path) -> list[dict]:
    skills = []
    for skill_file in sorted(root.rglob("SKILL.md")):
        relative = skill_file.relative_to(root)
        if any(part in (".git", "node_modules") for part in relative.parts):
            continue
        try:
            text = skill_file.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        frontmatter = parse_frontmatter(text)
        folder = relative.parts[0] if len(relative.parts) > 1 else relative.stem
        name = str(frontmatter.get("name") or folder)
        description = clean_description(frontmatter.get("description"))
        nested = " / ".join(relative.parts[:-1])
        skills.append(
            {
                "name": name,
                "description": description,
                "folder": folder,
                "path": str(relative).replace(os.sep, "/"),
                "nested": nested,
                "category": resolve_category(folder, frontmatter.get("metadata") or {}),
            }
        )
    return skills


def build_catalog(skills: list[dict]) -> str:
    grouped: dict[str, list[dict]] = {}
    for skill in skills:
        grouped.setdefault(skill["category"], []).append(skill)

    total = len(skills)
    lines = [
        "<div align=\"center\">",
        "",
        "# MySkills Catalog",
        "",
        f"**{total} skills · auto-generated index of every `SKILL.md` in this repository.**",
        "",
        "![Skills](https://img.shields.io/badge/Skills-"
        f"{total}-61DAFB?style=for-the-badge)",
        "![Generated](https://img.shields.io/badge/Generated-automatically-107c41?style=for-the-badge)",
        "",
        "</div>",
        "",
        "---",
        "",
        "## Categories",
        "",
        "| Category | Skills |",
        "|----------|--------|",
    ]

    for category in sorted(grouped):
        lines.append(f"| {category} | {len(grouped[category])} |")
    lines.append(f"| **Total** | **{total}** |")
    lines.extend(["", "---", ""])

    for category in sorted(grouped):
        lines.append(f"## {category}")
        lines.append("")
        lines.append("| Skill | Description | Path |")
        lines.append("|-------|-------------|------|")
        for skill in sorted(grouped[category], key=lambda item: item["name"].lower()):
            description = skill["description"] or "_No description provided._"
            if len(description) > 220:
                description = description[:217].rstrip() + "..."
            lines.append(
                f"| `{skill['name']}` | {description} | `{skill['path']}` |"
            )
        lines.append("")

    lines.extend(
        [
            "---",
            "",
            "## Regenerating this catalog",
            "",
            "```bash",
            "python scripts/generate_catalog.py",
            "```",
            "",
            "</div>",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate CATALOG.md for MySkills.")
    parser.add_argument("--root", default=".", help="Repository root (default: current directory)")
    parser.add_argument("--output", default="CATALOG.md", help="Output file path")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    if not root.is_dir():
        print(f"error: root not found: {root}", file=sys.stderr)
        return 1

    skills = discover_skills(root)
    if not skills:
        print("error: no SKILL.md files found", file=sys.stderr)
        return 1

    output = Path(args.output)
    if not output.is_absolute():
        output = root / output
    output.write_text(build_catalog(skills), encoding="utf-8")

    categories = len({skill["category"] for skill in skills})
    print(f"wrote {output} ({len(skills)} skills across {categories} categories)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
