"""Centralized application configuration."""

from __future__ import annotations

from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

_DEFAULT_GRAPH_PATH = Path(__file__).resolve().parent.parent / "data" / "train-ticket-be.json"


class Settings(BaseSettings):
    graph_path: Path = _DEFAULT_GRAPH_PATH

    model_config = SettingsConfigDict(env_prefix="SRQE_")


settings = Settings()
