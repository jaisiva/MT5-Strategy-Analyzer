"""
test_trade_factory.py

Unit tests for TradeFactory.

Author:
    MT5 Strategy Analyzer

License:
    MIT
"""

from __future__ import annotations

from datetime import datetime

import pytest

from mt5_analyzer.core.exceptions import ValidationError
from mt5_analyzer.core.trade_factory import TradeFactory
from mt5_analyzer.domain.enums import (
    Direction,
    PatternType,
    SessionType,
)
from mt5_analyzer.domain.trade import Trade


class TestTradeFactory:
    """
    Unit tests for TradeFactory.
    """

    def setup_method(self) -> None:
        """
        Create factory instance.
        """

        self.factory = TradeFactory()

    # ------------------------------------------------------------------

    @pytest.fixture
    def valid_row(self) -> dict:
        """
        Valid MT5 trade row.
        """

        return {

            "Ticket": 1001,

            "Symbol": "XAUUSD",

            "Direction": "BUY",

            "Volume": 0.01,

            "Entry Time": datetime(
                2024,
                1,
                1,
                9,
                0,
            ),

            "Exit Time": datetime(
                2024,
                1,
                1,
                10,
                0,
            ),

            "Entry Price": 2000.0,

            "Exit Price": 2010.0,

            "Stop Loss": 1990.0,

            "Take Profit": 2020.0,

            "Commission": 0.0,

            "Swap": 0.0,

            "Net Profit": 10.0,

        }

    # ------------------------------------------------------------------

    @pytest.mark.unit
    def test_create_trade(
        self,
        valid_row,
    ) -> None:
        """
        Factory should create Trade object.
        """

        trade = self.factory.create(
            valid_row,
        )

        assert isinstance(
            trade,
            Trade,
        )

    # ------------------------------------------------------------------

    @pytest.mark.unit
    def test_ticket_mapping(
        self,
        valid_row,
    ) -> None:
        """
        Ticket should be mapped correctly.
        """

        trade = self.factory.create(valid_row)

        assert trade.ticket == 1001

    # ------------------------------------------------------------------

    @pytest.mark.unit
    def test_symbol_mapping(
        self,
        valid_row,
    ) -> None:
        """
        Symbol should be mapped correctly.
        """

        trade = self.factory.create(valid_row)

        assert trade.symbol == "XAUUSD"

    # ------------------------------------------------------------------

    @pytest.mark.unit
    def test_direction_mapping(
        self,
        valid_row,
    ) -> None:
        """
        BUY should map to Direction.BUY.
        """

        trade = self.factory.create(valid_row)

        assert trade.direction is Direction.BUY

    # ------------------------------------------------------------------

    @pytest.mark.unit
    def test_sell_mapping(
        self,
        valid_row,
    ) -> None:
        """
        SELL should map to Direction.SELL.
        """

        valid_row["Direction"] = "SELL"

        trade = self.factory.create(valid_row)

        assert trade.direction is Direction.SELL

    # ------------------------------------------------------------------

    @pytest.mark.unit
    def test_invalid_direction(
        self,
        valid_row,
    ) -> None:
        """
        Unknown direction should raise ValidationError.
        """

        valid_row["Direction"] = "LONG"

        with pytest.raises(ValidationError):

            self.factory.create(valid_row)

    # ------------------------------------------------------------------

    @pytest.mark.unit
    def test_numeric_conversion(
        self,
        valid_row,
    ) -> None:
        """
        Numeric values should be converted correctly.
        """

        trade = self.factory.create(valid_row)

        assert trade.volume == pytest.approx(0.01)

        assert trade.entry_price == pytest.approx(2000.0)

        assert trade.exit_price == pytest.approx(2010.0)

        assert trade.net_profit == pytest.approx(10.0)

    # ------------------------------------------------------------------

    @pytest.mark.unit
    def test_datetime_mapping(
        self,
        valid_row,
    ) -> None:
        """
        Datetime fields should be mapped correctly.
        """

        trade = self.factory.create(valid_row)

        assert trade.entry_time < trade.exit_time

    # ------------------------------------------------------------------

    @pytest.mark.unit
    def test_default_pattern(
        self,
        valid_row,
    ) -> None:
        """
        Pattern should default to NONE.
        """

        trade = self.factory.create(valid_row)

        assert trade.pattern is PatternType.NONE

    # ------------------------------------------------------------------

    @pytest.mark.unit
    def test_default_session(
        self,
        valid_row,
    ) -> None:
        """
        Session should be initialized.
        """

        trade = self.factory.create(valid_row)

        assert isinstance(
            trade.session,
            SessionType,
        )

    # ------------------------------------------------------------------

    @pytest.mark.unit
    def test_missing_required_field(
        self,
        valid_row,
    ) -> None:
        """
        Missing required field should raise ValidationError.
        """

        del valid_row["Ticket"]

        with pytest.raises(ValidationError):

            self.factory.create(valid_row)
