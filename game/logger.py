"""Provides a shared, pre-configured logger for the whole game.

Call get_logger() from any module to get a logger that writes
timestamped messages to the console.  All modules share the same
underlying logger instance so the output stays in order.
"""
import logging

_LOGGER_NAME = "deep_jungle"


def get_logger(name: str = _LOGGER_NAME) -> logging.Logger:
    """Return a configured logger, creating it on first call.

    Args:
        name: Logger name (defaults to the game's root logger).

    Returns:
        A :class:`logging.Logger` with a timestamped stream handler.
    """
    logger = logging.getLogger(name)

    # Only attach the handler once — subsequent calls reuse the same instance.
    if logger.handlers:
        return logger

    logger.setLevel(logging.DEBUG)

    handler = logging.StreamHandler()
    handler.setLevel(logging.DEBUG)

    formatter = logging.Formatter(
        fmt="%(asctime)s [%(levelname)-8s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger
