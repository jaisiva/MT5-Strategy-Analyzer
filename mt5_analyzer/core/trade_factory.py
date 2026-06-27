"""
trade_factory.py

Factory responsible for creating immutable Trade domain objects.

The TradeFactory converts validated data into Trade instances.
It does not perform validation; all input is assumed to have been
validated by Validator.

Author:
    MT5 Strategy Analyzer

License:
    MIT
"""

from __future__ import annotations

from datetime import datetime
from typing import Any

from mt5_analyzer.domain.enums import PatternType, SessionType, TradeSide
from mt5_analyzer.domain.trade import Trade


class TradeFactory:
    """
    Factory for creating Trade objects.
    """

    DATE_FORMATS = (
        "%Y-%m-%d",
        "%d/%m/%Y",
        "%d-%m-%Y",
        "%m/%d/%Y",
    )

    TIME_FORMATS = (
        "%H:%M",
        "%H:%M:%S",
    )

    @classmethod
    def create(
        cls,
        *,
        ticket: int | None,
        symbol: str,
        side: str | TradeSide,
        volume: float,
        entry_date: Any,
        entry_time: Any,
        exit_date: Any,
        exit_time: Any,
        profit: float,
        commission: float = 0.0,
        swap: float = 0.0,
        pattern: PatternType = PatternType.ORIGINAL,
        session: SessionType | None = None,
    ) -> Trade:
        """
        Create a Trade instance.
        """

        return Trade(
            ticket=ticket,
            symbol=str(symbol).strip(),
            side=cls._parse_side(side),
            volume=float(volume),
            entry_time=cls._combine_datetime(entry_date, entry_time),
            exit_time=cls._combine_datetime(exit_date, exit_time),
            profit=float(profit),
            commission=float(commission),
            swap=float(swap),
            pattern=pattern,
            session=session,
        )

    @classmethod
    def create_from_mapping(cls, row: dict[str, Any]) -> Trade:
        """
        Create Trade from a mapping.

        Expected keys are canonical names produced by the loader.
        """

        return cls.create(
            ticket=row.get("ticket"),
            symbol=row["symbol"],
            side=row["side"],
            volume=row["volume"],
            entry_date=row["entry_date"],
            entry_time=row["entry_time"],
            exit_date=row["exit_date"],
            exit_time=row["exit_time"],
            profit=row["profit"],
            commission=row.get("commission", 0.0),
            swap=row.get("swap", 0.0),
        )

    @staticmethod
    def _parse_side(side: str | TradeSide) -> TradeSide:
        """
        Convert string into TradeSide enum.
        """

        if isinstance(side, TradeSide):
            return side

        return TradeSide.from_string(side)

    @classmethod
    def _combine_datetime(
        cls,
        date_value: Any,
        time_value: Any,
    ) -> datetime:
        """
        Combine date and time values into datetime.
        """

        if isinstance(date_value, datetime):
            return date_value

        date_text = str(date_value).strip()
        time_text = str(time_value).strip()

        for date_fmt in cls.DATE_FORMATS:

            try:

                date_part = datetime.strptime(
                    date_text,
                    date_fmt,
                ).date()

                break

            except ValueError:
                continue

        else:
            raise ValueError(
                f"Unsupported date format: {date_text}"
            )

        for time_fmt in cls.TIME_FORMATS:

            try:

                time_part = datetime.strptime(
                    time_text,
                    time_fmt,
                ).time()

                break

            except ValueError:
                continue

        else:
            raise ValueError(
                f"Unsupported time format: {time_text}"
            )

        return datetime.combine(
            date_part,
            time_part,
        )
