# Project Chimera — Automation (Task 3.2).
# Requires: uv (https://docs.astral.sh/uv/), Docker (for test).
# On Windows without make: run the commands under each target manually.

# Default target
.PHONY: setup test spec-check
.DEFAULT_GOAL := help

# Image name for Docker test run
IMAGE := chimera

help:
	@echo "Targets: setup | test | spec-check"

# Install dependencies on the host using uv (no Docker)
setup:
	uv sync --all-groups

# Run pytest inside Docker to eliminate environment drift (same result everywhere).
# Requires Docker daemon to be running (e.g. Docker Desktop on Windows).
test:
	docker build -t $(IMAGE) .
	docker run --rm $(IMAGE)

# Placeholder: verify code references specs/ (e.g. comments, docstrings, or imports).
# Expand to grep/scripts as needed; exit 0 so CI does not fail on placeholder.
spec-check:
	@echo "Placeholder: spec-check — verify code references specs/"
	@(grep -r "specs/" src tests 2>/dev/null | head -5) || true
	@echo "Done (placeholder)."
