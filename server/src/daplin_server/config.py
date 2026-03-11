"""Application configuration via pydantic-settings.

All settings are read from environment variables with the ``DAPLIN_`` prefix,
or from a ``.env`` file in the working directory.
"""

from __future__ import annotations

from pathlib import Path
from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="DAPLIN_",
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    instance_domain: str = Field(default="localhost", description="Public domain of this instance")
    instance_name: str = Field(default="Daplin Dev", description="Human-readable instance name")
    database_url: str = Field(
        default="sqlite+aiosqlite:///./daplin.db",
        description="SQLAlchemy async database URL",
    )
    storage_backend: Literal["filesystem", "ipfs"] = Field(
        default="filesystem",
        description="Content storage backend",
    )
    storage_path: Path = Field(
        default=Path("./storage"),
        description="Root directory for filesystem storage backend",
    )
    ipfs_api_url: str = Field(
        default="http://localhost:5001",
        description="Kubo HTTP RPC API URL for IPFS backend",
    )
    nats_url: str | None = Field(
        default=None,
        description="NATS server URL; None = use in-memory queue",
    )
    jwt_secret: str = Field(
        default="dev-secret-change-me",
        description="Secret key for JWT signing (change in production!)",
    )
    jwt_expiry_minutes: int = Field(
        default=60,
        description="JWT token lifetime in minutes",
    )
    federation_enabled: bool = Field(
        default=True,
        description="Whether this instance participates in federation",
    )
    registrations_open: bool = Field(
        default=True,
        description="Whether new identity registrations are accepted",
    )
