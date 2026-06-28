"""
session_engine.py

Trading session assignment and filtering.

Supported sessions

    Asia
    Europe
    US Overlap
    Late US

Author:
    MT5 Strategy Analyzer

License:
    MIT
"""

from __future__ import annotations

from dataclasses import replace
from datetime import time

from mt5_analyzer.domain.enums import SessionType
from mt5_analyzer.domain.trade import Trade


class SessionEngine:
    """
    Assigns and filters trading sessions.
    """

    # ------------------------------------------------------------
    # Default Session Definitions
    #
    # These can later be loaded from ConfigManager.
    # ------------------------------------------------------------

    ASIA_START = time(0, 0)
    ASIA_END = time(8, 0)

    EUROPE_START = time(8, 0)
    EUROPE_END = time(13, 0)

    US_OVERLAP_START = time(13, 0)
    US_OVERLAP_END = time(17, 0)

    LATE_US_START = time(17, 0)
    LATE_US_END = time(23, 59, 59)

    # ------------------------------------------------------------

    def assign_sessions(
        self,
        trades: list[Trade],
    ) -> list[Trade]:
        """
        Assign trading session to every trade.
        """

        result: list[Trade] = []

        for trade in trades:

            session = self._determine_session(
                trade.entry_time.time()
            )

            result.append(
                replace(
                    trade,
                    session=session,
                )
            )

        return result

    # ------------------------------------------------------------

    def filter_sessions(
        self,
        trades: list[Trade],
        sessions: list[SessionType],
    ) -> list[Trade]:
        """
        Filter trades belonging to selected sessions.
        """

        if not sessions:
            return list(trades)

        allowed = set(sessions)

        return [
            trade
            for trade in trades
            if trade.session in allowed
        ]

    # ------------------------------------------------------------

    def assign_and_filter(
        self,
        trades: list[Trade],
        sessions: list[SessionType],
    ) -> list[Trade]:
        """
        Convenience method.

        Assign sessions then filter.
        """

        assigned = self.assign_sessions(
            trades
        )

        return self.filter_sessions(
            assigned,
            sessions,
        )

    # ------------------------------------------------------------

    @classmethod
    def _determine_session(
        cls,
        value: time,
    ) -> SessionType:
        """
        Determine trading session.
        """

        if cls.ASIA_START <= value < cls.ASIA_END:
            return SessionType.ASIA

        if cls.EUROPE_START <= value < cls.EUROPE_END:
            return SessionType.EUROPE

        if cls.US_OVERLAP_START <= value < cls.US_OVERLAP_END:
            return SessionType.US_OVERLAP

        return SessionType.LATE_US
