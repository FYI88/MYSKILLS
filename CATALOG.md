<div align="center">

# MySkills Catalog

**200 skills · auto-generated index of every `SKILL.md` in this repository.**

![Skills](https://img.shields.io/badge/Skills-200-61DAFB?style=for-the-badge)
![Generated](https://img.shields.io/badge/Generated-automatically-107c41?style=for-the-badge)

</div>

---

## Categories

| Category | Skills |
|----------|--------|
| Agent & Plugin Development | 29 |
| Documentation & Knowledge | 13 |
| Frontend & Accessibility | 6 |
| Integrations & Automation | 22 |
| Output & Communication Style | 21 |
| Research & Analysis | 11 |
| Security & Red Teaming | 58 |
| Software Engineering | 23 |
| Workflow & Collaboration | 17 |
| **Total** | **200** |

---

## Agent & Plugin Development

| Skill | Description | Path |
|-------|-------------|------|
| `agent-development` | This skill should be used when the user asks to "create an agent", "add an agent", "write a subagent", "agent frontmatter", "when to use description", "agent examples", "agent tools", "agent colors", "autonomous agent... | `agent-development/SKILL.md` |
| `agent-self-scheduling` | Make an AI agent run on a schedule, loop, or interval — cron, heartbeats, recurring autonomous checks. Use for "run every N minutes", "schedule a task", "run on a loop", "heartbeat". Covers external clocks (Claude Cod... | `agent-self-scheduling/SKILL.md` |
| `anti-sleep` | Keep the user's MacBook awake reliably with macOS caffeinate for a set duration or while a process runs. Use for "don't let my Mac sleep", "keep the screen on", "anti-sleep", "caffeinate", overnight work, or long buil... | `anti-sleep/SKILL.md` |
| `build-mcp-app` | This skill should be used when the user wants to build an "MCP app", add "interactive UI" or "widgets" to an MCP server, "render components in chat", build "MCP UI resources", make a tool that shows a "form", "picker"... | `build-mcp-app/SKILL.md` |
| `build-mcp-server` | This skill should be used when the user asks to "build an MCP server", "create an MCP", "make an MCP integration", "wrap an API for Claude", "expose tools to Claude", "make an MCP app", or discusses building something... | `build-mcp-server/SKILL.md` |
| `build-mcpb` | This skill should be used when the user wants to "package an MCP server", "bundle an MCP", "make an MCPB", "ship a local MCP server", "distribute a local MCP", discusses ".mcpb files", mentions bundling a Node or Pyth... | `build-mcpb/SKILL.md` |
| `cavecrew` | Decision guide for delegating to caveman-style subagents. Tells the main thread WHEN to spawn `cavecrew-investigator` (locate code), `cavecrew-builder` (1-2 file edit), or `cavecrew-reviewer` (diff review) instead of... | `cavecrew/SKILL.md` |
| `claude-automation-recommender` | Analyze a codebase and recommend Claude Code automations (hooks, subagents, skills, plugins, MCP servers). Use when user asks for automation recommendations, wants to optimize their Claude Code setup, mentions improvi... | `claude-automation-recommender/SKILL.md` |
| `codex-subagent` | Launch OpenAI Codex CLI as a subagent (ChatGPT subscription auth, no API key). Use when delegating a self-contained coding task to Codex from another agent — parallel implementation work, a second opinion, or an indep... | `codex-subagent/SKILL.md` |
| `command-development` | This skill should be used when the user asks to "create a slash command", "add a command", "write a custom command", "define command arguments", "use command frontmatter", "organize commands", "create command with fil... | `command-development/SKILL.md` |
| `corral-launch-agents` | Launch new CLI coding agents through Corral Design 1, or correctly reopen existing agent sessions inside a Corral-active Herdr repository. Use when the user asks to launch, spawn, batch-start, reopen, relaunch, or res... | `corral-launch-agents/SKILL.md` |
| `distribute-skill-to-all-agents` | Distribute a skill across the 4 agent skill folders (Codex, Claude Code, Pi, Hermes) so all agents see it. Use when the user says "distribute this skill", "sync skills across agents", or after creating/updating a skil... | `distribute-skill-to-all-agents/SKILL.md` |
| `effective-agent-skills` | How to write effective agent skills — what to do, what not to do, anatomy, progressive disclosure, design patterns, anti-patterns, testing, security. Read this whenever a skill (Claude Skill, Agent Skill, SKILL.md) is... | `effective-agent-skills/SKILL.md` |
| `example-command` | An example user-invoked skill that demonstrates frontmatter options and the skills/<name>/SKILL.md layout | `example-command/SKILL.md` |
| `example-skill` | This skill should be used when the user asks to "demonstrate skills", "show skill format", "create a skill template", or discusses skill development patterns. Provides a reference template for creating Claude Code plu... | `example-skill/SKILL.md` |
| `fable-review` | Launch a Fable 5 Max 1M subagent to do a deep, neutral senior-developer review of the current work and report its findings back verbatim. Use when the user says "/fable-review", "fable review", or asks for Fable to re... | `fable-review/SKILL.md` |
| `fable-safe-prompt` | Rewrite a user's prompt to reduce the chance it trips Claude Fable 5's server-side safety classifiers (cyber/bio guardrails that force-route to Opus 4.8 or return stop_reason "refusal"). Use when the user hands you a... | `fable-safe-prompt/SKILL.md` |
| `goal-loop` | Explain and write effective instructions for the `/goal` feature — the persistent self-checking agent loop (plan → act → test → review → iterate), available in agents like Codex, Claude Code, and Hermes Agent. Use whe... | `goal-loop/SKILL.md` |
| `gpt-review` | Launch a GPT 5.6 Sol Max subagent to do a deep, neutral senior-developer review of the current work and report its findings back verbatim. Use when the user says "/gpt-review", "gpt review", or asks for GPT to review... | `gpt-review/SKILL.md` |
| `herdr` | Operate and coordinate AI agents running inside Herdr in Ghostty. Use when the user says "Use the Herdr skill," mentions Herdr, or asks to inspect, message, wait for, or coordinate agents in a Herdr workspace. Herdr-s... | `herdr/SKILL.md` |
| `hook-development` | This skill should be used when the user asks to "create a hook", "add a PreToolUse/PostToolUse/Stop hook", "validate tool use", "implement prompt-based hooks", "use ${CLAUDE_PLUGIN_ROOT}", "set up event-driven automat... | `hook-development/SKILL.md` |
| `launch-subagent` | Read this BEFORE launching any subagent (Task tool, background agents, parallel agents, best-of-N, delegating work to another agent). Hard model rules for subagents plus consensus principles for using them well. Trigg... | `launch-subagent/SKILL.md` |
| `mcp-integration` | This skill should be used when the user asks to "add MCP server", "integrate MCP", "configure MCP in plugin", "use .mcp.json", "set up Model Context Protocol", "connect external service", mentions "${CLAUDE_PLUGIN_ROO... | `mcp-integration/SKILL.md` |
| `pi-custom-model` | Register a custom or variant model (e.g. an OpenRouter ":nitro" / ":floor" / ":exacto" slug) in the Pi Agent so it can be set as the global default. Use when Pi silently falls back to a different model (e.g. moonshota... | `pi-custom-model/SKILL.md` |
| `plugin-settings` | This skill should be used when the user asks about "plugin settings", "store plugin configuration", "user-configurable plugin", ".local.md files", "plugin state files", "read YAML frontmatter", "per-project plugin set... | `plugin-settings/SKILL.md` |
| `plugin-structure` | This skill should be used when the user asks to "create a plugin", "scaffold a plugin", "understand plugin structure", "organize plugin components", "set up plugin.json", "use ${CLAUDE_PLUGIN_ROOT}", "add commands/age... | `plugin-structure/SKILL.md` |
| `skill-creator` | Create new skills, modify and improve existing skills, and measure skill performance. Use when users want to create a skill from scratch, edit, or optimize an existing skill, run evals to test a skill, benchmark skill... | `skill-creator/SKILL.md` |
| `skill-development` | This skill should be used when the user wants to "create a skill", "add a skill to plugin", "write a new skill", "improve skill description", "organize skill content", or needs guidance on skill structure, progressive... | `skill-development/SKILL.md` |
| `writing-rules` | This skill should be used when the user asks to "create a hookify rule", "write a hook rule", "configure hookify", "add a hookify rule", or needs guidance on hookify rule syntax and patterns. | `writing-rules/SKILL.md` |

## Documentation & Knowledge

| Skill | Description | Path |
|-------|-------------|------|
| `brain-to-docs` | Use when the user wants to extract project vision, decisions, and preferences from his head into clear documentation (README + ADRs) through a back-and-forth Q&A loop. Triggers on "brain-to-docs", "build out the docs"... | `brain-to-docs/SKILL.md` |
| `claude-md-improver` | Audit and improve CLAUDE.md files in repositories. Use when user asks to check, audit, update, improve, or fix CLAUDE.md files. Scans for all CLAUDE.md files, evaluates quality against templates, outputs quality repor... | `claude-md-improver/SKILL.md` |
| `domain-modeling` | Build and sharpen a project's domain model. Use when the user wants to pin down domain terminology or a ubiquitous language, record an architectural decision, or when another skill needs to maintain the domain model. | `domain-modeling/SKILL.md` |
| `folder-specific-claude-and-agents-md` | Create a specialized CLAUDE.md (+ AGENTS.md symlink) inside a specific folder to give future agents folder-scoped context. Use when the user asks to create a CLAUDE.md for a folder, write folder instructions, or add a... | `folder-specific-claude-and-agents-md/SKILL.md` |
| `level-up` | Gauge the user's technical + product knowledge through 7 adaptive questions, log verbatim answers with honest ratings, and grow a learning plan from the gaps found. Use when the user says "level up", "level-up session... | `level-up/SKILL.md` |
| `project-artifact` | Generate and publish a project status artifact — an opinionated, tabbed status page for a project too big for one update (overview & success criteria, the workstream sequence, next steps, plus background, plan, risks... | `project-artifact/SKILL.md` |
| `read-all-adrs` | Read every ADR markdown file in the project's docs/adr/ folder so you have full context on past decisions. Use only when the user explicitly calls it. | `read-all-adrs/SKILL.md` |
| `receipts` | Generate a personal Claude Code usage & impact report ("receipts") from this machine's local session transcripts — for justifying Claude Code usage/spend to a manager, self-review, or "what have I been using this for"... | `receipts/SKILL.md` |
| `scaffold-exercises` | Create exercise directory structures with sections, problems, solutions, and explainers that pass linting. Use when user wants to scaffold exercises, create exercise stubs, or set up a new course section. | `scaffold-exercises/SKILL.md` |
| `session-report` | Generate an explorable HTML report of Claude Code session usage (tokens, cache, subagents, skills, expensive prompts) from ~/.claude/projects transcripts. | `session-report/SKILL.md` |
| `setup-matt-pocock-skills` | Configure this repo for the engineering skills — set up its issue tracker, triage label vocabulary, and domain doc layout. Run once before first use of the other engineering skills. | `setup-matt-pocock-skills/SKILL.md` |
| `teach` | Teach the user a new skill or concept, within this workspace. | `teach/SKILL.md` |
| `writing-for-agents` | Writing documents for agents. Use when creating or editing skills, or modifying AGENTS.md or CLAUDE.md. | `writing-for-agents/SKILL.md` |

## Frontend & Accessibility

| Skill | Description | Path |
|-------|-------------|------|
| `accessibility` | Design, implement, and audit inclusive digital products using WCAG 2.2 Level AA. Use when building or auditing UI that must meet WCAG 2.2 Level AA, or when reviewing a change for keyboard, contrast, or screen-reader s... | `accessibility/SKILL.md` |
| `framer` | Use when the user wants to design, edit, analyze, or publish a website or web page — creating layouts, editing sections, updating text or images, querying site analytics, managing CMS collections and content, syncing... | `framer/SKILL.md` |
| `framer-code-components` | Framer code component implementation guidance, platform constraints, layout annotations, property controls, and authoring best practices. Use only after loading the framer skill and reading the Components row of the g... | `framer-code-components/SKILL.md` |
| `frontend-design` | Guidance for distinctive, intentional visual design when building new UI or reshaping an existing one. Helps with aesthetic direction, typography, and making choices that don't read as templated defaults. | `frontend-design/SKILL.md` |
| `frontend-patterns` | Frontend development patterns for React, Next.js, state management, performance optimization, and UI best practices. Use when building or reviewing React or Next.js components, state, or render performance. | `frontend-patterns/SKILL.md` |
| `playground` | Creates interactive HTML playgrounds — self-contained single-file explorers that let users configure something visually through controls, see a live preview, and copy out a prompt. Use when the user asks to make a pla... | `playground/SKILL.md` |

## Integrations & Automation

| Skill | Description | Path |
|-------|-------------|------|
| `browser-harness` | Direct browser control via CDP. Use when the user wants to automate, scrape, test, or interact with web pages. Connects to the user's already-running Chrome. | `browser-harness/SKILL.md` |
| `cardputer-buddy` | Iterate on the Cardputer-Adv MicroPython app bundle (Claude Buddy, Snake, Hello) after the device is already provisioned via m5-onboard. Use when the user wants to add a new app, push a single changed .py without re-f... | `cardputer-buddy/SKILL.md` |
| `cmux` | Control the cmux macOS terminal app (CLI + socket API) — cmux workspaces, panes, surfaces, browser automation, notifications, settings, hooks. MUST be read before running any `cmux` command. Trigger ONLY when the user... | `cmux/SKILL.md` |
| `create-readonly-db-role` | Provision a hardened SELECT-only Postgres role so AI agents can safely read a production database. Works on Supabase and any Postgres. Use when the user wants agents to query prod data, says "read-only role", "safe pr... | `create-readonly-db-role/SKILL.md` |
| `discord-access` | Manage Discord channel access — approve pairings, edit allowlists, set DM/group policy. Use when the user asks to pair, approve someone, check who's allowed, or change policy for the Discord channel. | `discord-access/SKILL.md` |
| `discord-configure` | Set up the Discord channel — save the bot token and review access policy. Use when the user pastes a Discord bot token, asks to configure Discord, asks "how do I set this up" or "who can reach me," or wants to check c... | `discord-configure/SKILL.md` |
| `git-guardrails-claude-code` | Set up Claude Code hooks to block dangerous git commands (push, reset --hard, clean, branch -D, etc.) before they execute. Use when user wants to prevent destructive git operations, add git safety hooks, or block git... | `git-guardrails-claude-code/SKILL.md` |
| `github-outside-sandbox` | Run Git and GitHub CLI commands through the host context when sandboxing blocks Keychain authentication, network access, or .git writes. Use for gh auth, repository or PR operations, and git index.lock or permission f... | `github-outside-sandbox/SKILL.md` |
| `global-agent-guardrails` | One shared denylist of catastrophic shell commands (rm -rf on / or ~, dd/mkfs, sudo rm, fork bombs, curl\|sh, git push --force, gh repo delete) enforced as a PreToolUse/pre-exec guard across every AI coding agent on t... | `global-agent-guardrails/SKILL.md` |
| `google-safe-browsing` | Prevent and fix Google Safe Browsing "Dangerous site" flags. Use when launching a public web app, buying/picking a domain, building a login or signup page, or when any site shows a red "Dangerous site" / "Deceptive si... | `google-safe-browsing/SKILL.md` |
| `imessage-access` | Manage iMessage channel access — approve pairings, edit allowlists, set DM/group policy. Use when the user asks to pair, approve someone, check who's allowed, or change policy for the iMessage channel. | `imessage-access/SKILL.md` |
| `imessage-configure` | Check iMessage channel setup and review access policy. Use when the user asks to configure iMessage, asks "how do I set this up" or "who can reach me," or wants to know why texts aren't reaching the assistant. | `imessage-configure/SKILL.md` |
| `m5-onboard` | End-to-end onboarding for a freshly-plugged-in M5Stack ESP32 device (Cardputer, Cardputer-Adv, Core, CoreS3, Stick) — detect on USB, flash UIFlow 2.0 firmware, and install the Claude Buddy MicroPython app bundle. Use... | `m5-onboard/SKILL.md` |
| `macbook-metrics-setup` | Replicate the macbook-metrics setup on any Mac — a local, always-on system-metrics collector (CPU, GPU, RAM, disk, network, battery, thermals) built as a Swift CLI, run by launchd every 60s, stored in SQLite, and back... | `macbook-metrics-setup/SKILL.md` |
| `nuke-cursor-app` | End-to-end Cursor IDE restart on the user's MacBook: snapshot metrics, kill ALL Cursor processes, relaunch Cursor, report before/after memory. Recovers from the known renderer memory leak that makes Cursor lag. Manual... | `nuke-cursor-app/SKILL.md` |
| `prod-push` | Push to GitHub main and babysit the change until it is verifiably live in production, fixing CI and deploy failures along the way. Use when the user says "push", "push to github", "push to prod", "ship it", or "deploy... | `prod-push/SKILL.md` |
| `push-skill-to-github` | Commit and push agent-skill changes to the user's private skills GitHub repo (private-skills-repo, rooted at ~/.agents). Use after creating or updating any skill, when the user says "push the skill", "push skills to g... | `push-skill-to-github/SKILL.md` |
| `read-prod-database` | Query the production Supabase Postgres read-only via psql using the SELECT-only agents_readonly role. Use when debugging prod issues, investigating a user report, checking real usage/billing/retention numbers, or veri... | `read-prod-database/SKILL.md` |
| `remove-ai-marks` | Remove multi-vendor AI provenance marks: invisible Unicode (Layer A), statistical text watermarks via rewrite (Layer B, always offer), and C2PA/EXIF/XMP/container metadata on PNG/JPEG/SVG/PDF/DOCX/ODT/HTML/MD. Covers... | `remove-ai-marks/SKILL.md` |
| `telegram-access` | Manage Telegram channel access — approve pairings, edit allowlists, set DM/group policy. Use when the user asks to pair, approve someone, check who's allowed, or change policy for the Telegram channel. | `telegram-access/SKILL.md` |
| `telegram-configure` | Set up the Telegram channel — save the bot token and review access policy. Use when the user pastes a Telegram bot token, asks to configure Telegram, asks "how do I set this up" or "who can reach me," or wants to chec... | `telegram-configure/SKILL.md` |
| `wizard` | Generate an interactive bash wizard that walks a human through steps only they can perform. Use when provisioning infrastructure, setting up credentials or CI secrets, walking an unfamiliar third-party dashboard, or r... | `wizard/SKILL.md` |

## Output & Communication Style

| Skill | Description | Path |
|-------|-------------|------|
| `adhd` | Shape output for a reader with ADHD: lead with the next action, number multi-step work, restate state across turns, suppress tangents, give specific time estimates, make wins visible. Invoke with /adhd; stays on until... | `adhd/SKILL.md` |
| `adhd1` | Always-on ADHD output shaping: lead with the next action, number multi-step work, restate state across turns, suppress tangents, give specific time estimates, make wins visible. Applies by default to every response in... | `adhd1/SKILL.md` |
| `btw` | Manually-invoked side-question mode — answer a quick tangential question without disturbing the main task. Use when the user says "btw", "quick question", "side question", or asks something unrelated mid-task. | `btw/SKILL.md` |
| `caveman` | Ultra-compressed communication mode. Cuts output tokens 65% (measured) by speaking like caveman while keeping full technical accuracy. Supports intensity levels: lite, full (default), ultra, wenyan-lite, wenyan-full,... | `caveman/SKILL.md` |
| `caveman-commit` | Ultra-compressed commit message generator. Cuts noise from commit messages while preserving intent and reasoning. Conventional Commits format. Subject ≤50 chars, body only when "why" isn't obvious. Use when user says... | `caveman-commit/SKILL.md` |
| `caveman-compress` | Compress natural language memory files (CLAUDE.md, todos, preferences) into caveman format to save input tokens. Preserves all technical substance, code, URLs, and structure. Compressed version overwrites the original... | `caveman-compress/SKILL.md` |
| `caveman-discover` | Find every LLM workflow in the current repository and label it, so Caveman Cloud groups spend by what the code actually does (support-reply, nightly-digest) instead of one anonymous bucket. Use when the user pastes th... | `caveman-discover/SKILL.md` |
| `caveman-evidence-review` | Review Caveman Cloud evidence read-only: costs, Cave Score, Cave Plan, workflows, traces, latency, errors, compression, routing, and verified savings. Use when the user asks what Caveman found, where LLM spend goes, w... | `caveman-evidence-review/SKILL.md` |
| `caveman-explore` | Read-only repository explorer. Use PROACTIVELY for cold-start exploration, broad cross-file localization, or when a direct search has failed and you need to find where something lives. Skip it when the issue already n... | `caveman-explore/SKILL.md` |
| `caveman-help` | Quick-reference card for all caveman modes, skills, and commands. One-shot display, not a persistent mode. Trigger: /caveman-help, "caveman help", "what caveman commands", "how do I use caveman". | `caveman-help/SKILL.md` |
| `caveman-learn` | Close the loop on a Caveman learn report — review the ranked token sinks and apply cost-lowering fixes (trim config, offload recurring context to cavemem) with per-edit consent. Use when the user runs "caveman learn",... | `caveman-learn/SKILL.md` |
| `caveman-manage` | Inspect Caveman Cloud's eval-gated experiment lifecycle and block unsafe execution. Use when the user asks to start, approve, cancel, promote, or roll back a Caveman experiment, or asks what action an experiment's evi... | `caveman-manage/SKILL.md` |
| `caveman-optimize` | Turn Caveman's exact report-only repository observations into an operator-chosen optimization candidate with a paired baseline/candidate evaluation. Use when the user asks to inspect an optimization observation, evalu... | `caveman-optimize/SKILL.md` |
| `caveman-review` | Ultra-compressed code review comments. Cuts noise from PR feedback while preserving the actionable signal. Each comment is one line: location, problem, fix. Use when user says "review this PR", "code review", "review... | `caveman-review/SKILL.md` |
| `caveman-setup` | Wire the current repository through the Caveman Cloud gateway so every LLM request is measured — cost, tokens, latency — with zero behavior change. Use when the user pastes the Caveman setup prompt, says "set up cavem... | `caveman-setup/SKILL.md` |
| `caveman-stats` | Show real token usage and estimated savings for the current session. Reads directly from the Claude Code session log — no AI estimation. Triggers on /caveman-stats. Output is injected by the mode-tracker hook; the mod... | `caveman-stats/SKILL.md` |
| `ghost` | Give direct, fast answers: lead with the answer, no preamble, no recap, no filler, no polite ceremony, no re-explaining the problem back. Same work, about a quarter fewer words. Use when the user wants a straight answ... | `ghost/SKILL.md` |
| `remind` | Rewrite the last response simpler and shorter in plain English, prefixed with a 3-5 sentence TLDR of the conversation so far. Manual-only, invoked as /remind. | `remind/SKILL.md` |
| `short` | Manually-invoked skill that forces the agent to compress its current answer — strip filler, simplify wording, and cut length while keeping the substance. Use when the user says "short", "shorter", "simpler", "too long... | `short/SKILL.md` |
| `stop-overthinking` | Manually-invoked skill that stops overthinking and forces a short, practical decision. Use only when the user explicitly invokes stop-overthinking. | `stop-overthinking/SKILL.md` |
| `wait-what` | Stop. That last message did not land — re-pitch it. | `wait-what/SKILL.md` |

## Research & Analysis

| Skill | Description | Path |
|-------|-------------|------|
| `deep-research` | Run a deep, source-backed research query via DeepAPI (go to deepapi.co to get an API key) POST /v1/research/deep. Builds a rigorous one-paragraph research prompt (per research-prompt rules), fires it, and saves a cite... | `deep-research/SKILL.md` |
| `deepapi` | Use DeepAPI for all regular web searches (POST /v1/search/web) and for any deep research you perform (POST /v1/research/deep), instead of built-in search or research tools. Use it for all scraping of the web (websites... | `deepapi/SKILL.md` |
| `fireflies-transcript` | Pull raw meeting transcripts from David's Fireflies.ai notetaker via its GraphQL API, using the key saved globally on this MacBook. Use when the user wants a call transcript, meeting notes, "what was said on the call"... | `fireflies-transcript/SKILL.md` |
| `math-olympiad` | Solve competition math problems (IMO, Putnam, USAMO, AIME) with adversarial verification that catches the errors self-verification misses. Activates when asked to 'solve this IMO problem', 'prove this olympiad inequal... | `math-olympiad/SKILL.md` |
| `monid` | Discover better ways to complete tasks. Proactively run `monid discover` before writing a scraper, before using a generic web fetch for structured data, or before telling the user something is inaccessible — and whene... | `monid/SKILL.md` |
| `online-shopping` | Research any online purchase with DeepAPI — fair-price checks, best deals, where to buy, shop trust. Load whenever the user is shopping or buying anything online: mentions buying a product, comparing prices, "is this... | `online-shopping/SKILL.md` |
| `pi-web-search` | ONLY for Pi Agents — all other agents have their own web tools. How Pi accesses the web via the pi-web-access package — search, fetch URLs/PDFs/YouTube/GitHub. Use whenever a Pi task needs current info, docs, news, pr... | `pi-web-search/SKILL.md` |
| `research` | Investigate a question against high-trust primary sources and capture the findings as a Markdown file in the repo. Use when the user wants a topic researched, docs or API facts gathered, or reading legwork delegated t... | `research/SKILL.md` |
| `research-prompt` | Write a single-paragraph Deep Research prompt to hand to a human researcher (or a deep-research AI). Use when the user wants a research brief, a "deep research prompt", a one-paragraph task for a researcher, or asks "... | `research-prompt/SKILL.md` |
| `run-deep-swe` | Score any AI model on the DeepSWE coding-agent benchmark via the OpenRouter API. Use when the user wants an independent, reproducible coding-agent eval — "run DeepSWE", "benchmark this model on DeepSWE", "score model... | `run-deep-swe/SKILL.md` |
| `youtube-transcript` | Use whenever the user needs the transcript of a YouTube video — fetching, extracting, downloading, or pulling captions/subtitles/transcript text from a YouTube URL. Triggers on "get the transcript", "transcript of thi... | `youtube-transcript/SKILL.md` |

## Security & Red Teaming

| Skill | Description | Path |
|-------|-------------|------|
| `auditme` | Umbrella router for the auditme offensive-security library. Points to the right offensive-* skill (web, wireless, cloud, recon, exploit-dev, AD, mobile, IoT, fuzzing, reporting) for a red-team or pentest task, and to... | `auditme/SKILL.md` |
| `claude-security` | The Claude Security menu — pick a job: scan the codebase (the whole repository or a scoped part of it), scan changes (this branch's or a pull request's diff, or one commit), or suggest patches (findings turned into ta... | `claude-security/SKILL.md` |
| `offensive-active-directory` | Active Directory attack methodology for internal network red team engagements. Covers reconnaissance (BloodHound, PowerView, ADExplorer), credential abuse (Kerberoasting, ASREProasting, NTLM relay, LLMNR/NBT-NS poison... | `auditme/claude-red-review/active-directory/offensive-active-directory/SKILL.md` |
| `offensive-advanced-redteam` | Advanced Redteam Ops: Practical advanced red team operations guide: OPSEC discipline, C2 infrastructure design, living-off-the-land techniques, lateral movement, persistence, data exfiltration, and evading modern defe... | `auditme/claude-red-review/infrastructure/offensive-advanced-redteam/SKILL.md` |
| `offensive-ai-security` | AI Pentest: AI/LLM security offensive checklist: prompt injection, jailbreaking, model extraction, training data poisoning, adversarial inputs, LLM-assisted attack automation, and AI system reconnaissance. Use when as... | `auditme/claude-red-review/ai/offensive-ai-security/SKILL.md` |
| `offensive-basic-exploitation` | Week 5: Basic Exploitation (Linux with Mitigations Disabled): Week 5 exploit development curriculum. Foundational exploitation techniques: controlling EIP/RIP, ROP chain construction, ret2libc, shellcode injection, he... | `auditme/claude-red-review/exploit-dev/offensive-basic-exploitation/SKILL.md` |
| `offensive-bluetooth-ble` | Bluetooth Low Energy (BLE) attack methodology — GATT enumeration, characteristic read/write without auth, pairing downgrade (Just Works forced), LE Secure Connections bypass, MITM via active relay, sniffing with Sniff... | `auditme/claude-red-review/wireless/offensive-bluetooth-ble/SKILL.md` |
| `offensive-bluetooth-classic` | Bluetooth Classic (BR/EDR) attack methodology — device discovery, service enumeration via SDP, LMP/L2CAP layer attacks, legacy PIN cracking (BlueBorne / KNOB), Bluetooth file-transfer abuse (BlueSnarfing legacy), unau... | `auditme/claude-red-review/wireless/offensive-bluetooth-classic/SKILL.md` |
| `offensive-bug-identification` | Bug Identification: Systematic bug identification methodology: source code review patterns, black-box testing strategies, taint analysis, dangerous function hunting, data flow tracing, and automated scanning setup. Us... | `auditme/claude-red-review/fuzzing/offensive-bug-identification/SKILL.md` |
| `offensive-business-logic` | Business logic vulnerability testing for web/mobile/API engagements. Covers workflow bypass, state machine violations, multi-step process abuse, price/quantity/discount manipulation, currency confusion, coupon stackin... | `auditme/claude-red-review/web/offensive-business-logic/SKILL.md` |
| `offensive-cloud` | Cloud security attack methodology covering AWS, Azure, and GCP. Includes credential harvesting (IMDS, ~/.aws, env vars, leaked CI secrets, instance roles), enumeration with cloud-specific tools (pacu, ScoutSuite, Prow... | `auditme/claude-red-review/cloud/offensive-cloud/SKILL.md` |
| `offensive-crash-analysis` | Week 4: Crash Analysis and Exploitability Assessment: Week 4 exploit development curriculum. Crash triage and analysis methodology: WinDbg/GDB analysis, ASAN/MSAN output interpretation, exploitability assessment, regi... | `auditme/claude-red-review/exploit-dev/offensive-crash-analysis/SKILL.md` |
| `offensive-deauth-disassoc` | Deauthentication and disassociation attacks against 802.11 networks — targeted single-client deauth for handshake capture, broadcast deauth for DoS (with authorization), action-frame attacks bypassing 802.11w (PMF), b... | `auditme/claude-red-review/wireless/offensive-deauth-disassoc/SKILL.md` |
| `offensive-deserialization` | Insecure Deserialization: Insecure deserialization attack checklist: identifying deserialization sinks, Java/PHP/.NET/Python deserialization exploitation, ysoserial gadget chains, magic method abuse, and detection eva... | `auditme/claude-red-review/web/offensive-deserialization/SKILL.md` |
| `offensive-edr-evasion` | Endpoint Detection and Response: EDR evasion offensive checklist: hook unhooking (user/kernel), direct syscalls, PPID spoofing, process injection variants, AMSI bypass, ETW patching, memory encryption, and behavior-ba... | `auditme/claude-red-review/infrastructure/offensive-edr-evasion/SKILL.md` |
| `offensive-evil-twin` | Evil Twin / KARMA / Mana access point methodology — rogue AP construction with hostapd-mana / wifiphisher / airgeddon, KARMA universal probe response, Mana selective probe response, captive portal phishing, deauth-dri... | `auditme/claude-red-review/wireless/offensive-evil-twin/SKILL.md` |
| `offensive-exploit-dev-course` | Exploit Development: Full exploit development course roadmap and syllabus: weekly topics, recommended reading, lab setup, and learning path from vulnerability classes through advanced exploitation. Use to structure ex... | `auditme/claude-red-review/exploit-dev/offensive-exploit-dev-course/SKILL.md` |
| `offensive-exploit-development` | Exploit Development: Exploit development operational guide: environment setup, debugging workflow, PoC development lifecycle, writing reliable exploits, using pwntools/pwndbg, heap exploitation techniques, and weaponi... | `auditme/claude-red-review/exploit-dev/offensive-exploit-development/SKILL.md` |
| `offensive-fast-checking` | Fast Testing Checklist: Speed-optimized offensive checklist for rapid assessment: quick-win vulnerability patterns, fast recon shortcuts, automated scanner configurations, and triage shortcuts. Use for time-boxed asse... | `auditme/claude-red-review/utility/offensive-fast-checking/SKILL.md` |
| `offensive-fuzzing` | Practical offensive fuzzing methodology covering target identification, fuzzer selection (AFL++, libFuzzer, Honggfuzz, Boofuzz, syzkaller), harness writing, corpus curation, mutation strategies, coverage measurement,... | `auditme/claude-red-review/fuzzing/offensive-fuzzing/SKILL.md` |
| `offensive-fuzzing-course` | Week 2: Finding Vulnerabilities Through Fuzzing: Week 2 of the exploit development curriculum. Covers fuzzing methodology: target selection, corpus generation, coverage-guided fuzzing with AFL++/libFuzzer, structured... | `auditme/claude-red-review/fuzzing/offensive-fuzzing-course/SKILL.md` |
| `offensive-graphql` | GraphQL Vulnerabilities: GraphQL security testing checklist: introspection abuse, batching attacks, query depth/complexity DoS, field suggestion enumeration, IDOR via GraphQL, injection through arguments, authorizatio... | `auditme/claude-red-review/web/offensive-graphql/SKILL.md` |
| `offensive-idor` | Insecure Direct Object References (IDOR): IDOR (Insecure Direct Object Reference) testing checklist: object ID enumeration, horizontal/vertical privilege escalation, GUID predictability, indirect references via hashes... | `auditme/claude-red-review/web/offensive-idor/SKILL.md` |
| `offensive-initial-access` | Modern Initial Access: Initial access techniques checklist: phishing (spear/smishing), credential stuffing, exposed service exploitation, supply chain attacks, watering hole, VPN/RDP brute force, public-facing applica... | `auditme/claude-red-review/infrastructure/offensive-initial-access/SKILL.md` |
| `offensive-iot` | IoT and embedded device security testing methodology. Covers hardware reconnaissance (UART, JTAG, SWD, SPI flash, I2C EEPROM, eMMC chip-off), firmware acquisition (vendor portals, OTA capture, flash dump, binwalk extr... | `auditme/claude-red-review/iot/offensive-iot/SKILL.md` |
| `offensive-jwt` | JWT attack methodology for penetration testers. Covers algorithm confusion (alg:none, RS256→HS256), weak HMAC secret brute force, kid parameter injection (SQLi, path traversal), jku/x5u/jwk header injection, JWKS cach... | `auditme/claude-red-review/auth/offensive-jwt/SKILL.md` |
| `offensive-keylogger-arch` | Novel research: Low-level keylogger architecture design: kernel driver hooks (WH_KEYBOARD_LL, SetWindowsHookEx), ETW-based input capture, user-mode vs kernel-mode approaches, stealth techniques, and data exfiltration.... | `auditme/claude-red-review/infrastructure/offensive-keylogger-arch/SKILL.md` |
| `offensive-krack-fragattacks` | KRACK (CVE-2017-13077..082) and FragAttacks (CVE-2020-24586..588 + 26139-26147) — key reinstallation, fragmentation, and aggregation attacks against WPA2 supplicants. Covers Vanhoef's test scripts, viability against m... | `auditme/claude-red-review/wireless/offensive-krack-fragattacks/SKILL.md` |
| `offensive-lorawan-sub-ghz` | LoRaWAN and sub-GHz (433 / 868 / 915 MHz) attack methodology — LoRaWAN ABP/OTAA join attack, network/session key reuse, frame counter replay, downlink injection on TTN/Helium-style networks, sub-GHz protocol replay (K... | `auditme/claude-red-review/wireless/offensive-lorawan-sub-ghz/SKILL.md` |
| `offensive-mitigations` | Modern Kernel Exploit Mitigations: Security mitigation reference and bypass catalog: ASLR, DEP/NX, RELRO, stack canaries, CFI, sandboxing, seccomp. Covers both detection of enabled mitigations and known bypass techniq... | `auditme/claude-red-review/exploit-dev/offensive-mitigations/SKILL.md` |
| `offensive-mobile` | Mobile (Android + iOS) application penetration testing methodology. Covers static analysis (apktool/jadx for Android, class-dump/Hopper/IDA for iOS), dynamic instrumentation with Frida and Objection, SSL pinning bypas... | `auditme/claude-red-review/mobile/offensive-mobile/SKILL.md` |
| `offensive-oauth` | OAuth Security Testing: OAuth 2.0 attack checklist: authorization code interception, redirect_uri bypass, CSRF on OAuth flow, state parameter abuse, open redirector chaining, token leakage via Referer, PKCE bypass, an... | `auditme/claude-red-review/auth/offensive-oauth/SKILL.md` |
| `offensive-open-redirect` | Open Redirect Vulnerabilities: Open redirect vulnerability checklist: parameter identification, bypass techniques (URL encoding, double slashes, CRLF injection, protocol handlers), chaining with OAuth/SSRF, and impact... | `auditme/claude-red-review/web/offensive-open-redirect/SKILL.md` |
| `offensive-osint` | Comprehensive OSINT methodology skill for offensive security, red team intelligence gathering, and bug bounty reconnaissance. Covers domain recon, email harvesting, social media profiling, GitHub/code leaks, Shodan/Ce... | `auditme/claude-red-review/recon/offensive-osint/SKILL.md` |
| `offensive-osint-methodology` | OSINT Methodology: Structured OSINT methodology framework: target definition, source selection, collection workflows, data correlation, timeline reconstruction, and reporting. Use to guide systematic OSINT campaigns o... | `auditme/claude-red-review/recon/offensive-osint-methodology/SKILL.md` |
| `offensive-parameter-pollution` | HTTP Parameter Pollution (HPP): HTTP parameter pollution (HPP) checklist: duplicate parameter injection, backend vs frontend parsing differences, WAF bypass via HPP, server-side vs client-side HPP, and practical explo... | `auditme/claude-red-review/web/offensive-parameter-pollution/SKILL.md` |
| `offensive-race-condition` | Race Conditions: Race condition (TOCTOU) testing checklist: identifying timing windows, Burp Suite Turbo Intruder, Last-Byte sync technique, rate limit bypass, double-spend attacks, and concurrent request exploitation... | `auditme/claude-red-review/web/offensive-race-condition/SKILL.md` |
| `offensive-reporting` | Penetration test and red team report writing methodology. Covers executive summary structuring (risk-led narrative for non-technical readers), technical finding format (title, severity, affected scope, narrative, repr... | `auditme/claude-red-review/utility/offensive-reporting/SKILL.md` |
| `offensive-request-smuggling` | HTTP Request Smuggling: HTTP request smuggling checklist: CL.TE, TE.CL, TE.TE variants, detection with timing and differential responses, WAF bypass, cache poisoning, credential hijacking, and request smuggling via HT... | `auditme/claude-red-review/web/offensive-request-smuggling/SKILL.md` |
| `offensive-shellcode` | Shellcode development reference for offensive security engagements. Use when writing custom x86/x64 shellcode, implementing position-independent code (PIC), building shellcode loaders, evading AV/EDR detection, or con... | `auditme/claude-red-review/infrastructure/offensive-shellcode/SKILL.md` |
| `offensive-ssrf` | Server-Side Request Forgery (SSRF): Server-Side Request Forgery testing checklist: SSRF discovery, blind SSRF with out-of-band, cloud metadata endpoints (AWS/GCP/Azure), SSRF filter bypass techniques (IP encoding, DNS... | `auditme/claude-red-review/web/offensive-ssrf/SKILL.md` |
| `offensive-ssti` | Server-Side Template Injection (SSTI): Server-Side Template Injection testing checklist: template engine identification (Jinja2, Twig, Freemarker, Pebble, Velocity), polyglot detection payloads, engine-specific RCE pa... | `auditme/claude-red-review/web/offensive-ssti/SKILL.md` |
| `offensive-toctou` | Time-of-Check / Time-of-Use (TOCTOU) race condition exploitation methodology across binary, kernel, filesystem, web, and container layers. Covers symbolic-link races (open/access/stat split), file-descriptor races, fo... | `auditme/claude-red-review/exploit-dev/offensive-toctou/SKILL.md` |
| `offensive-vuln-classes` | Week 1: Vulnerability Classes with Real-World Examples: Exploit development curriculum covering core vulnerability classes with real-world CVE case studies: stack/heap buffer overflows, use-after-free, integer overflo... | `auditme/claude-red-review/fuzzing/offensive-vuln-classes/SKILL.md` |
| `offensive-waf-bypass` | WAF Bypass Techniques: WAF bypass techniques checklist: encoding bypass (URL/HTML/Unicode/double encoding), case variation, comment injection, HTTP header manipulation, chunked encoding, IP rotation, timing attacks, a... | `auditme/claude-red-review/web/offensive-waf-bypass/SKILL.md` |
| `offensive-wifi` | Wireless / 802.11 attack methodology for red team engagements and wireless security assessments. Covers monitor-mode setup, WPA/WPA2-PSK handshake capture and PMKID attacks, WPA3 SAE downgrade and Dragonblood, WPA-Ent... | `auditme/claude-red-review/wireless/offensive-wifi/SKILL.md` |
| `offensive-wifi-recon` | Wi-Fi reconnaissance methodology — adapter selection, monitor mode and packet injection setup, regulatory domain handling, multi-band airspace mapping, hidden SSID discovery, BSSID/ESSID/channel/PMF/encryption fingerp... | `auditme/claude-red-review/wireless/offensive-wifi-recon/SKILL.md` |
| `offensive-windows-boundaries` | Week 7: Defeating Windows Security Boundaries: Windows security boundary taxonomy and attack surface enumeration: kernel/user boundary, sandbox boundaries (LPAC, AppContainer), COM/RPC boundaries, hypervisor boundary,... | `auditme/claude-red-review/infrastructure/offensive-windows-boundaries/SKILL.md` |
| `offensive-windows-mitigations` | Week 6: Understanding Windows Mitigations: Deep-dive on Windows exploit mitigations: ASLR, DEP/NX, CFG, CET/Shadow Stack, SEHOP, Heap Guard, ACG, Arbitrary Code Guard. Covers both the protection mechanism and known by... | `auditme/claude-red-review/infrastructure/offensive-windows-mitigations/SKILL.md` |
| `offensive-wpa-enterprise` | WPA/WPA2/WPA3-Enterprise (802.1X / EAP) attack methodology — EAP method identification (PEAP-MSCHAPv2, EAP-TTLS, EAP-TLS, EAP-GTC, EAP-PWD, EAP-FAST), evil-twin RADIUS attacks with eaphammer for credential capture, MS... | `auditme/claude-red-review/wireless/offensive-wpa-enterprise/SKILL.md` |
| `offensive-wpa2-psk` | WPA/WPA2-PSK attack methodology — four-way handshake capture via targeted deauthentication, PMKID attacks (no client required), hcxdumptool / hcxpcapngtool conversion to hashcat hc22000 format, GPU-accelerated crackin... | `auditme/claude-red-review/wireless/offensive-wpa2-psk/SKILL.md` |
| `offensive-wpa3-sae` | WPA3 / SAE (Simultaneous Authentication of Equals) attack methodology — transition-mode (mixed WPA2/WPA3) downgrade, Dragonblood side-channel attacks (CVE-2019-9494, 9495, 13377, 13456), SAE auth flooding for AP CPU e... | `auditme/claude-red-review/wireless/offensive-wpa3-sae/SKILL.md` |
| `offensive-wps` | WPS (Wi-Fi Protected Setup) PIN attack methodology — Pixie Dust offline attack against vulnerable chipsets (Ralink, Realtek, Broadcom, MediaTek), online PIN brute-force with reaver/bully, lockout handling, time-of-day... | `auditme/claude-red-review/wireless/offensive-wps/SKILL.md` |
| `offensive-xss` | Cross-Site Scripting (XSS): Cross-Site Scripting testing checklist: stored/reflected/DOM/blind XSS discovery, polyglot payloads, CSP bypass, XSS filter bypass, event handler injection, DOM clobbering, mutation XSS, an... | `auditme/claude-red-review/web/offensive-xss/SKILL.md` |
| `offensive-xxe` | XML External Entity (XXE) Injection: XML External Entity injection testing checklist: classic XXE, blind XXE (out-of-band), XXE via file upload (SVG/docx), XXE in SOAP/REST, error-based XXE, XInclude attacks, and XXE... | `auditme/claude-red-review/web/offensive-xxe/SKILL.md` |
| `offensive-z-wave` | Z-Wave attack methodology — sniffing with Z-Force / EZ-Wave / RTL-SDR + ZniffMobile, S0 (legacy) network-key derivation flaw and key reuse, S2 (modern) ECDH commissioning analysis, replay/injection on unauthenticated... | `auditme/claude-red-review/wireless/offensive-z-wave/SKILL.md` |
| `offensive-zigbee-thread-matter` | Zigbee, Thread, and Matter mesh-protocol attack methodology — IEEE 802.15.4 sniffing with TI CC2531 / CC2540 / Sonoff Zigbee Dongle E, KillerBee toolkit, Touchlink commissioning abuse with the well-known transport key... | `auditme/claude-red-review/wireless/offensive-zigbee-thread-matter/SKILL.md` |
| `security-audit` | Performs an exhaustive, adversarial, multi-pass security audit of web apps — HTML/JS/CSS, IndexedDB/localStorage, WebRTC/P2P/STUN/TURN, PWA/Service Worker, WebView/Electron/Tauri, CSP & security headers, auth/session/... | `security-audit/SKILL.md` |

## Software Engineering

| Skill | Description | Path |
|-------|-------------|------|
| `code-review` | Review the changes since a fixed point (commit, branch, tag, or merge-base) along two axes — Standards (does the code follow this repo's documented coding standards?) and Spec (does the code match what the originating... | `code-review/SKILL.md` |
| `codebase-design` | Shared vocabulary for designing deep modules. Use when the user wants to design or improve a module's interface, find deepening opportunities, decide where a seam goes, make code more testable or AI-navigable, or when... | `codebase-design/SKILL.md` |
| `diagnosing-bugs` | Diagnosis loop for hard bugs and performance regressions. Use when the user says "diagnose"/"debug this", or reports something broken/throwing/failing/slow. | `diagnosing-bugs/SKILL.md` |
| `git-worktree` | Use git worktrees to run multiple coding agents in parallel on one repo without collisions. Use when starting a task in a shared repo, when the user says "worktree", "parallel agents", "one worktree per task", or when... | `git-worktree/SKILL.md` |
| `implement` | Implement a piece of work based on a spec or set of tickets. | `implement/SKILL.md` |
| `improve-codebase-architecture` | Scan a codebase for deepening opportunities, present them as a visual HTML report, then grill through whichever one you pick. | `improve-codebase-architecture/SKILL.md` |
| `investigate-first` | Diagnose ambiguous failures before editing. Use for unknown causes, intermittent behavior, performance regressions, or investigations needing evidence-ranked hypotheses. | `investigate-first/SKILL.md` |
| `lean-build` | Build feature work with high overbuilding risk. Use for new behavior, product slices, or integrations where repository reuse, strict scope, and an explicit stop condition matter. | `lean-build/SKILL.md` |
| `migrate-to-shoehorn` | Migrate test files from `as` type assertions to @total-typescript/shoehorn. Use when user mentions shoehorn, wants to replace `as` in tests, or needs partial test data. | `migrate-to-shoehorn/SKILL.md` |
| `migration` | Implement reversible compatibility-safe transitions. Use for schema, data, API, protocol, configuration, or dependency migrations requiring rollback and preservation proof. | `migration/SKILL.md` |
| `ponytail` | Forces the laziest solution that actually works, simplest, shortest, most minimal. Channels a senior dev who has seen everything: question whether the task needs to exist at all (YAGNI), reach for the standard library... | `ponytail/SKILL.md` |
| `ponytail-audit` | Whole-repo audit for over-engineering. Like ponytail-review, but scans the entire codebase instead of a diff: a ranked list of what to delete, simplify, or replace with stdlib/native equivalents. Use when the user say... | `ponytail-audit/SKILL.md` |
| `ponytail-debt` | Harvest every `ponytail:` comment in the codebase into a debt ledger, so the deliberate shortcuts and deferrals ponytail leaves behind get tracked instead of rotting into "later means never". Use when the user says "p... | `ponytail-debt/SKILL.md` |
| `ponytail-gain` | Show ponytail's measured impact as a compact scoreboard: less code, less cost, more speed, from the benchmark medians. One-shot display, not a persistent mode, and not a per-repo number. Trigger: /ponytail-gain, "pony... | `ponytail-gain/SKILL.md` |
| `ponytail-help` | Quick-reference card for all ponytail modes, skills, and commands. One-shot display, not a persistent mode. Trigger: /ponytail-help, "ponytail help", "what ponytail commands", "how do I use ponytail". | `ponytail-help/SKILL.md` |
| `ponytail-review` | Code review focused exclusively on over-engineering. Finds what to delete: reinvented standard library, unneeded dependencies, speculative abstractions, dead flexibility. One line per finding: location, what to cut, w... | `ponytail-review/SKILL.md` |
| `prototype` | Build a throwaway prototype to answer a design question. Use when the user wants to sanity-check whether a state model or logic feels right, or explore what a UI should look like. | `prototype/SKILL.md` |
| `resolving-merge-conflicts` | Use when you need to resolve an in-progress git merge/rebase conflict. | `resolving-merge-conflicts/SKILL.md` |
| `safe-refactor` | Restructure code while preserving behavior. Use for extraction, consolidation, ownership moves, or cleanup where verification must bracket structural edits. | `safe-refactor/SKILL.md` |
| `setup-pre-commit` | Set up Husky pre-commit hooks with lint-staged (Prettier), type checking, and tests in the current repo. Use when user wants to add pre-commit hooks, set up Husky, configure lint-staged, or add commit-time formatting/... | `setup-pre-commit/SKILL.md` |
| `surgical-patch` | Fix bugs and small behavior changes at the narrowest responsible layer. Use when regression proof, preserved surrounding behavior, and task-relevant tests matter. | `surgical-patch/SKILL.md` |
| `tdd` | Test-driven development. Use when the user wants to build features or fix bugs test-first, mentions "red-green-refactor", or wants integration tests. | `tdd/SKILL.md` |
| `verify-and-stop` | Prove existing work meets acceptance conditions without expanding scope. Use for validation-only tasks, completion checks, focused gate runs, and last-mile proof. | `verify-and-stop/SKILL.md` |

## Workflow & Collaboration

| Skill | Description | Path |
|-------|-------------|------|
| `ask-matt` | Ask which skill or flow fits your situation. A router over the skills in this repo. | `ask-matt/SKILL.md` |
| `ask-then-build` | Scope a feature, change, or refactor by asking the user 3-6 pointed questions ONE at a time (options A-D, state a preference, wait), record every answer, then deliver ONE concise paragraph prompt that another agent ca... | `ask-then-build/SKILL.md` |
| `before-building` | Fire the moment the user proposes a build. Instantly surface the 1-3 consequential choices hidden in his idea. Can also be invoked with /before-building. | `before-building/SKILL.md` |
| `decisions` | Ask the agent to list all choices it made during the current work that it is not confident of. Manual-only; invoke with /decisions. | `decisions/SKILL.md` |
| `grill-me` | A relentless interview to sharpen a plan or design. | `grill-me/SKILL.md` |
| `grill-with-docs` | A relentless interview to sharpen a plan or design, which also creates docs (ADR's and glossary) as we go. | `grill-with-docs/SKILL.md` |
| `grilling` | Grill the user relentlessly about a plan, decision, or idea. Use when the user wants to stress-test their thinking, or uses any 'grill' trigger phrases. | `grilling/SKILL.md` |
| `handoff` | Compact the current conversation into a handoff document for another agent to pick up. | `handoff/SKILL.md` |
| `next-decision` | Drill open decisions one at a time — present the most important decision not yet clarified, give the top four choices, state a preference, ask the user. Use when the user says "next decision", "one decision at a time"... | `next-decision/SKILL.md` |
| `prompt-me` | Prompt the user with pointed questions to extract what is in his head about a project — remaining work, what is being avoided, what really matters, what does not. Use when the user says "prompt me", "ask me questions"... | `prompt-me/SKILL.md` |
| `setup-help` | Walk the user through setting up anything step by step. Use when the user asks for help setting up, configuring, installing, or getting something working — "help me set up X", "walk me through this", "setup-help". Dif... | `setup-help/SKILL.md` |
| `to-questionnaire` | Turn a decision you can't fully answer into a questionnaire for someone else to fill in. | `to-questionnaire/SKILL.md` |
| `to-spec` | Turn the current conversation into a spec and publish it to the project issue tracker — no interview, just synthesis of what you've already discussed. | `to-spec/SKILL.md` |
| `to-tickets` | Break a plan, spec, or the current conversation into a set of tracer-bullet tickets, each declaring its blocking edges, published to the configured tracker — edges as text in one file per ticket locally, or native blo... | `to-tickets/SKILL.md` |
| `triage` | Move issues and external PRs through a state machine of triage roles — categorise, verify, grill if needed, and write agent-ready briefs. | `triage/SKILL.md` |
| `unlazy` | Anti-laziness execution discipline for substantial tasks. Use when work keeps coming back half done, when an agent reports done before it is done, when output must be exhaustive rather than fast, on long autonomous ru... | `unlazy/SKILL.md` |
| `wayfinder` | Plan a huge chunk of work — more than one agent session can hold — as a shared map of decision tickets on your issue tracker, and resolve them one at a time until the way to the destination is clear. | `wayfinder/SKILL.md` |

---

## Regenerating this catalog

```bash
python scripts/generate_catalog.py
```

</div>
