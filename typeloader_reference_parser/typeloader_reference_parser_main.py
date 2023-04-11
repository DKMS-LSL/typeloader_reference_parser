#!/usr/bin/env python3
"""Created on 2023-04-11.

This script does ...

@author: Bianca Schöne
"""

# import modules:
import logging
import sys

from pathlib import Path

sys.path.append(r"T:\Skripte\_Module_\pylib3\lslcommons\lslcommons-loggerutils")

from lslcommons.loggerutils import LoggerSetup  # noqa: E402

try:
    from __init__ import __version__
except ImportError:
    from typeloader_reference_parser.__init__ import __version__

logger_setup = (
    LoggerSetup()
    .load_config(Path(__file__).parent / "config/logger.toml")
    .create_log_dirs(True)
    .set_error_to_email(None)
)
logger_setup.apply()

logger = logging.getLogger(__name__)

# ===========================================================
# parameters:


# ===========================================================
# classes:


# ===========================================================
# functions:


# ===========================================================
# main:


def main() -> bool:
    """Call main functionality of typeloader_reference_parser."""
    logger.info(f"<Start typeloader_reference_parser V{__version__}>")

    logger.info("<End typeloader_reference_parser>")
    return True


if __name__ == "__main__":
    main()
