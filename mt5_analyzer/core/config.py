"""
config.py

Configuration manager for MT5 Strategy Analyzer.

Loads application configuration from JSON and validates it using
Pydantic models.

Author:
    MT5 Strategy Analyzer

License:
    MIT
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Optional

from pydantic import BaseModel, Field, ValidationError as PydanticValidationError

from mt5_analyzer.core.exceptions import ConfigurationError


# ============================================================================
# Configuration Models
# ============================================================================


class GeneralConfig(BaseModel):
    """General application settings."""

    initial_equity: float = Field(default=100.0, gt=0)
    margin_per_trade: float = Field(default=5.0, gt=0)
    default_lot_size: float = Field(default=0.01, gt=0)
    timezone: str = "UTC"


class SessionConfig(BaseModel):
    """Trading session definitions."""

    asia_start: str = "00:00"
    asia_end: str = "08:00"

    europe_start: str = "08:00"
    europe_end: str = "13:00"

    us_overlap_start: str = "13:00"
    us_overlap_end: str = "17:00"

    late_us_start: str = "17:00"
    late_us_end: str = "23:59"


class PatternConfig(BaseModel):
    """Pattern engine settings."""

    enabled: list[str] = [
        "Original",
        "L",
        "LL",
        "LLL",
        "LLLL",
        "LLLLL",
    ]


class DrawdownConfig(BaseModel):
    """Drawdown strategy settings."""

    thresholds: list[int] = [10, 15, 20, 25, 30]


class ReportConfig(BaseModel):
    """Report generation settings."""

    output_directory: str = "output"
    create_charts: bool = True
    overwrite_existing: bool = True


class ApplicationConfig(BaseModel):
    """Root configuration object."""

    general: GeneralConfig = GeneralConfig()
    sessions: SessionConfig = SessionConfig()
    patterns: PatternConfig = PatternConfig()
    drawdown: DrawdownConfig = DrawdownConfig()
    reports: ReportConfig = ReportConfig()


# ============================================================================
# Configuration Manager
# ============================================================================


class ConfigManager:
    """
    Loads and caches application configuration.
    """

    _config: Optional[ApplicationConfig] = None

    @classmethod
    def load(
        cls,
        config_file: str | Path = "config/config.json",
    ) -> ApplicationConfig:
        """
        Load configuration from JSON.

        Parameters
        ----------
        config_file
            Path to JSON configuration file.

        Returns
        -------
        ApplicationConfig
        """

        if cls._config is not None:
            return cls._config

        path = Path(config_file)

        if not path.exists():
            raise ConfigurationError(
                f"Configuration file not found: {path}"
            )

        try:
            with path.open(
                "r",
                encoding="utf-8",
            ) as fp:
                data = json.load(fp)

            cls._config = ApplicationConfig.model_validate(data)

            return cls._config

        except json.JSONDecodeError as ex:
            raise ConfigurationError(
                f"Invalid JSON configuration: {ex}"
            ) from ex

        except PydanticValidationError as ex:
            raise ConfigurationError(
                f"Configuration validation failed:\n{ex}"
            ) from ex

    @classmethod
    def get(cls) -> ApplicationConfig:
        """
        Return cached configuration.

        Raises
        ------
        ConfigurationError
            If configuration has not been loaded.
        """

        if cls._config is None:
            raise ConfigurationError(
                "Configuration has not been loaded."
            )

        return cls._config

    @classmethod
    def reload(
        cls,
        config_file: str | Path = "config/config.json",
    ) -> ApplicationConfig:
        """
        Force reload configuration.
        """

        cls._config = None

        return cls.load(config_file)

    @classmethod
    def reset(cls) -> None:
        """
        Clear cached configuration.

        Mainly used in unit tests.
        """

        cls._config = None
