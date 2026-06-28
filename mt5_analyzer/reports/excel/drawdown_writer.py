"""
drawdown_writer.py

Excel report writer for Drawdown Strategy.

Generates Excel workbook containing:

    • Summary
    • Statistics
    • Drawdown Cycles
    • Cycle Trades
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


class DrawdownReportWriter:
    """
    Excel writer for Drawdown Strategy reports.
    """

    def write(
        self,
        result: StrategyResult,
        output_file: str | Path,
    ) -> Path:
        """
        Generate Drawdown workbook.
        """

        workbook = ExcelWorkbook()

        self._write_summary(workbook, result)
        self._write_statistics(workbook, result)
        self._write_cycles(workbook, result)
        self._write_cycle_trades(workbook, result)
        self._write_monthly(workbook, result)
        self._write_yearly(workbook, result)

        # ---------------------------------------------------------
        # Workbook Formatting
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
        result: StrategyResult,
    ) -> None:

        sheet = workbook.add_sheet("Summary")

        stats = result.statistics

        TableBuilder(sheet).write_table(

            title="Drawdown Strategy Summary",

            data=[

                {

                    "Strategy": result.strategy_name,

                    "Trades": stats.total_trades,

                    "Wins": stats.winning_trades,

                    "Losses": stats.losing_trades,

                    "Net Profit": stats.net_profit,

                    "Gross Profit": stats.gross_profit,

                    "Gross Loss": stats.gross_loss,

                    "Profit Factor": stats.profit_factor,

                    "Expectancy": stats.expectancy,

                    "Maximum Drawdown": stats.max_drawdown,

                    "Peak Margin": stats.peak_margin,

                    "Capital Used": stats.capital_used,

                    "%ROE": stats.roe,

                    "Recovery Factor": stats.recovery_factor,

                }

            ],

        )

    # -------------------------------------------------------------

    def _write_statistics(
        self,
        workbook: ExcelWorkbook,
        result: StrategyResult,
    ) -> None:

        sheet = workbook.add_sheet("Statistics")

        TableBuilder(sheet).write_table(

            title="Strategy Statistics",

            data=[

                result.statistics.to_dict()

            ],

        )

    # -------------------------------------------------------------

    def _write_cycles(
        self,
        workbook: ExcelWorkbook,
        result: StrategyResult,
    ) -> None:

        sheet = workbook.add_sheet("Drawdown Cycles")

        data = []

        for cycle in getattr(result, "cycles", []):

            data.append(

                cycle.to_dict()

            )

        TableBuilder(sheet).write_table(

            title="Rolling Peak Drawdown Cycles",

            data=data,

        )

    # -------------------------------------------------------------

    def _write_cycle_trades(
        self,
        workbook: ExcelWorkbook,
        result: StrategyResult,
    ) -> None:

        sheet = workbook.add_sheet("Cycle Trades")

        rows = []

        for cycle in getattr(result, "cycles", []):

            for index, trade in enumerate(cycle.trades, start=1):

                record = trade.to_dict()

                record = {

                    "Cycle ID": cycle.cycle_id,

                    "Cycle Number": cycle.cycle_number,

                    "Trade #": index,

                    **record,

                }

                rows.append(record)

        TableBuilder(sheet).write_table(

            title="Trades by Drawdown Cycle",

            data=rows,

        )

    # -------------------------------------------------------------

    def _write_monthly(
        self,
        workbook: ExcelWorkbook,
        result: StrategyResult,
    ) -> None:

        sheet = workbook.add_sheet("Monthly")

        data = []

        if hasattr(result, "monthly_statistics"):

            data = [

                stat.to_dict()

                for stat in result.monthly_statistics.values()

            ]

        TableBuilder(sheet).write_table(

            title="Monthly Statistics",

            data=data,

        )

    # -------------------------------------------------------------

    def _write_yearly(
        self,
        workbook: ExcelWorkbook,
        result: StrategyResult,
    ) -> None:

        sheet = workbook.add_sheet("Yearly")

        data = []

        if hasattr(result, "yearly_statistics"):

            data = [

                stat.to_dict()

                for stat in result.yearly_statistics.values()

            ]

        TableBuilder(sheet).write_table(

            title="Yearly Statistics",

            data=data,

        )
