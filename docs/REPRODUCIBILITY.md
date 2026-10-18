# Reproducibility guide

This document describes how to capture the environment and rerun the research without leaking local state or distributing restricted artifacts.

## 1. Capture both Conda environments

Run from the project root:

```bash
mkdir -p environment
conda env export --no-builds -n laya > environment/laya-environment.yml
conda run -n laya python -m pip freeze > environment/laya-pip-freeze.txt
conda env export --no-builds -n pkreviews > environment/pkreviews-environment.yml
conda run -n pkreviews python -m pip freeze > environment/pkreviews-pip-freeze.txt
```

Review the files for local absolute paths, private package indexes, secrets, and machine-specific dependencies. Environment exports may contain more than the project strictly requires; label them as captured environments rather than minimal installation specifications.

## 2. Record hardware and model versions

For each run, save non-sensitive output from:

```bash
nvidia-smi
conda list -n laya
conda list -n pkreviews
```

Also record the source-control commit, Python version, CUDA runtime/driver, model identifier and digest, inference parameters, seed, batch size, worker count, and evaluation command. Do not include endpoint credentials or private server details.

## 3. Preserve evaluation integrity

- Keep training, validation, and held-out test sets separate.
- Deduplicate exact and normalized/near-duplicate reviews before splitting.
- Freeze the test set before model or prompt selection.
- Keep the metric definition and evaluation script version alongside each result.
- Report denominators, missing/invalid outputs, and confidence intervals where appropriate.
- Treat the 100-review audit as a diagnostic sample, not a definitive benchmark.

## 4. Charts

Regenerate charts from machine-readable result files and check that labels match the underlying measurements. Mark estimates as estimates. Include chart-generation source code and the exact input results when licensing and privacy allow. Do not manually edit chart values to make results look better.

## 5. Public release safety checks

Before committing:

```bash
git status --short
find . -type f -size +50M -print
# If installed, scan the staged tree for secrets using a trusted secret scanner.
```

Review the complete diff, raw data, generated files, environment exports, notebook outputs, logs, and Git history. Removing a secret from the latest commit does not remove it from prior commits; rotate any exposed credentials.
