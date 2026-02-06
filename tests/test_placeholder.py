"""Placeholder test to verify pytest and environment."""

import chimera


def test_chimera_has_version() -> None:
    """Chimera package exposes a version."""
    assert chimera.__version__ == "0.1.0"
