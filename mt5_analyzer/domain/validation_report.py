"""
validation_report.py

Domain model representing the results of validating an MT5 report.

This model is returned by the Validator and consumed by the CLI,
GUI, Loader, and unit tests.

Author:
    MT5 Strategy Analyzer

License:
    MIT
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True, frozen=True)
class ValidationMessage:
    """
    Represents a single validation message.
    """

    row: int | None
    column: str | None
    message: str


@dataclass(slots=True)
class ValidationReport:
    """
    Validation summary for an MT5 report.
    """

    total_rows: int = 0

    valid_rows: int = 0

    invalid_rows: int = 0

    warnings: list[ValidationMessage] = field(default_factory=list)

    errors: list[ValidationMessage] = field(default_factory=list)

    # ------------------------------------------------------------------
    # Properties
    # ------------------------------------------------------------------

    @property
    def passed(self) -> bool:
        """
        Returns True if validation passed.
        """
        return len(self.errors) == 0

    @property
    def warning_count(self) -> int:
        """
        Number of warnings.
        """
        return len(self.warnings)

    @property
    def error_count(self) -> int:
        """
        Number of errors.
        """
        return len(self.errors)

    # ------------------------------------------------------------------
    # Methods
    # ------------------------------------------------------------------

    def add_warning(
        self,
        message: str,
        row: int | None = None,
        column: str | None = None,
    ) -> None:
        """
        Add validation warning.
        """

        self.warnings.append(
            ValidationMessage(
                row=row,
                column=column,
                message=message,
            )
        )

    def add_error(
        self,
        message: str,
        row: int | None = None,
        column: str | None = None,
    ) -> None:
        """
        Add validation error.
        """

        self.errors.append(
            ValidationMessage(
                row=row,
                column=column,
                message=message,
            )
        )

    def merge(self, other: "ValidationReport") -> None:
        """
        Merge another validation report.
        """

        self.total_rows += other.total_rows
        self.valid_rows += other.valid_rows
        self.invalid_rows += other.invalid_rows

        self.warnings.extend(other.warnings)
        self.errors.extend(other.errors)

    def summary(self) -> str:
        """
        Returns human-readable validation summary.
        """

        status = "PASSED" if self.passed else "FAILED"

        return (
            f"Validation {status}\n"
            f"---------------------------\n"
            f"Total Rows   : {self.total_rows}\n"
            f"Valid Rows   : {self.valid_rows}\n"
            f"Invalid Rows : {self.invalid_rows}\n"
            f"Warnings     : {self.warning_count}\n"
            f"Errors       : {self.error_count}"
        )

    def to_dict(self) -> dict:
        """
        Convert validation report to dictionary.
        """

        return {
            "total_rows": self.total_rows,
            "valid_rows": self.valid_rows,
            "invalid_rows": self.invalid_rows,
            "warnings": self.warning_count,
            "errors": self.error_count,
            "passed": self.passed,
        }

    def __str__(self) -> str:
        return self.summary()
