"""
column_mapper.py

Maps MT5 report column names to MT5 Strategy Analyzer's internal
canonical column names.

Different MT5 versions and brokers may export different column names.
This module provides a single place to normalize them.

Author:
    MT5 Strategy Analyzer

License:
    MIT
"""

from __future__ import annotations

from typing import Dict, List

from mt5_analyzer.core.exceptions import MissingColumnError


class ColumnMapper:
    """
    Maps MT5 report columns to the application's internal schema.
    """

    # ----------------------------------------------------------------------
    # Canonical Column Mapping
    # ----------------------------------------------------------------------

    COLUMN_ALIASES: Dict[str, List[str]] = {

        # Entry Date
        "entry_date": [
            "entry_date",
            "Entry Date",
            "Open Date",
            "Date",
        ],

        # Entry Time
        "entry_time": [
            "entry_time",
            "Entry Time",
            "Open Time",
            "Time",
        ],

        # Exit Date
        "exit_date": [
            "exit_date",
            "Exit Date",
            "Close Date",
        ],

        # Exit Time
        "exit_time": [
            "exit_time",
            "Exit Time",
            "Close Time",
        ],

        # Symbol
        "symbol": [
            "Symbol",
            "Instrument",
        ],

        # Side
        "side": [
            "Type",
            "Entry Type",
            "Direction",
            "Side",
            "Trade Type",
        ],

        # Volume
        "volume": [
            "Volume",
            "Lots",
            "Lot",
        ],

        # Profit
        "profit": [
            "Profit",
            "P/L",
            "Net Profit",
        ],

        # Commission
        "commission": [
            "Commission",
        ],

        # Swap
        "swap": [
            "Swap",
        ],

        # Ticket
        "ticket": [
            "Ticket",
            "Trade No",
            "Order",
            "Position",
        ],
    }

    # Required fields for analysis
    REQUIRED_COLUMNS = [
        "entry_date",
        "entry_time",
        "exit_date",
        "exit_time",
        "symbol",
        "side",
        "volume",
        "profit",
    ]

    @classmethod
    def map_columns(cls, columns: List[str]) -> Dict[str, str]:
        """
        Map MT5 column names to internal names.

        Parameters
        ----------
        columns
            List of columns from the MT5 report.

        Returns
        -------
        Dict[str, str]

            Example

            {
                "Entry Date": "entry_date",
                "Profit": "profit"
            }
        """

        mapping: Dict[str, str] = {}

        for canonical, aliases in cls.COLUMN_ALIASES.items():

            for alias in aliases:

                if alias in columns:
                    mapping[alias] = canonical
                    break

        return mapping

    @classmethod
    def validate_columns(cls, columns: List[str]) -> None:
        """
        Validate required MT5 columns exist.
        """

        mapping = cls.map_columns(columns)

        mapped_columns = set(mapping.values())

        for required in cls.REQUIRED_COLUMNS:

            if required not in mapped_columns:
                raise MissingColumnError(required)

    @classmethod
    def rename_mapping(cls, columns: List[str]) -> Dict[str, str]:
        """
        Returns dictionary suitable for pandas.DataFrame.rename()

        Example
        -------

        {
            "Entry Date": "entry_date",
            "Profit": "profit"
        }
        """

        return cls.map_columns(columns)

    @classmethod
    def canonical_columns(cls) -> List[str]:
        """
        Return all canonical column names.
        """

        return list(cls.COLUMN_ALIASES.keys())
