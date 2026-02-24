"""Lightweight rotating debug logger for runtime diagnostics."""

import logging
import os
import sys
from logging.handlers import RotatingFileHandler

from src.config import get_config_path

_MAX_LOG_BYTES = 256 * 1024
_LOG_BACKUP_COUNT = 3
_LOCAL_LOG_FILENAME = "productivity_clock_debug.log"
_EXE_LOG_FILENAME = "debug.log"


def get_debug_log_path():
    """Return the absolute debug log file path."""
    if getattr(sys, "frozen", False):
        # Keep exe logging in the user config directory.
        config_dir = os.path.dirname(get_config_path())
        os.makedirs(config_dir, exist_ok=True)
        return os.path.join(config_dir, _EXE_LOG_FILENAME)

    # Manual Python runs: keep log in the local project root.
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(project_root, _LOCAL_LOG_FILENAME)


def get_debug_logger(name):
    """Return a configured rotating logger with the given name."""
    logger = logging.getLogger(name)
    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO)
    handler = RotatingFileHandler(
        get_debug_log_path(),
        maxBytes=_MAX_LOG_BYTES,
        backupCount=_LOG_BACKUP_COUNT,
        encoding="utf-8",
    )
    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(threadName)s | %(message)s"
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.propagate = False
    return logger
