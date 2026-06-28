"""
test_validator.py

Unit tests for TradeValidator.

Author:
    MT5 Strategy Analyzer

License:
    MIT
"""

from __future__ import annotations

from datetime import timedelta

import pytest

from mt5_analyzer.core.exceptions import ValidationError
from mt5_analyzer.core.validator import TradeValidator
from mt5_analyzer.domain.enums import Direction


class TestTradeValidator:
    """
    Unit tests for TradeValidator.
    """

    def setup_method(self) -> None:
        """
        Create validator instance.
        """

        self.validator = TradeValidator()

    # ------------------------------------------------------------------

    @pytest.mark.unit
    def test_valid_trade(
        self,
        sample_trade,
    ) -> None:
        """
        A valid trade should pass validation.
        """

        self.validator.validate(sample_trade)

    # ------------------------------------------------------------------

    @pytest.mark.unit
    def test_missing_ticket(
        self,
        trade_factory,
    ) -> None:
        """
        Missing ticket should fail validation.
        """

        trade = trade_factory()

        trade.ticket = None

        with pytest.raises(ValidationError):

            self.validator.validate(trade)

    # ------------------------------------------------------------------

    @pytest.mark.unit
    def test_missing_symbol(
        self,
        trade_factory,
    ) -> None:
        """
        Empty symbol should fail validation.
        """

        trade = trade_factory()

        trade.symbol = ""

        with pytest.raises(ValidationError):

            self.validator.validate(trade)

    # ------------------------------------------------------------------

    @pytest.mark.unit
    def test_negative_volume(
        self,
        trade_factory,
    ) -> None:
        """
        Negative volume should fail validation.
        """

        trade = trade_factory()

        trade.volume = -0.01

        with pytest.raises(ValidationError):

            self.validator.validate(trade)

    # ------------------------------------------------------------------

    @pytest.mark.unit
    def test_zero_volume(
        self,
        trade_factory,
    ) -> None:
        """
        Zero volume should fail validation.
        """

        trade = trade_factory()

        trade.volume = 0

        with pytest.raises(ValidationError):

            self.validator.validate(trade)

    # ------------------------------------------------------------------

    @pytest.mark.unit
    def test_entry_after_exit(
        self,
        trade_factory,
    ) -> None:
        """
        Entry time after exit time should fail.
        """

        trade = trade_factory()

        trade.entry_time = trade.exit_time + timedelta(hours=1)

        with pytest.raises(ValidationError):

            self.validator.validate(trade)

    # ------------------------------------------------------------------

    @pytest.mark.unit
    def test_invalid_direction(
        self,
        trade_factory,
    ) -> None:
        """
        Invalid direction should fail validation.
        """

        trade = trade_factory()

        trade.direction = "LONG"

        with pytest.raises(ValidationError):

            self.validator.validate(trade)

    # ------------------------------------------------------------------

    @pytest.mark.unit
    def test_nan_profit(
        self,
        trade_factory,
    ) -> None:
        """
        NaN profit should fail validation.
        """

        trade = trade_factory()

        trade.net_profit = float("nan")

        with pytest.raises(ValidationError):

            self.validator.validate(trade)

    # ------------------------------------------------------------------

    @pytest.mark.unit
    def test_infinite_profit(
        self,
        trade_factory,
    ) -> None:
        """
        Infinite profit should fail validation.
        """

        trade = trade_factory()

        trade.net_profit = float("inf")

        with pytest.raises(ValidationError):

            self.validator.validate(trade)

    # ------------------------------------------------------------------

    @pytest.mark.unit
    def test_zero_profit(
        self,
        trade_factory,
    ) -> None:
        """
        Zero-profit trade should be valid.
        """

        trade = trade_factory()

        trade.net_profit = 0.0

        self.validator.validate(trade)

    # ------------------------------------------------------------------

    @pytest.mark.unit
    def test_zero_commission(
        self,
        trade_factory,
    ) -> None:
        """
        Zero commission should be valid.
        """

        trade = trade_factory()

        trade.commission = 0.0

        self.validator.validate(trade)

    # ------------------------------------------------------------------

    @pytest.mark.unit
    def test_zero_swap(
        self,
        trade_factory,
    ) -> None:
        """
        Zero swap should be valid.
        """

        trade = trade_factory()

        trade.swap = 0.0

        self.validator.validate(trade)

    # ------------------------------------------------------------------

    @pytest.mark.unit
    def test_large_profit(
        self,
        trade_factory,
    ) -> None:
        """
        Very large profits should still be valid.
        """

        trade = trade_factory()

        trade.net_profit = 1_000_000.0

        self.validator.validate(trade)

    # ------------------------------------------------------------------

    @pytest.mark.unit
    def test_small_lot_size(
        self,
        trade_factory,
    ) -> None:
        """
        Small lot sizes should be valid.
        """

        trade = trade_factory()

        trade.volume = 0.01

        self.validator.validate(trade)
