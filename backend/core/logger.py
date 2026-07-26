import logging


def get_logger(name: str) -> logging.Logger:
    """
    Return a logger instance.

    Args:
        name: Logger name.

    Returns:
        Logger.
    """

    return logging.getLogger(name)