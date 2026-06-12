import logging

from app.core.config import LOG_LEVEL


def setup_logger() -> None:
    logging.basicConfig(
        level=LOG_LEVEL,
        format=(
            "%(asctime)s | "
            "%(levelname)s | "
            "%(name)s | "
            "%(message)s"
        ),
    )