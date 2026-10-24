#!/usr/bin/env bash
# MySkills installer — clones the skills repo and wires it into every agent that reads
# from a standard skills directory. Safe to re-run: it updates the clone and never
# deletes an existing agent skill folder.
#
# Usage:
#   curl -fsSL https://raw.githubusercontent.com/FYI88/MYSKILLS/main/install.sh | bash
#   bash install.sh --help

set -euo pipefail

REPO_URL="${MYSKILLS_REPO:-https://github.com/FYI88/MYSKILLS.git}"
BRANCH="${MYSKILLS_BRANCH:-main}"
CANONICAL="${MYSKILLS_DIR:-${HOME}/.agents/skills}"
DO_LINK=1
DO_HERMES=1
FORCE=0
DRY_RUN=0

LINK_TARGETS=(
  "${HOME}/.claude/skills"
  "${HOME}/.pi/agent/skills"
  "${HOME}/.config/opencode/skills"
)
HERMES_TARGET="${HOME}/.hermes/skills"

log()  { printf '  %s\n' "$*"; }
warn() { printf '  ! %s\n' "$*" >&2; }
err()  { printf '  x %s\n' "$*" >&2; }
step() { printf '\n==> %s\n' "$*"; }

usage() {
  cat <<'EOF'
MySkills installer

Options:
  --repo URL     Repository to install from (default: https://github.com/FYI88/MYSKILLS.git)
  --branch NAME  Branch to track (default: main)
  --dir PATH     Canonical skills directory (default: ~/.agents/skills)
  --no-link      Install only the canonical copy, do not link agent folders
  --no-hermes    Skip the Hermes independent copy
  --force        Repoint existing links / replace diverged entries
  --dry-run      Show what would happen without changing anything
  -h, --help     Show this help
EOF
}

while [ $# -gt 0 ]; do
  case "$1" in
    --repo) REPO_URL="$2"; shift 2 ;;
    --branch) BRANCH="$2"; shift 2 ;;
    --dir) CANONICAL="$2"; shift 2 ;;
    --no-link) DO_LINK=0; shift ;;
    --no-hermes) DO_HERMES=0; shift ;;
    --force) FORCE=1; shift ;;
    --dry-run) DRY_RUN=1; shift ;;
    -h|--help) usage; exit 0 ;;
    *) err "Unknown option: $1"; usage; exit 1 ;;
  esac
done

run() {
  if [ "$DRY_RUN" -eq 1 ]; then
    printf '  [dry-run] %s\n' "$*"
  else
    "$@"
  fi
}

step "Checking prerequisites"
if ! command -v git >/dev/null 2>&1; then
  err "git is required. Install Git, then re-run this script."
  exit 1
fi
log "git: $(git --version)"
log "canonical: ${CANONICAL}"

step "Installing the canonical skill collection"
mkdir -p "$(dirname "$CANONICAL")"

if [ -d "${CANONICAL}/.git" ]; then
  current_remote="$(git -C "$CANONICAL" remote get-url origin 2>/dev/null || true)"
  case "$current_remote" in
    *MYSKILLS*|*myskills*)
      log "existing clone found — updating"
      if [ "$DRY_RUN" -eq 1 ]; then
        log "[dry-run] git -C ${CANONICAL} pull --ff-only origin ${BRANCH}"
      else
        git -C "$CANONICAL" pull --ff-only origin "$BRANCH"
      fi
      ;;
    *)
      err "${CANONICAL} is a git repo for a different remote (${current_remote})."
      err "Re-run with --dir PATH to use a different location, or move the folder aside."
      exit 1
      ;;
  esac
elif [ -e "$CANONICAL" ] && [ -n "$(ls -A "$CANONICAL" 2>/dev/null)" ]; then
  err "${CANONICAL} exists and is not empty, and is not a git clone of MYSKILLS."
  err "Re-run with --dir PATH to use a different location, or move the folder aside."
  exit 1
else
  log "cloning ${REPO_URL}"
  if [ "$DRY_RUN" -eq 1 ]; then
    log "[dry-run] git clone --branch ${BRANCH} ${REPO_URL} ${CANONICAL}"
  else
    git clone --branch "$BRANCH" "$REPO_URL" "$CANONICAL"
  fi
fi

skill_count="$(find "$CANONICAL" -name SKILL.md -not -path '*/.git/*' 2>/dev/null | wc -l | tr -d ' ' || true)"
[ -n "$skill_count" ] || skill_count=0
log "${skill_count} skills available"

if [ "$DO_LINK" -eq 0 ]; then
  step "Done (agent linking skipped)"
  exit 0
fi

make_link() {
  local target="$1"
  local source="$2"
  if [ "$DRY_RUN" -eq 1 ]; then
    printf '  [dry-run] link %s -> %s\n' "$target" "$source"
    return 0
  fi
  if ln -s "$source" "$target" 2>/dev/null; then
    return 0
  fi
  warn "symlinks unavailable, copying instead: ${target}"
  cp -R "$source" "$target"
}

link_into() {
  local target="$1"
  local parent
  parent="$(dirname "$target")"

  if [ -L "$target" ]; then
    local current
    current="$(readlink "$target")"
    if [ "$current" = "$CANONICAL" ]; then
      log "already linked: ${target}"
      return 0
    fi
    if [ "$FORCE" -eq 1 ]; then
      log "repointing: ${target} -> ${CANONICAL}"
      run rm "$target"
      make_link "$target" "$CANONICAL"
      return 0
    fi
    warn "${target} points to ${current} (use --force to repoint)"
    return 0
  fi

  if [ -d "$target" ]; then
    log "existing folder found, merging skills into it: ${target}"
    merge_into_dir "$target"
    return 0
  fi

  log "linking: ${target} -> ${CANONICAL}"
  run mkdir -p "$parent"
  make_link "$target" "$CANONICAL"
}

merge_into_dir() {
  local dir="$1"
  local linked=0
  local kept=0
  local skill_path
  local name
  local dest
  local current

  for skill_path in "${CANONICAL}"/*/; do
    [ -f "${skill_path}SKILL.md" ] || continue
    name="$(basename "$skill_path")"
    dest="${dir}/${name}"

    if [ -L "$dest" ]; then
      current="$(readlink "$dest")"
      if [ "$current" = "${skill_path%/}" ]; then
        continue
      fi
      if [ "$FORCE" -eq 1 ]; then
        run rm "$dest"
      else
        kept=$((kept + 1))
        continue
      fi
    elif [ -e "$dest" ]; then
      kept=$((kept + 1))
      continue
    fi

    make_link "$dest" "${skill_path%/}"
    linked=$((linked + 1))
  done

  log "linked ${linked} new skill(s), kept ${kept} existing entr(ies) untouched"
}

step "Linking agent skill folders"
for target in "${LINK_TARGETS[@]}"; do
  link_into "$target"
done

if [ "$DO_HERMES" -eq 1 ]; then
  step "Copying skills for Hermes (independent copy, as Hermes snapshots on start)"
  if [ "$DRY_RUN" -eq 1 ]; then
    log "[dry-run] copy ${CANONICAL}/* -> ${HERMES_TARGET}"
  else
    mkdir -p "$HERMES_TARGET"
    copied=0
    for skill_path in "${CANONICAL}"/*/; do
      [ -f "${skill_path}SKILL.md" ] || continue
      name="$(basename "$skill_path")"
      if [ -d "${HERMES_TARGET}/${name}" ] && [ "$FORCE" -eq 0 ]; then
        continue
      fi
      rm -rf "${HERMES_TARGET:?}/${name}"
      cp -R "$skill_path" "${HERMES_TARGET}/${name}"
      copied=$((copied + 1))
    done
    log "copied ${copied} skill(s) to ${HERMES_TARGET}"
  fi
fi

step "Done"
log "Re-run this script anytime to pull the latest skills."
log "Browse the catalog: ${CANONICAL}/CATALOG.md"
