"""
portfolio_writer.py

Excel report writer for Portfolio Analysis.

Generates Excel workbook containing:

    Summary
    Strategy Comparison
    Portfolio Statistics
    Combined Trades
    Monthly Statistics
    Yearly Statistics

Author:
    MT5 Strategy Analyzer

License:
    MIT
"""

from __future__ import annotations

from pathlib import Path

from mt5_analyzer.domain.portfolio_result import PortfolioResult
from mt5_analyzer.reports.excel.table_builder import TableBuilder
from mt5_analyzer.reports.excel.workbook import ExcelWorkbook


class PortfolioReportWriter:
    """
    Excel writer for portfolio analysis.
    """

    def write(
        self,
        result: PortfolioResult,
        output_file: str | Path,
    ) -> Path:
        """
        Generate portfolio workbook.
        """

        workbook = ExcelWorkbook()

        self._write_summary(
            workbook,
            result,
        )

        self._write_strategy_comparison(
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

        # ---------------------------------------------------------
        # Format Workbook
        # ---------------------------------------------------------

        for sheet_name in workbook.sheet_names:

            sheet = workbook.workbook[sheet_name]

            workbook.freeze_header(sheet)

            workbook.auto_fit(sheet)

        workbook.activate_sheet("Summary")

        workbook.set_zoom(
            workbook.workbook["Summary"],
            90,
        )

        return workbook.save(output_file)

    # -------------------------------------------------------------

    def _write_summary(
        self,
        workbook: ExcelWorkbook,
        result: PortfolioResult,
    ) -> None:

        sheet = workbook.add_sheet(
            "Summary"
        )

        builder = TableBuilder(sheet)

        builder.write_table(

            title="Portfolio Summary",

            data=[

                {
                    "Portfolio": result.portfolio_name,
                    "Description": result.description,
                    "Strategies": result.strategy_count,
                    "Trades": result.trade_count,
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

    def _write_strategy_comparison(
        self,
        workbook: ExcelWorkbook,
        result: PortfolioResult,
    ) -> None:

        sheet = workbook.add_sheet(
            "Strategy Comparison"
        )

        data = []

        for strategy in result.strategies:

            stats = strategy.statistics

            data.append(

                {

                    "Strategy": strategy.strategy_name,

                    "Trades": stats.total_trades,

                    "Wins": stats.winning_trades,

                    "Losses": stats.losing_trades,

                    "Net Profit": stats.net_profit,

                    "MDD": stats.max_drawdown,

                    "Peak Margin": stats.peak_margin,

                    "Capital Used": stats.capital_used,

                    "%ROE": stats.roe,

                    "Profit Factor": stats.profit_factor,

                }

            )

        TableBuilder(sheet).write_table(

            title="Strategy Comparison",

            data=data,

        )

    # -------------------------------------------------------------

    def _write_statistics(
        self,
        workbook: ExcelWorkbook,
        result: PortfolioResult,
    ) -> None:

        sheet = workbook.add_sheet(
            "Portfolio Statistics"
        )

        TableBuilder(sheet).write_table(

            title="Portfolio Statistics",

            data=[
                result.statistics.to_dict()
            ],

        )

    # -------------------------------------------------------------

    def _write_trades(
        self,
        workbook: ExcelWorkbook,
        result: PortfolioResult,
    ) -> None:

        sheet = workbook.add_sheet(
            "Combined Trades"
        )

        TableBuilder(sheet).write_table(

            title="Combined Trade List",

            data=[
                trade.to_dict()
                for trade in result.trades
            ],

        )

    # -------------------------------------------------------------

    def _write_monthly(
        self,
        workbook: ExcelWorkbook,
        result: PortfolioResult,
    ) -> None:

        sheet = workbook.add_sheet(
            "Monthly"
        )

        data = [

            stats.to_dict()

            for stats in result.monthly_statistics.values()

        ]

        TableBuilder(sheet).write_table(

            title="Monthly Statistics",

            data=data,

        )

    # -------------------------------------------------------------

    def _write_yearly(
        self,
        workbook: ExcelWorkbook,
        result: PortfolioResult,
    ) -> None:

        sheet = workbook.add_sheet(
            "Yearly"
        )

        data = [

            stats.to_dict()

            for stats in result.yearly_statistics.values()

        ]

        TableBuilder(sheet).write_table(

            title="Yearly Statistics",

            data=data,

        )
