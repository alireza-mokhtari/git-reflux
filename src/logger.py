from __future__ import annotations

import logging


def configure_logging(verbose: bool, quiet: bool) -> logging.Logger:
    level = logging.INFO
    if quiet:
        level = logging.WARNING
    if verbose:
        level = logging.DEBUG
    logging.basicConfig(level=level, format="%(levelname)s %(message)s")
    return logging.getLogger("git_reflux")


