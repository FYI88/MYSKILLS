<div align="center">

# Skills
## Personal AI Agent Skills Repository

**A centralized, synchronized collection of reusable AI agent skills for Claude Code, OpenCode, Codex, Pi, Hermes, and custom agent frameworks.**

![Skills](https://img.shields.io/badge/Skills-200-61DAFB?style=for-the-badge&logo=appveyor)
![Git](https://img.shields.io/badge/Git-Synced-107c41?style=for-the-badge&logo=git&logoColor=white)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-3178C6?style=for-the-badge)
![License](https://img.shields.io/badge/License-Mixed-ff6b35?style=for-the-badge)

Created & Maintained by **FYI88**

</div>

---

## Quick Start

### One-line install (recommended)

```bash
# macOS / Linux
curl -fsSL https://raw.githubusercontent.com/FYI88/MYSKILLS/main/install.sh | bash
```

```powershell
# Windows PowerShell
irm https://raw.githubusercontent.com/FYI88/MYSKILLS/main/install.ps1 | iex
```

The installer clones the repo into `~/.agents/skills`, then links it into every agent that reads a standard skills folder. **Re-run it any time to pull the latest skills.**

### Manual install

```bash
git clone https://github.com/FYI88/MYSKILLS.git ~/.agents/skills
```

### Installer options

| Option | `install.sh` | `install.ps1` | Action |
|--------|--------------|---------------|--------|
| Custom repo | `--repo URL` | `-Repo URL` | Install from a fork or mirror |
| Custom branch | `--branch NAME` | `-Branch NAME` | Track a different branch |
| Custom location | `--dir PATH` | `-Dir PATH` | Change the canonical skills folder |
| Skip agent linking | `--no-link` | `-NoLink` | Canonical copy only |
| Skip Hermes copy | `--no-hermes` | `-NoHermes` | Do not copy skills for Hermes |
| Repoint existing links | `--force` | `-Force` | Replace diverged links and entries |
| Preview only | `--dry-run` | `-DryRun` | Print the plan, change nothing |

---

## Agent Coverage

The installer wires the canonical collection into every standard location:

| Agent | Skills Folder | Link Method |
|-------|---------------|-------------|
| **Global Agents / Codex** | `~/.agents/skills` | Canonical clone |
| **Claude Code** | `~/.claude/skills` | Symlink / NTFS junction |
| **OpenCode** | `~/.config/opencode/skills` | Symlink / NTFS junction |
| **Pi Agent** | `~/.pi/agent/skills` | Symlink / NTFS junction |
| **Hermes** | `~/.hermes/skills` | Independent copy (Hermes snapshots skills at session start) |

> **Note:** Pi reads from `~/.pi/agent/skills` — the nested `agent/` path is required. `~/.pi/skills` is ignored.

---

## What's Inside?

**200 skills** across 9 categories — see the full searchable index in **[CATALOG.md](CATALOG.md)**.

- **Agent & Plugin Development** (29) — `agent-development`, `build-mcp-server`, `build-mcp-app`, `build-mcpb`, `skill-creator`, `hook-development`, `plugin-structure`
- **Security & Red Teaming** (58) — `security-audit`, `claude-security`, `auditme` (Active Directory, Cloud, Mobile, IoT, Web, Wireless, Exploit Dev, OSINT)
- **Software Engineering** (23) — `code-review`, `safe-refactor`, `diagnosing-bugs`, `tdd`, `codebase-design`, `migration`, `surgical-patch`
- **Integrations & Automation** (22) — `discord-configure`, `telegram-access`, `imessage-configure`, `m5-onboard`, `cardputer-buddy`, `deepapi`
- **Output & Communication Style** (21) — `adhd`, `ghost`, `short`, `caveman`, `remind`, `ponytail`, `wait-what`
- **Workflow & Collaboration** (17) — `brain-to-docs`, `grill-me`, `to-spec`, `to-tickets`, `triage`, `wayfinder`, `handoff`
- **Documentation & Knowledge** (13) — `claude-md-improver`, `domain-modeling`, `teach`, `level-up`, `read-all-adrs`
- **Research & Analysis** (11) — `deep-research`, `monid`, `youtube-transcript`, `math-olympiad`, `run-deep-swe`
- **Frontend & Accessibility** (6) — `frontend-design`, `frontend-patterns`, `accessibility`, `framer`, `playground`

---

## Repository Structure

```text
./
├── README.md                    # This file
├── CATALOG.md                   # Auto-generated searchable index of all skills
├── install.sh                   # macOS / Linux installer
├── install.ps1                  # Windows PowerShell installer
├── scripts/
│   └── generate_catalog.py      # Regenerates CATALOG.md from SKILL.md frontmatter
├── <skill-name>/                # Individual skill directory
│   ├── SKILL.md                 # Primary skill instructions & frontmatter
│   ├── references/              # Additional documentation & patterns (if applicable)
│   └── scripts/                 # Supporting scripts & tools (if applicable)
└── .github/workflows/           # Automated validation on every push
```

---

## Adding a Skill

1. Create `<skill-name>/SKILL.md` with YAML frontmatter:

   ```markdown
   ---
   name: my-skill
   description: What it does and when to use it. Include trigger phrases.
   ---

   # My Skill
   Instructions here.
   ```

2. Regenerate the catalog:

   ```bash
   python scripts/generate_catalog.py
   ```

3. Commit and push — the installers pull the new skill on the next run.

---

## Syncing Updates

**Pulling the latest skills on any machine:**

```bash
# macOS / Linux
curl -fsSL https://raw.githubusercontent.com/FYI88/MYSKILLS/main/install.sh | bash

# Windows PowerShell
irm https://raw.githubusercontent.com/FYI88/MYSKILLS/main/install.ps1 | iex
```

**Publishing changes from your canonical copy:**

```bash
cd ~/.agents/skills
git add -A
git commit -m "Update skills"
git push origin main
```

---

## License

Skills carry their own licenses — see each skill's frontmatter and any `LICENSE` file inside its directory. Third-party vendored skills retain their original terms.
