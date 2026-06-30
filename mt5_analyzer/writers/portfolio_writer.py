"""
portfolio_writer.py

Excel report writer for Portfolio Analysis.

Generates a professional Excel workbook containing

    • Portfolio Summary
    • Strategy Summary
    • Portfolio Monthly
    • Portfolio Yearly
    • Portfolio Trades

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
    Excel report writer for Portfolio Analysis.
    """

    # ---------------------------------------------------------

    def write(
        self,
        result: PortfolioResult,
        output_file: str | Path,
    ) -> Path:
        """
        Generate Portfolio workbook.

        Parameters
        ----------
        result

            PortfolioResult returned by PortfolioEngine.

        output_file

            Destination workbook.

        Returns
        -------
        Path
            Saved workbook.
        """

        workbook = ExcelWorkbook()

        #
        # Portfolio Summary
        #
        self._write_portfolio_summary(
            workbook,
            result,
        )

        #
        # Strategy Summary
        #
        self._write_strategy_summary(
            workbook,
            result,
        )

        #
        # Monthly
        #
        self._write_portfolio_monthly(
            workbook,
            result,
        )

        #
        # Yearly
        #
        self._write_portfolio_yearly(
            workbook,
            result,
        )

        #
        # Trades
        #
        self._write_portfolio_trades(
            workbook,
            result,
        )

        #
        # Workbook formatting
        #
        for sheet_name in workbook.sheet_names:

            sheet = workbook.workbook[
                sheet_name
            ]

            workbook.freeze_header(
                sheet
            )

            workbook.auto_fit(
                sheet
            )

        workbook.activate_sheet(
            "Portfolio Summary"
        )

        workbook.set_zoom(

            workbook.workbook[
                "Portfolio Summary"
            ],

            90,

        )

        return workbook.save(
            output_file
        )

    # ---------------------------------------------------------
    # Helper
    # ---------------------------------------------------------

    def _write_table_sheet(
        self,
        workbook: ExcelWorkbook,
        sheet_name: str,
        title: str,
        data: list[dict],
    ) -> None:
        """
        Generic worksheet writer.

        Used by all Portfolio worksheets.
        """

        sheet = workbook.add_sheet(
            sheet_name
        )

        builder = TableBuilder(
            sheet
        )

        builder.write_table(

            title=title,

            data=data,

        )

    # ---------------------------------------------------------
    # Worksheet writers
    # ---------------------------------------------------------

    def _write_portfolio_summary(
        self,
        workbook: ExcelWorkbook,
        result: PortfolioResult,
    ) -> None:
        """
        Implemented in Part-2.
        """
        ...

    # ---------------------------------------------------------

    def _write_strategy_summary(
        self,
        workbook: ExcelWorkbook,
        result: PortfolioResult,
    ) -> None:
        """
        Implemented in Part-3.
        """
        ...

    # ---------------------------------------------------------

    def _write_portfolio_monthly(
        self,
        workbook: ExcelWorkbook,
        result: PortfolioResult,
    ) -> None:
        """
        Implemented in Part-4.
        """
        ...

    # ---------------------------------------------------------

    def _write_portfolio_yearly(
        self,
        workbook: ExcelWorkbook,
        result: PortfolioResult,
    ) -> None:
        """
        Implemented in Part-4.
        """
        ...

    # ---------------------------------------------------------

    def _write_portfolio_trades(
        self,
        workbook: ExcelWorkbook,
        result: PortfolioResult,
    ) -> None:
        """
        Implemented in Part-5.
        """
        ...
		
    # ---------------------------------------------------------
    # Portfolio Summary
    # ---------------------------------------------------------

    def _write_portfolio_summary(
        self,
        workbook: ExcelWorkbook,
        result: PortfolioResult,
    ) -> None:
        """
        Write Portfolio Summary worksheet.

        One consolidated row representing the
        complete portfolio.
        """

        statistics = result.statistics

        #
        # Build worksheet data.
        #
        data = [

            {

                "Portfolio Trade Count":
                    statistics.trade_count,

                "Portfolio Wins":
                    statistics.wins,

                "Portfolio Losses":
                    statistics.losses,

                "Portfolio Peak Margin":
                    statistics.peak_margin,

                "Portfolio MDD":
                    statistics.maximum_drawdown,

                "Portfolio Avg P/L":
                    statistics.average_profit,

                "Portfolio Net P/L":
                    statistics.net_profit,

                "Portfolio Capital":
                    statistics.capital,

                "Portfolio %ROE":
                    statistics.return_on_equity,

            }

        ]

        self._write_table_sheet(

            workbook=workbook,

            sheet_name="Portfolio Summary",

            title="Portfolio Summary",

            data=data,

        )

    # ---------------------------------------------------------
    # Strategy Summary
    # ---------------------------------------------------------

    def _write_strategy_summary(
        self,
        workbook: ExcelWorkbook,
        result: PortfolioResult,
    ) -> None:
        """
        Write Strategy Summary worksheet.

        One row per strategy.

        Future versions may optionally expand this
        to one row per Strategy/Year/Month.
        """

        data: list[dict] = []

        for strategy_result in result.strategy_results:

            statistics = strategy_result.statistics

            #
            # Strategy level summary.
            #
            data.append(

                {

                    "Pattern":
                        strategy_result.strategy_name,

                    "Year":
                        "",

                    "Month":
                        "",

                    "Trade Count":
                        statistics.total_trades,

                    "Wins":
                        statistics.winning_trades,

                    "Losses":
                        statistics.losing_trades,

                    "Margin":
                        statistics.peak_margin,

                    "MDD":
                        statistics.max_drawdown,

                    "Avg P/L":
                        statistics.expectancy,

                    "Net P/L":
                        statistics.net_profit,

                    "Capital":
                        statistics.capital_used,

                    "%ROE":
                        statistics.roe,

                }

            )

        self._write_table_sheet(

            workbook=workbook,

            sheet_name="Strategy Summary",

            title="Strategy Summary",

            data=data,

        )
		
    # ---------------------------------------------------------
    # Portfolio Monthly
    # ---------------------------------------------------------

    def _write_portfolio_monthly(
        self,
        workbook: ExcelWorkbook,
        result: PortfolioResult,
    ) -> None:
        """
        Write Portfolio Monthly Summary.
        """

        data: list[dict] = []

        for (year, month), statistics in sorted(
            result.monthly_statistics.items()
        ):

            data.append(

                {

                    "Portfolio Year":
                        year,

                    "Portfolio Month":
                        month,

                    "Portfolio Trade Count":
                        statistics.trade_count,

                    "Portfolio Wins":
                        statistics.wins,

                    "Portfolio Losses":
                        statistics.losses,

                    "Portfolio Peak Margin":
                        statistics.peak_margin,

                    "Portfolio MDD":
                        statistics.maximum_drawdown,

                    "Portfolio Avg P/L":
                        statistics.average_profit,

                    "Portfolio Net P/L":
                        statistics.net_profit,

                    "Portfolio Capital":
                        statistics.capital,

                    "Portfolio %ROE":
                        statistics.return_on_equity,

                }

            )

        self._write_table_sheet(

            workbook=workbook,

            sheet_name="Portfolio Monthly",

            title="Portfolio Monthly Summary",

            data=data,

        )

    # ---------------------------------------------------------
    # Portfolio Yearly
    # ---------------------------------------------------------

    def _write_portfolio_yearly(
        self,
        workbook: ExcelWorkbook,
        result: PortfolioResult,
    ) -> None:
        """
        Write Portfolio Yearly Summary.
        """

        data: list[dict] = []

        for year, statistics in sorted(

            result.yearly_statistics.items()

        ):

            data.append(

                {

                    "Portfolio Year":
                        year,

                    "Portfolio Trade Count":
                        statistics.trade_count,

                    "Portfolio Wins":
                        statistics.wins,

                    "Portfolio Losses":
                        statistics.losses,

                    "Portfolio Peak Margin":
                        statistics.peak_margin,

                    "Portfolio MDD":
                        statistics.maximum_drawdown,

                    "Portfolio Avg P/L":
                        statistics.average_profit,

                    "Portfolio Net P/L":
                        statistics.net_profit,

                    "Portfolio Capital":
                        statistics.capital,

                    "Portfolio %ROE":
                        statistics.return_on_equity,

                }

            )

        self._write_table_sheet(

            workbook=workbook,

            sheet_name="Portfolio Yearly",

            title="Portfolio Yearly Summary",

            data=data,

        )
		
    # ---------------------------------------------------------
    # Portfolio Trades
    # ---------------------------------------------------------

    def _write_portfolio_trades(
        self,
        workbook: ExcelWorkbook,
        result: PortfolioResult,
    ) -> None:
        """
        Write Portfolio Trades worksheet.
        """

        data: list[dict] = []

        for portfolio_trade in result.portfolio_trades:

            trade = portfolio_trade.trade

            data.append(

                {

                    "Strategy":
                        portfolio_trade.strategy,

                    "Trade No":
                        trade.trade_number,

                    "Symbol":
                        trade.symbol,

                    "Entry Date":
                        trade.entry_date,

                    "Entry Time":
                        trade.entry_time,

                    "Exit Date":
                        trade.exit_date,

                    "Exit Time":
                        trade.exit_time,

                    "Volume":
                        trade.volume,

                    "Entry Type":
                        trade.entry_type,

                    "Exit Type":
                        trade.exit_type,

                    "Open Price":
                        trade.open_price,

                    "SL":
                        trade.stop_loss,

                    "TP":
                        trade.take_profit,

                    "Profit":
                        trade.net_profit,

                }

            )

        self._write_table_sheet(

            workbook,

            "Portfolio Trades",

            "Portfolio Trades",

            data,

        )
