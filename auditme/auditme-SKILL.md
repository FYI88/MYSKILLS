---
name: auditme
description: "Combined adversarial security audit. One command that runs BOTH the defensive audit (grep blitz, WSTG-mapped checklist, live-browser verification, fixes, findings.json) AND the offensive attack pass (claude-red exploitation skills matched to the target). ALWAYS use when the user invokes /auditme, or asks to 'audit', 'attack-test', 'hack-check', 'pentest', 'is this safe', or says 'run everything on it' — even if they only name one side. Do not stop at static review: if the target runs, verify findings live."
---

# AuditMe — combined offensive + defensive security audit

One run, both sides. The **defensive** side comes from the `security-audit`
skill (methodology, greps, WSTG, dynamic verification, fixes, machine-readable
findings). The **offensive** side comes from the `claude-red-*` skill library
(exploitation methodology per technique class). You orchestrate both against
the same target and produce ONE report.

Two hard rules:

1. **Never mark a finding from memory.** Every finding needs file:line (or a
   live observation) and the exact payload tried. The claude-red skills are
   methodology, not proof — their payloads must be run against the real sink.
2. **No item is skipped because it "doesn't apply."** If there's no network
   code, say `N/A — no fetch/XHR/WebSocket found (grep evidence)`. A missing
   section reads as "not checked."

## Step 0 — Threat model (2 minutes)

Run the 3-question interview from `security-audit` (crown jewel, adversaries,
shared device?). Offer its presets: **couples-app, saas-with-backend, p2p-game,
electron-desktop**. If the user won't answer, assume the most sensitive
plausible option and say so. Record answers — they tune every severity below.

## Step 1 — Pick the offensive kit

Match claude-red skills to what the target actually is (read the chosen
SKILL.md files first — they're the playbooks):

| Target has...                          | Activate these claude-red skills |
|----------------------------------------|----------------------------------|
| Web app / API / auth                   | `offensive-sqli`, `-xss`, `-jwt`, `-ssrf`, `-ssti`, `-xxe`, `-idor`, `-graphql`, `-open-redirect`, `-waf-bypass`, `-parameter-pollution`, `-race-condition`, `-business-logic`, `-request-smuggling`, `-deserialization`, `-file-upload`, `-rce` |
| Files uploaded / stored                | `-file-upload`, `-deserialization`, `-rce` |
| Desktop / Electron / native            | shell-hardening sections of `security-audit` + IPC/file-surface review (`-basic-exploitation` for memory only if native) |
| Cloud / infra in scope                 | `-cloud`, `-initial-access`, `-edr-evasion`, `-advanced-redteam` |
| Mobile in scope                        | `-mobile`, `-jwt` (storage sections) |
| Network / wireless in scope            | `-wifi`, `-wpa2-psk`, `-bluetooth-*`, `-iot`, `-z-wave`, etc. |
| Anything that parses input             | `-fuzzing`, `-vuln-classes`, `-bug-identification`, `-crash-analysis` |

Read the actual SKILL.md of each activated skill and follow its methodology.
If a category doesn't apply, write it down as N/A with grep evidence.

## Step 2 — Inventory + grep blitz

1. Inventory every source/config file. Note the data model (what's sensitive).
2. Run the defensive grep arsenal (from `security-audit/tools/`):
   ```bash
   python ~/.claude/skills/security-audit/tools/run-greps.py --root <target> --output hits.json
   ```
3. Run target-specific greps from the activated claude-red playbooks (e.g.
   SQLi → string-concat SQL, JWT → alg/jwk/jku headers, SSRF → fetch with
   user input in URL).
4. Record hits per group — these are the attack surface, not the findings.

## Step 3 — Defensive checklist sweep (security-audit)

Walk the `security-audit` checklist sections against the code, citing
file:line. Weight severities with Step 0's threat model (e.g. shared device
elevates storage findings; electron-desktop elevates any renderer-XSS-to-RCE
chain). Grep evidence for every N/A. Map coverage to WSTG IDs from
`security-audit/wstg-mapping.md`.

## Step 4 — Offensive pass (claude-red, in this order)

1. **Craft hostile inputs first** — for a vault, that's the file format the
   app parses; for a web app, every input sink. Fuzz parsers (truncation,
   length overflows, JSON bombs, oversized fields).
2. **Attack auth/session** (JWT methodology) — alg confusion, weak secrets,
   header injection, claims validation, token storage.
3. **Attack injection surfaces** (SQLi/XSS/SSTI/XXE/SSRF per the kit) — run
   the playbook's probes against the real sinks.
4. **Attack business logic / race conditions / IDOR** where state exists.
5. **Chain findings** — the goal is a kill chain, not a list. Missing CSP +
   one XSS sink = script execution surface, reported at the chained severity.

## Step 5 — Dynamic verification (if the target runs)

Run it (dev server / preview / packaged app). Observe console + network for
CSP violations, mixed content, failed SRI, runtime errors. Reproduce every
CRITICAL PoC through the REAL input path with a benign marker (e.g.
`window.__auditme_verified = 1`) — never exfiltrate to real infra. Label each
PoC `verified live` or `static-only (reason)`.

## Step 6 — Fixes

For every finding, emit the `security-audit` Fix Generation Format (file,
vulnerable block, drop-in secure replacement, why it works). For offensive
findings, use the claude-red playbook's remediation notes if present, then
the defensive fixes. Never describe a fix in prose only.

## Step 7 — Re-audit + deliverables

1. Re-run the relevant greps and re-verify each fix (mentally, then live
   where possible) — confirm no regression.
2. Emit machine-readable findings:
   ```bash
   # write findings.json per security-audit/findings.schema.json
   python ~/.claude/skills/security-audit/tools/validate-findings.py findings.json
   ```
3. Generate issue bodies from `security-audit/issue-template.md` (they plug
   into the ask-matt triage flow).
4. Produce the report: mode + threat model, summary counts, findings
   (Critical → Warning → Info), sections confirmed N/A, tooling gaps, and a
   binary ship verdict. 0 CRITICAL required for "ship-ready", said explicitly.

## Report header

```
# AuditMe — <target>
Mode: <quick|standard|deep>   Preset: <threat model used>
Findings data: findings.json (validated)   Filed issues: <n>
```
