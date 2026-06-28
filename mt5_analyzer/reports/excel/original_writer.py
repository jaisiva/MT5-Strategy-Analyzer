"""
original_writer.py

Excel report writer for the Original Strategy.

Generates a professional Excel workbook containing:

    • Summary
    • Statistics
    • Trade List
    • Monthly Statistics
    • Yearly Statistics

Author:
    MT5 Strategy Analyzer

License:
    MIT
"""

from __future__ import annotations

from pathlib import Path

from mt5_analyzer.domain.strategy_result import StrategyResult
from mt5_analyzer.reports.excel.table_builder import TableBuilder
from mt5_analyzer.reports.excel.workbook import ExcelWorkbook


class OriginalReportWriter:
    """
    Excel report writer for Original Strategy.
    """

    def write(
        self,
        result: StrategyResult,
        output_file: str | Path,
    ) -> Path:
        """
        Generate Original Strategy workbook.

        Parameters
        ----------
        result
            StrategyResult returned by OriginalStrategyEngine.

        output_file
            Destination workbook.

        Returns
        -------
        Path
            Saved workbook.
        """

        workbook = ExcelWorkbook()

        self._write_summary(
            workbook,
            result,
        )

        self._write_statistics(
            workbook,
            result,
        )

        self._write_trades(
            workbook,
            result,
        )

        self._write_monthly(
            workbook,
            result,
        )

        self._write_yearly(
            workbook,
            result,
        )

        # Apply workbook formatting
        for sheet_name in workbook.sheet_names:

            sheet = workbook.workbook[sheet_name]

            workbook.freeze_header(sheet)

            workbook.auto_fit(sheet)

        workbook.activate_sheet(
            "Summary"
        )

        workbook.set_zoom(
            workbook.workbook["Summary"],
            90,
        )

        return workbook.save(output_file)

    # -------------------------------------------------------------

    def _write_summary(
        self,
        workbook: ExcelWorkbook,
        result: StrategyResult,
    ) -> None:

        sheet = workbook.add_sheet(
            "Summary"
        )

        builder = TableBuilder(sheet)

        builder.write_table(

            title="Strategy Summary",

            data=[
                {
                    "Strategy": result.strategy_name,
                    "Trades": result.statistics.total_trades,
                    "Wins": result.statistics.winning_trades,
                    "Losses": result.statistics.losing_trades,
                    "Net Profit": result.statistics.net_profit,
                    "Gross Profit": result.statistics.gross_profit,
                    "Gross Loss": result.statistics.gross_loss,
                    "Profit Factor": result.statistics.profit_factor,
                    "Expectancy": result.statistics.expectancy,
                    "MDD": result.statistics.max_drawdown,
                    "Peak Margin": result.statistics.peak_margin,
                    "Capital Used": result.statistics.capital_used,
                    "%ROE": result.statistics.roe,
                }
            ],

        )

    # -------------------------------------------------------------

    def _write_statistics(
        self,
        workbook: ExcelWorkbook,
        result: StrategyResult,
    ) -> None:

        sheet = workbook.add_sheet(
            "Statistics"
        )

        builder = TableBuilder(sheet)

        builder.write_table(

            title="Statistics",

            data=[
                result.statistics.to_dict()
            ],

        )

    # -------------------------------------------------------------

    def _write_trades(
        self,
        workbook: ExcelWorkbook,
        result: StrategyResult,
    ) -> None:

        sheet = workbook.add_sheet(
            "Trades"
        )

        builder = TableBuilder(sheet)

        builder.write_table(

            title="Trade List",

            data=[
                trade.to_dict()
                for trade in result.trades
            ],

        )

    # -------------------------------------------------------------

    def _write_monthly(
        self,
        workbook: ExcelWorkbook,
        result: StrategyResult,
    ) -> None:

        sheet = workbook.add_sheet(
            "Monthly"
        )

        builder = TableBuilder(sheet)

        if hasattr(result, "monthly_statistics"):

            data = [
                stat.to_dict()
                for stat in result.monthly_statistics.values()
            ]

        else:

            data = []

        builder.write_table(

            title="Monthly Statistics",

            data=data,

        )

    # -------------------------------------------------------------

    def _write_yearly(
        self,
        workbook: ExcelWorkbook,
        result: StrategyResult,
    ) -> None:

        sheet = workbook.add_sheet(
            "Yearly"
        )

        builder = TableBuilder(sheet)

        if hasattr(result, "yearly_statistics"):

            data = [
                stat.to_dict()
                for stat in result.yearly_statistics.values()
            ]

        else:

            data = []

        builder.write_table(

            title="Yearly Statistics",

            data=data,

        )
