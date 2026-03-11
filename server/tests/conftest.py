"""Shared pytest fixtures for the daplin-server test suite."""

from __future__ import annotations

import pytest

from daplin_server.config import Settings


@pytest.fixture
def settings() -> Settings:
    """Return a Settings instance configured for testing."""
    return Settings(
        instance_domain="test.localhost",
        instance_name="Daplin Test",
        database_url="sqlite+aiosqlite:///:memory:",
        storage_backend="filesystem",
        storage_path=__import__("pathlib").Path("/tmp/daplin-test-storage"),
        nats_url=None,
        jwt_secret="test-secret",
        federation_enabled=False,
    )
