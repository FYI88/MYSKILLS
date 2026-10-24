#!/usr/bin/env python3
"""
validate-findings.py — structural validation of a security-audit
findings.json, no external dependencies.

Checks the same rules as findings.schema.json (top-level shape, per-finding
required fields and enums, file+line mandatory for critical/warning,
duplicate ids, chain references, summary counts). Exit 0 = valid, 1 =
invalid, 2 = unreadable.

Usage:
    python tools/validate-findings.py findings.json
"""

import argparse
import json
import sys

SEVERITIES = {"critical", "warning", "info"}
STATUSES = {"open", "fix-proposed", "resolved"}
VERIFIED = {"live-browser", "static-only"}
MODES = {"quick", "standard", "deep"}


def main():
    ap = argparse.ArgumentParser(description="Validate a findings.json against the security-audit schema")
    ap.add_argument("findings", help="path to findings.json")
    args = ap.parse_args()

    try:
        with open(args.findings, "r", encoding="utf-8") as fh:
            data = json.load(fh)
    except Exception as exc:
        sys.exit(f"cannot read {args.findings}: {exc}")

    errors = []

    # ---- top level -----------------------------------------------------
    for key in ("schema_version", "audit", "threat_model", "findings", "chains", "summary"):
        if key not in data:
            errors.append(f"missing top-level key: {key}")
    if data.get("schema_version") != "1.0":
        errors.append(f"schema_version must be \"1.0\", got {data.get('schema_version')!r}")

    audit = data.get("audit", {})
    if audit.get("mode") not in MODES:
        errors.append(f"audit.mode must be one of {sorted(MODES)}, got {audit.get('mode')!r}")
    if not audit.get("app"):
        errors.append("audit.app is required")
    if not audit.get("date"):
        errors.append("audit.date is required")

    tm = data.get("threat_model", {})
    for key in ("crown_jewel", "adversaries", "shared_device", "backend_in_scope"):
        if key not in tm:
            errors.append(f"threat_model.{key} is required")
    if "adversaries" in tm and not isinstance(tm["adversaries"], list):
        errors.append("threat_model.adversaries must be a list")

    # ---- findings ------------------------------------------------------
    finding_ids = set()
    for i, f in enumerate(data.get("findings", [])):
        base = f"findings[{i}]"
        if not isinstance(f, dict):
            errors.append(f"{base}: must be an object")
            continue
        fid = f.get("id")
        if not isinstance(fid, str) or not fid.startswith("SEC-") or len(fid) != 7:
            errors.append(f"{base}: id must look like SEC-001, got {fid!r}")
        elif fid in finding_ids:
            errors.append(f"{base}: duplicate id {fid}")
        finding_ids.add(fid)

        if f.get("severity") not in SEVERITIES:
            errors.append(f"{base}: severity must be one of {sorted(SEVERITIES)}, got {f.get('severity')!r}")
        for key in ("title", "section", "status", "verified"):
            if key not in f:
                errors.append(f"{base}: missing required key {key}")
        if f.get("status") not in STATUSES:
            errors.append(f"{base}: status must be one of {sorted(STATUSES)}, got {f.get('status')!r}")
        if f.get("verified") not in VERIFIED:
            errors.append(f"{base}: verified must be one of {sorted(VERIFIED)}, got {f.get('verified')!r}")
        section = f.get("section")
        if section is not None and not (isinstance(section, int) and 1 <= section <= 15):
            errors.append(f"{base}: section must be an integer 1-15, got {section!r}")

        if f.get("severity") in ("critical", "warning"):
            if "file" not in f or "line" not in f:
                errors.append(f"{base}: {fid} ({f.get('severity')}) requires file and line")
        line = f.get("line")
        if line is not None and not (isinstance(line, int) and line >= 1):
            errors.append(f"{base}: line must be a positive integer, got {line!r}")

        for w in f.get("wstg", []):
            if not isinstance(w, str) or not w.startswith("WSTG-"):
                errors.append(f"{base}: wstg entries must look like WSTG-CLNT-01, got {w!r}")
        cwe = f.get("cwe")
        if cwe is not None and (not isinstance(cwe, str) or not cwe.startswith("CWE-")):
            errors.append(f"{base}: cwe must look like CWE-79, got {cwe!r}")

    # ---- chains --------------------------------------------------------
    chain_ids = set()
    for i, c in enumerate(data.get("chains", [])):
        base = f"chains[{i}]"
        cid = c.get("id")
        if not isinstance(cid, str) or not cid.startswith("CHAIN-"):
            errors.append(f"{base}: id must look like CHAIN-01, got {cid!r}")
        elif cid in chain_ids:
            errors.append(f"{base}: duplicate chain id {cid}")
        chain_ids.add(cid)
        if c.get("end_severity") not in SEVERITIES:
            errors.append(f"{base}: end_severity must be one of {sorted(SEVERITIES)}")
        for comp in c.get("components", []):
            if comp not in finding_ids:
                errors.append(f"{base}: component {comp!r} does not match any finding id")

    for i, f in enumerate(data.get("findings", [])):
        ref = f.get("chain")
        if ref and ref not in chain_ids:
            errors.append(f"findings[{i}]: chain reference {ref!r} does not match any chain id")

    # ---- summary counts ------------------------------------------------
    counts = {"critical": 0, "warning": 0, "info": 0}
    for f in data.get("findings", []):
        sev = f.get("severity") if isinstance(f, dict) else None
        if sev in counts:
            counts[sev] += 1
    summary = data.get("summary", {})
    for key, expected in (("critical", counts["critical"]),
                          ("warning", counts["warning"]),
                          ("info", counts["info"]),
                          ("chains", len(data.get("chains", [])))):
        if summary.get(key) != expected:
            errors.append(f"summary.{key} says {summary.get(key)!r}, expected {expected}")

    # ---- verdict -------------------------------------------------------
    if errors:
        print(f"INVALID: {len(errors)} error(s):")
        for err in errors:
            print(f"  - {err}")
        sys.exit(1)
    n = len(data.get("findings", []))
    print(f"VALID: {n} finding(s), {len(data.get('chains', []))} chain(s), summary consistent")


if __name__ == "__main__":
    main()
