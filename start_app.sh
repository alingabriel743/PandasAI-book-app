#!/usr/bin/env bash
set -euo pipefail

# Determine repo root regardless of the invocation location
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$REPO_ROOT"

VENV_PATH="$REPO_ROOT/venv/bin/activate"
if [[ -f "$VENV_PATH" ]]; then
  # shellcheck disable=SC1090
  source "$VENV_PATH"
fi

exec streamlit run app.py
