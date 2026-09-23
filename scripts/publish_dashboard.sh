#!/usr/bin/env bash
# Commits and pushes the latest trade/equity data so the GitHub Pages dashboard reflects it.
set -euo pipefail
cd "$(dirname "$0")/.."

git add docs/data/trades.json docs/data/equity.json
if git diff --cached --quiet; then
  echo "No dashboard data changes to publish."
  exit 0
fi

git commit -m "Update dashboard data"
git push
