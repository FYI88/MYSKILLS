#!/usr/bin/env python3
"""
osv-check.py — real CVE data for dependencies via the OSV API.

The audit skill must never *claim* a dependency is vulnerable from memory.
This tool queries the OSV database (api.osv.dev) for every pinned dependency
in package.json / package-lock.json and reports actual vulnerability IDs,
summaries, and (when available) fixed versions.

It uses /v1/query (which returns full advisory records) rather than
/v1/querybatch (which returns stub records), and verifies each advisory's
affected ranges actually contain the pinned version client-side, so a
package-only OSV match can't turn into a false-positive finding.

Usage:
    python tools/osv-check.py                     # uses ./package.json + ./package-lock.json
    python tools/osv-check.py --manifest app/package.json
    python tools/osv-check.py --manifest app/package.json --lockfile app/package-lock.json
    python tools/osv-check.py --manifest app/package.json --json   # also write osv-findings.json

Exit codes:
    0  scanned, no known vulnerabilities (or nothing to scan)
    1  known vulnerabilities found
    2  tool-level failure (network, parse) — the skill must fall back to
       web search / manual review and note it in the report
"""

import argparse
import json
import os
import re
import sys
import urllib.request
from concurrent.futures import ThreadPoolExecutor

OSV_QUERY_URL = "https://api.osv.dev/v1/query"
TIMEOUT = 60
MAX_WORKERS = 8

# --------------------------------------------------------------------------
# Minimal semver comparison (npm versions; prereleases treated as < release)
# --------------------------------------------------------------------------

_SEMVER_RE = re.compile(r"^(\d+)(?:\.(\d+))?(?:\.(\d+))?(?:[-+].*)?$")


def _parse(v):
    m = _SEMVER_RE.match(str(v).strip().lstrip("v= "))
    if not m:
        return None
    major, minor, patch = m.groups()
    return (int(major or 0), int(minor or 0), int(patch or 0))


def _lt(a, b):
    pa, pb = _parse(a), _parse(b)
    if pa is None or pb is None:
        return None  # unparseable — caller treats as unknown
    return pa < pb


def _lte(a, b):
    pa, pb = _parse(a), _parse(b)
    if pa is None or pb is None:
        return None
    return pa <= pb


def version_in_range(version, rng):
    """True/False if the range clearly does/doesn't contain version; None if unknowable."""
    events = rng.get("events", [])
    introduced = fixed = last_affected = None
    for event in events:
        if "introduced" in event:
            introduced = event["introduced"]
        elif "fixed" in event:
            fixed = event["fixed"]
        elif "last_affected" in event:
            last_affected = event["last_affected"]
    if introduced is not None and introduced != "0":
        if _lt(version, introduced) is True:
            return False
    if fixed is not None:
        return _lt(version, fixed)
    if last_affected is not None:
        return _lte(version, last_affected)
    return None  # only an 'introduced' event, or malformed


def is_affected(name, version, vuln):
    """Return (matched: bool, how: str). 'how' explains the match for the report."""
    matched_any = False
    for affected in vuln.get("affected", []):
        pkg = affected.get("package", {})
        if pkg.get("name") != name:
            continue
        versions = affected.get("versions")
        if versions is not None:
            matched_any = True
            if version in versions:
                return True, "versions list"
        for rng in affected.get("ranges", []):
            res = version_in_range(version, rng)
            if res is True:
                return True, "affected range"
            if res is None:
                matched_any = True
    # OSV matched the package but no range/list data supports containment.
    return (None, "package-only match (range unverifiable)") if matched_any else (False, "no affected entry")


# --------------------------------------------------------------------------
# Package collection
# --------------------------------------------------------------------------


def read_json(path):
    with open(path, "r", encoding="utf-8") as fh:
        return json.load(fh)


def collect_packages(manifest_path, lockfile_path):
    """Return a dict name -> version (resolved via lockfile when present)."""
    pkgs = {}
    if manifest_path and os.path.isfile(manifest_path):
        manifest = read_json(manifest_path)
        for section in ("dependencies", "devDependencies", "optionalDependencies"):
            for name, version in manifest.get(section, {}).items():
                pkgs.setdefault(name, version)  # lockfile resolution may override
    if lockfile_path and os.path.isfile(lockfile_path):
        lock = read_json(lockfile_path)
        if "packages" in lock:  # lockfile v2/v3
            for path, info in lock["packages"].items():
                if path and "version" in info:
                    name = path.rsplit("node_modules/", 1)[-1]
                    if not name:
                        continue
                    pkgs[name] = info["version"]
        elif "dependencies" in lock:  # lockfile v1
            for name, info in lock["dependencies"].items():
                pkgs[name] = info.get("version", "")
    return pkgs


# --------------------------------------------------------------------------
# OSV querying
# --------------------------------------------------------------------------


def query_one(name, version):
    body = json.dumps({
        "package": {"name": name, "ecosystem": "npm"},
        "version": version,
    }).encode("utf-8")
    req = urllib.request.Request(
        OSV_QUERY_URL, data=body,
        headers={"Content-Type": "application/json", "User-Agent": "security-audit-osv-check/1.0"},
    )
    with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    return data.get("vulns", [])


def fixed_version(name, vuln):
    """First known-fixed version across the advisory's affected entries for this package."""
    for affected in vuln.get("affected", []):
        if affected.get("package", {}).get("name") != name:
            continue
        for rng in affected.get("ranges", []):
            for event in rng.get("events", []):
                if "fixed" in event:
                    return event["fixed"]
    return None


def severity_of(vuln):
    for s in vuln.get("severity", []):
        if s.get("type") == "CVSS_V3":
            return s.get("score", "")
    return ""


def check_package(item):
    name, version = item
    try:
        vulns = query_one(name, version)
    except Exception as exc:
        return (name, version, None, f"query failed: {exc}")
    findings = []
    for vuln in vulns:
        matched, how = is_affected(name, version, vuln)
        if matched is False:
            continue  # OSV package-only noise — range clearly excludes this version
        findings.append({
            "package": name,
            "version": version,
            "id": vuln.get("id", "?"),
            "summary": vuln.get("summary", ""),
            "severity": severity_of(vuln),
            "fixed": fixed_version(name, vuln),
            "match": how,
            "reference": f"https://osv.dev/vulnerability/{vuln.get('id', '')}",
        })
    return (name, version, findings, None)


def main():
    ap = argparse.ArgumentParser(description="Check npm dependencies against the OSV vulnerability database")
    ap.add_argument("--manifest", default="package.json")
    ap.add_argument("--lockfile", default="package-lock.json")
    ap.add_argument("--json", action="store_true", help="write osv-findings.json")
    args = ap.parse_args()

    try:
        packages = collect_packages(args.manifest, args.lockfile)
    except Exception as exc:
        sys.exit(f"tool-level failure reading manifests: {exc}")

    if not packages:
        print("no dependencies found to check (no package.json / lockfile)")
        sys.exit(0)

    errors = []
    findings = []
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as pool:
        for name, version, result, error in pool.map(check_package, packages.items()):
            if error:
                errors.append(f"{name}@{version}: {error}")
            elif result:
                findings.extend(result)

    for err in errors:
        print(f"  !! {err}", file=sys.stderr)
    if errors:
        print("  (some packages could not be checked — see Tooling gaps in the report)", file=sys.stderr)

    if args.json:
        with open("osv-findings.json", "w", encoding="utf-8") as fh:
            json.dump(findings, fh, indent=2)
            fh.write("\n")

    if not findings:
        print(f"checked {len(packages)} pinned dependencies: no known vulnerabilities found")
        sys.exit(0 if not errors else 2)

    print(f"{len(findings)} known vulnerability/ies across {len(packages)} pinned dependencies:\n")
    for f in findings:
        fixed = f["fixed"] or "unknown"
        print(f"  {f['id']}  {f['package']}@{f['version']}  "
              f"CVSS {f['severity'] or 'n/a'}  fixed in {fixed}  [{f['match']}]")
        print(f"    {f['summary'][:140]}")
        print(f"    {f['reference']}")
    sys.exit(1 if not errors else 1)


if __name__ == "__main__":
    main()
