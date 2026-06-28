"""
main.py

Application entry point.

Author:
    MT5 Strategy Analyzer

License:
    MIT
"""

from __future__ import annotations

import sys

from mt5_analyzer.cli import run


def main() -> int:
    """
    Application entry point.
    """

    return run()


if __name__ == "__main__":

    sys.exit(main())
