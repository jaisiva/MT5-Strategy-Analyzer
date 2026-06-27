"""
logger.py

Application-wide logging infrastructure for MT5 Strategy Analyzer.

This module provides a singleton logger manager built on top of Loguru.

Features
--------
- Console logging
- Rotating file logs
- Colored output
- Configurable debug mode
- Exception tracing
- Thread-safe singleton

Author:
    MT5 Strategy Analyzer

License:
    MIT
"""

from __future__ import annotations

from pathlib import Path
from typing import Optional

from loguru import logger


class LoggerManager:
    """
    Singleton Loguru logger manager.
    """

    _configured: bool = False

    @classmethod
    def configure(
        cls,
        log_directory: str | Path = "logs",
        log_level: str = "INFO",
        debug: bool = False,
    ) -> None:
        """
        Configure Loguru logger.

        Parameters
        ----------
        log_directory
            Directory where log files are written.

        log_level
            Minimum logging level.

        debug
            Enables DEBUG logging.
        """

        if cls._configured:
            return

        log_path = Path(log_directory)
        log_path.mkdir(parents=True, exist_ok=True)

        logger.remove()

        # ------------------------------------------------------------------
        # Console
        # ------------------------------------------------------------------

        logger.add(
            sink=lambda msg: print(msg, end=""),
            level="DEBUG" if debug else log_level,
            colorize=True,
            format=(
                "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
                "<level>{level:<8}</level> | "
                "<cyan>{name}</cyan>:"
                "<cyan>{function}</cyan>:"
                "<cyan>{line}</cyan> - "
                "<level>{message}</level>"
            ),
        )

        # ------------------------------------------------------------------
        # File
        # ------------------------------------------------------------------

        logger.add(
            log_path / "mt5_analyzer.log",
            level="DEBUG",
            rotation="10 MB",
            retention="30 days",
            compression="zip",
            enqueue=True,
            backtrace=True,
            diagnose=True,
            encoding="utf-8",
            format=(
                "{time:YYYY-MM-DD HH:mm:ss.SSS} | "
                "{level:<8} | "
                "{name}:{function}:{line} | "
                "{message}"
            ),
        )

        cls._configured = True

        logger.success("Logger initialized.")

    @classmethod
    def shutdown(cls) -> None:
        """
        Shutdown logger.
        """
        logger.info("Logger shutdown.")
        logger.remove()
        cls._configured = False


def configure_logger(
    log_directory: str | Path = "logs",
    log_level: str = "INFO",
    debug: bool = False,
) -> None:
    """
    Configure application logger.
    """

    LoggerManager.configure(
        log_directory=log_directory,
        log_level=log_level,
        debug=debug,
    )


def get_logger(name: Optional[str] = None):
    """
    Returns Loguru logger.

    Parameters
    ----------
    name
        Reserved for future use.

    Returns
    -------
    loguru.Logger
    """

    return logger


def shutdown_logger() -> None:
    """
    Shutdown logging system.
    """

    LoggerManager.shutdown()
