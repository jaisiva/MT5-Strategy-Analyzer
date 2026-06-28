"""
test_cli.py

CLI integration tests.
"""

from __future__ import annotations

import pytest

from mt5_analyzer.cli import run


class TestCLI:

    @pytest.mark.integration
    def test_original_command(
        self,
        sample_report_file,
        output_dir,
    ):

        output = output_dir / "original.xlsx"

        exit_code = run(

            [

                "original",

                "--input",

                str(sample_report_file),

                "--output",

                str(output),

            ]

        )

        assert exit_code == 0

        assert output.exists()

    # ------------------------------------------------------------

    @pytest.mark.integration
    def test_help(self):

        with pytest.raises(SystemExit):

            run(["--help"])
