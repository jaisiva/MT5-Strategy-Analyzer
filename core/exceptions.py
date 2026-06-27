"""
exceptions.py

Custom exception hierarchy for MT5 Strategy Analyzer.

Every module in the application should raise one of these exceptions
instead of built-in exceptions wherever possible.

Author:
    MT5 Strategy Analyzer

License:
    MIT
"""

from __future__ import annotations


class MT5AnalyzerError(Exception):
    """
    Base exception for the entire application.
    """

    def __init__(self, message: str = "MT5 Analyzer Error") -> None:
        self.message = message
        super().__init__(message)


# ============================================================================
# Configuration
# ============================================================================

class ConfigurationError(MT5AnalyzerError):
    """
    Raised when configuration files are invalid or missing.
    """


# ============================================================================
# Loader
# ============================================================================

class LoaderError(MT5AnalyzerError):
    """
    Raised while loading MT5 reports.
    """


class UnsupportedFileFormatError(LoaderError):
    """
    Raised when the input file format is unsupported.
    """


class FileReadError(LoaderError):
    """
    Raised when a report cannot be opened.
    """


# ============================================================================
# Validation
# ============================================================================

class ValidationError(MT5AnalyzerError):
    """
    Base validation exception.
    """


class MissingColumnError(ValidationError):
    """
    Raised when a required MT5 column is missing.
    """

    def __init__(self, column_name: str) -> None:
        super().__init__(f"Required column '{column_name}' is missing.")
        self.column_name = column_name


class InvalidTradeError(ValidationError):
    """
    Raised when an invalid trade record is detected.
    """


class InvalidDateError(ValidationError):
    """
    Raised when an invalid date/time is encountered.
    """


class DuplicateTradeError(ValidationError):
    """
    Raised when duplicate trades are detected.
    """


class InvalidVolumeError(ValidationError):
    """
    Raised when trade volume is invalid.
    """


class InvalidProfitError(ValidationError):
    """
    Raised when trade profit cannot be parsed.
    """


# ============================================================================
# Pattern Engine
# ============================================================================

class PatternEngineError(MT5AnalyzerError):
    """
    Raised while generating L-pattern strategies.
    """


# ============================================================================
# Session Engine
# ============================================================================

class SessionEngineError(MT5AnalyzerError):
    """
    Raised while assigning trading sessions.
    """


# ============================================================================
# Drawdown Engine
# ============================================================================

class DrawdownEngineError(MT5AnalyzerError):
    """
    Raised while processing drawdown cycles.
    """


# ============================================================================
# Portfolio
# ============================================================================

class PortfolioError(MT5AnalyzerError):
    """
    Raised while building portfolio statistics.
    """


# ============================================================================
# Reports
# ============================================================================

class ReportGenerationError(MT5AnalyzerError):
    """
    Raised when report generation fails.
    """


class ExcelWriterError(ReportGenerationError):
    """
    Raised while writing Excel workbooks.
    """


# ============================================================================
# CLI
# ============================================================================

class CLIError(MT5AnalyzerError):
    """
    Raised for command-line interface errors.
    """


# ============================================================================
# Internal
# ============================================================================

class InternalApplicationError(MT5AnalyzerError):
    """
    Unexpected internal application error.
    """
