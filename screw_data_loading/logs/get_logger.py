import logging
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler
from typing import Any, Dict, List, Tuple


def get_logger(
    name: str,
    log_file: str = "screw_data_loading/logs/loading.log",
    level: int = logging.INFO,
    rotation_type: str = "size",
    max_bytes: int = 10 * 1024 * 1024,
    backup_count: int = 5,
    when: str = "midnight",
    interval: int = 1,
) -> logging.Logger:
    """
    Returns a logger with the specified name, log file, logging level,
    and log rotation based on size or time.

    Args:
        name (str):
            The name of the logger.
        log_file (str):
            The path to the log file.
        level (int):
            The logging level.
        rotation_type (str):
            Type of rotation ('size' or 'time').
        max_bytes (int):
            Maximum log file size in bytes before rotating (for size-based rotation).
        backup_count (int):
            Number of backup files to keep.
        when (str):
            Interval type for time-based rotation (e.g., 'midnight', 'D', 'H', 'M').
        interval (int):
            Interval of rotation for time-based rotation.

    Returns:
        logging.Logger: Configured logger.
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Clear existing handlers to prevent duplicate logs
    if logger.hasHandlers():
        logger.handlers.clear()

    # Create handlers based on rotation type
    if rotation_type == "size":
        file_handler = RotatingFileHandler(
            log_file, maxBytes=max_bytes, backupCount=backup_count, mode="a"
        )
    elif rotation_type == "time":
        file_handler = TimedRotatingFileHandler(
            log_file, when=when, interval=interval, backupCount=backup_count
        )
    else:
        raise ValueError(f"Invalid rotation_type: {rotation_type}")

    stream_handler = logging.StreamHandler()

    # Create formatter and add it to handlers
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    file_handler.setFormatter(formatter)
    stream_handler.setFormatter(formatter)

    # Add handlers to the logger
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)

    return logger
