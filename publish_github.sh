#!/usr/bin/env bash
set -Eeuo pipefail

# Run from the actual project root. This script intentionally does not upload raw datasets,
# databases, checkpoints, or model weights. Review every staged file before publishing.

if ! command -v git >/dev/null 2>&1; then echo "ERROR: git is not installed." >&2; exit 1; fi
if ! command -v gh >/dev/null 2>&1; then echo "ERROR: GitHub CLI (gh) is not installed." >&2; exit 1; fi
if ! gh auth status >/dev/null 2>&1; then echo "ERROR: gh is not authenticated. Run: gh auth login" >&2; exit 1; fi

ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
cd "$ROOT"

read -r -p "GitHub repository name (e.g. roman-urdu-ecommerce-sentiment): " REPO
if [[ -z "${REPO// }" ]]; then echo "Repository name cannot be empty." >&2; exit 1; fi
read -r -p "Visibility (public/private) [public]: " VISIBILITY
VISIBILITY="${VISIBILITY:-public}"
if [[ "$VISIBILITY" != "public" && "$VISIBILITY" != "private" ]]; then echo "Visibility must be public or private." >&2; exit 1; fi

mkdir -p environment
if conda env list | awk '{print $1}' | grep -qx 'laya'; then
  conda env export --no-builds -n laya > environment/laya-environment.yml
  conda run -n laya python -m pip freeze > environment/laya-pip-freeze.txt
else echo "NOTE: Conda environment 'laya' not found; skipped its exports."; fi
if conda env list | awk '{print $1}' | grep -qx 'pkreviews'; then
  conda env export --no-builds -n pkreviews > environment/pkreviews-environment.yml
  conda run -n pkreviews python -m pip freeze > environment/pkreviews-pip-freeze.txt
else echo "NOTE: Conda environment 'pkreviews' not found; skipped its exports."; fi

printf '\nPotentially large files (>50 MiB):\n'
find . -type f -size +50M -not -path './.git/*' -print || true
printf '\nPotential secret-like filenames (review manually):\n'
find . -type f \( -iname '.env' -o -iname '*credential*' -o -iname '*secret*' -o -iname '*token*' -o -iname '*.pem' -o -iname '*.key' \) -not -path './.git/*' -print || true

if [[ ! -f README.md ]]; then echo "ERROR: README.md missing in $ROOT. Copy/adapt the release-kit README first." >&2; exit 1; fi
if [[ ! -f .gitignore ]]; then echo "WARNING: .gitignore is missing; add and review one before continuing."; fi

printf '\nCurrent project root: %s\n' "$ROOT"
# Initialize Git before checking repository status.
if [[ ! -d .git ]]; then git init; fi

printf 'Files currently tracked/untracked (review this carefully):\n'
git status --short

read -r -p "Have you verified data/model licensing, privacy, and the full staged diff? Type PUBLISH to continue: " CONFIRM
if [[ "$CONFIRM" != "PUBLISH" ]]; then echo "Cancelled. No repository was created."; exit 0; fi
if ! git config user.name >/dev/null || ! git config user.email >/dev/null; then
  echo "Git author identity is not configured. Set git config user.name and user.email, then rerun." >&2
  exit 1
fi

# Explicit allowlist for the first research release.
# Do not stage the whole scripts/, evaluation/, or environment/ directories.
git add README.md README_DARAZ_RUNNER.md DATASET_CARD.md CITATION.cff .gitignore publish_github.sh
git add docs/REPRODUCIBILITY.md docs/roman_urdu_language_policy.md

# Include only the reviewed environment exports.
git add environment/laya-environment.yml environment/laya-pip-freeze.txt
git add environment/pkreviews-environment.yml environment/pkreviews-pip-freeze.txt

# Include the approved chart images and aggregate evaluation report.
git add figures/aspect_category_f1_by_label.png
git add figures/classification_accuracy.png
git add figures/classification_macro_f1.png
git add figures/inference_throughput.png
git add figures/intent_f1_by_label.png
git add figures/multilabel_micro_f1.png
git add figures/seconds_per_record.png
git add evaluation/roman_urdu_100_v1/analysis_report/REPORT.md

# Include aggregate metrics only; never add predictions or disagreement files.
git add -f evaluation/roman_urdu_100_v1/analysis_report/classification_metrics.csv
git add -f evaluation/roman_urdu_100_v1/analysis_report/inference_speed.csv
git add -f evaluation/roman_urdu_100_v1/analysis_report/multilabel_metrics.csv
git add -f evaluation/roman_urdu_100_v1/analysis_report/per_label_metrics.csv

# Stage only explicitly approved files. Review staged content before committing.
printf '\nStaged files:\n'
git diff --cached --name-status
printf '\nStaged diff summary:\n'
git diff --cached --stat
read -r -p "Type COMMIT to commit the staged files: " COMMIT_CONFIRM
if [[ "$COMMIT_CONFIRM" != "COMMIT" ]]; then echo "Cancelled before commit. Review staging and rerun."; exit 0; fi

git commit -m "Document Roman Urdu sentiment research and reproducibility"

OWNER="$(gh api user --jq .login)"
if gh repo view "$OWNER/$REPO" >/dev/null 2>&1; then
  echo "Repository already exists: https://github.com/$OWNER/$REPO"
  git remote get-url origin >/dev/null 2>&1 || git remote add origin "https://github.com/$OWNER/$REPO.git"
else
  gh repo create "$OWNER/$REPO" "--$VISIBILITY" --description "Roman Urdu e-commerce review sentiment research: Qwen-assisted annotation and LAYA evaluation" --source=. --remote=origin
fi

git push -u origin HEAD
printf '\nPublished: https://github.com/%s/%s\n' "$OWNER" "$REPO"
