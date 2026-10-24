#!/usr/bin/env bash
# sync-install.sh — propagate edits to the installed copy of this skill.
#
# Run this from the workspace copy of the skill after editing, so the
# installed copy (~/.claude/skills/security-audit) picks up the changes
# and /security-audit stays current.
#
# Usage:
#   bash tools/sync-install.sh                 # sync to ~/.claude/skills/security-audit
#   bash tools/sync-install.sh --downloads     # also refresh the flat copies in ~/Downloads
#   bash tools/sync-install.sh --check         # report whether the installed copy is in sync
#   DEST=/custom/path bash tools/sync-install.sh   # override the install target
#
# One-liner equivalent (no script needed):
#   cp -R skills/security-audit/. ~/.claude/skills/security-audit/
set -euo pipefail

SRC="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DEST="${DEST:-$HOME/.claude/skills/security-audit}"

excludes() {
  echo --exclude '__pycache__' --exclude '*.pyc' --exclude '.DS_Store'
}

check() {
  if [ ! -d "$DEST" ]; then
    echo "not installed yet — run: bash tools/sync-install.sh"
    return
  fi
  if command -v diff >/dev/null 2>&1; then
    local out
    out="$(diff -rq "$SRC" "$DEST" 2>&1 || true)"
    if [ -z "$out" ]; then
      echo "in sync: $SRC == $DEST"
    else
      echo "OUT OF SYNC — differences:"
      echo "$out"
    fi
  else
    echo "diff not available; run the sync and trust the copy"
  fi
}

sync_to() {
  local target="$1"
  mkdir -p "$target"
  if command -v rsync >/dev/null 2>&1; then
    rsync -a "$(excludes)" "$SRC/" "$target/"
  else
    cp -R "$SRC/." "$target/"
    find "$target" -type d -name '__pycache__' -exec rm -rf {} + 2>/dev/null || true
    find "$target" -type f -name '*.pyc' -delete 2>/dev/null || true
  fi
  echo "synced: $SRC -> $target"
}

case "${1:-}" in
  --check)
    check
    ;;
  --downloads)
    sync_to "$DEST"
    for f in SKILL.md wstg-mapping.md threat-model-presets.md; do
      cp "$SRC/$f" "$HOME/Downloads/$f"
    done
    echo "refreshed flat copies in $HOME/Downloads (SKILL.md, wstg-mapping.md, threat-model-presets.md)"
    ;;
  *)
    sync_to "$DEST"
    ;;
esac
