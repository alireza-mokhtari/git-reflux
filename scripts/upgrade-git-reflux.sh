#!/usr/bin/env bash
set -euo pipefail

# Upgrade git-reflux installed via pipx. Accepts optional path to local repo.
# Usage:
#   upgrade-git-reflux.sh                 # upgrade from PyPI (if spec was PyPI)
#   upgrade-git-reflux.sh /path/to/repo   # force-reinstall from local path

REPO_PATH="${1:-}"

if ! command -v pipx >/dev/null 2>&1; then
  echo "pipx not found. Please install pipx first (brew install pipx; pipx ensurepath)." >&2
  exit 1
fi

# Ensure pipx shims dir is in PATH for this shell
export PATH="$HOME/.local/bin:$PATH"

if [[ -n "$REPO_PATH" ]]; then
  echo "Reinstalling git-reflux from local path: $REPO_PATH"
  pipx install --force "$REPO_PATH"
else
  echo "Upgrading git-reflux via pipx (using existing spec)"
  pipx upgrade git-reflux || {
    echo "pipx upgrade failed; trying force reinstall from existing spec" >&2
    pipx install --force git-reflux
  }
fi

echo "Upgrade complete. Version: $(git-reflux --version 2>/dev/null || true)"


