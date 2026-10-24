#!/usr/bin/env python3
"""
sri.py — generate real Subresource Integrity hashes for CDN findings.

Instead of writing "add an integrity attribute" in a fix, compute the actual
hash of the resource the app is loading so the fix is drop-in.

Usage:
    python tools/sri.py <url>
    python tools/sri.py <url> --algo sha256|sha384|sha512
    python tools/sri.py <url> --tag            # print a full <script> tag

Prints the integrity value (or full tag with --tag). Exit code 0 on success,
1 on fetch failure.
"""

import argparse
import base64
import hashlib
import sys
import urllib.request

USER_AGENT = "security-audit-sri-generator/1.0"
TIMEOUT = 30


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
        if resp.status != 200:
            raise RuntimeError(f"HTTP {resp.status} for {url}")
        final_url = resp.geturl()
        return resp.read(), final_url


def integrity(data, algo):
    digest = hashlib.new(algo, data).digest()
    b64 = base64.b64encode(digest).decode("ascii")
    return f"{algo}-{b64}"


def main():
    ap = argparse.ArgumentParser(description="Generate an SRI integrity hash for a CDN resource")
    ap.add_argument("url", help="https:// URL of the resource")
    ap.add_argument("--algo", choices=["sha256", "sha384", "sha512"], default="sha384")
    ap.add_argument("--tag", action="store_true", help="print a full <script> tag")
    args = ap.parse_args()

    if not args.url.startswith(("https://", "http://")):
        sys.exit(f"not a fetchable URL: {args.url}")

    try:
        data, final_url = fetch(args.url)
    except Exception as exc:
        sys.exit(f"fetch failed: {exc}")

    value = integrity(data, args.algo)
    if args.tag:
        print(f'<script src="{args.url}" integrity="{value}" crossorigin="anonymous"></script>')
    else:
        print(value)
    if final_url != args.url:
        print(f"(redirected to: {final_url})", file=sys.stderr)


if __name__ == "__main__":
    main()
