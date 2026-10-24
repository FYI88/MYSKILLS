<div align="center">

# MySkills
## Personal AI Agent Skills Repository

**A centralized, synchronized collection of reusable AI agent skills for Claude Code, OpenCode, and custom agent frameworks.**

![Skills Count](https://img.shields.io/badge/Skills-100%2B-61DAFB?style=for-the-badge&logo=appveyor)
![Git](https://img.shields.io/badge/Git-Synced-107c41?style=for-the-badge&logo=git&logoColor=white)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-3178C6?style=for-the-badge)

Created & Maintained by **FYI88**

</div>

---

## Quick Start

To clone and install all skills onto a new machine or agent environment:

```bash
git clone https://github.com/FYI88/MYSKILLS.git ~/.agents/skills
```

### Linking / Syncing across Agents

| Tool / Framework | Target Skills Path | Installation Command |
|------------------|-------------------|----------------------|
| **Global Agents** | `~/.agents/skills` | `git clone https://github.com/FYI88/MYSKILLS.git ~/.agents/skills` |
| **Claude Code** | `~/.claude/skills` | `ln -s ~/.agents/skills ~/.claude/skills` |
| **OpenCode** | `~/.config/opencode/skills` | `ln -s ~/.agents/skills ~/.config/opencode/skills` |

---

## What's Inside?

This repository contains 100+ production-grade agent skills across key domains:

- **Productivity & Output Shaping** — `adhd`, `ghost`, `short`, `caveman`, `remind`, `ponytail`
- **Security & Red Teaming** — `security-audit`, `auditme` (Active Directory, Cloud, Mobile, IoT, Web, Wireless, Exploitation)
- **Software Engineering & Architecture** — `code-review`, `safe-refactor`, `diagnosing-bugs`, `tdd`, `codebase-design`, `migration`
- **MCP & Agent Building** — `build-mcp-server`, `build-mcp-app`, `build-mcpb`, `agent-development`, `skill-creator`
- **Research & Integrations** — `deep-research`, `deepapi`, `monid`, `youtube-transcript`, `fireflies-transcript`

---

## Repository Structure

```text
./
├── README.md               # Overview and quick start guide
├── <skill-name>/          # Individual skill directory
│   ├── SKILL.md           # Primary skill instructions & frontmatter
│   ├── references/        # Additional documentation & patterns (if applicable)
│   └── scripts/           # Supporting scripts & tools (if applicable)
```

---

## Syncing Updates

To push new skills or updates back to the repo:

```bash
cd ~/.agents/skills
git add -A
git commit -m "Update skills"
git push origin main
```
