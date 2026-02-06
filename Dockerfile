# Project Chimera — Docker image for standardized test runs.
# Python 3.11+; dependencies via uv; capable of running failing tests (Task 3.2).
# No production logic; interfaces and tests only.

FROM python:3.12-slim

# Install uv for reproducible dependency install (per specs / tooling strategy)
RUN pip install --no-cache-dir uv

WORKDIR /app

# Copy dependency manifests first for better layer caching
COPY pyproject.toml uv.lock README.md ./
COPY src ./src
COPY tests ./tests
COPY skills ./skills

# Install project and all dependency groups (includes dev for pytest).
# --no-editable would skip editable install; we need the package on PYTHONPATH.
RUN uv sync --frozen --all-groups

# Default: run the test suite (failing tests are expected until implementations exist)
CMD ["uv", "run", "pytest", "tests/", "-v", "--tb=short"]
