"""Terminal ve dosya loglarını yapılandırır."""
import logging
from logging.handlers import RotatingFileHandler
from pusulaflow.config import PROJECT_ROOT


def setup_logging() -> None:
    logger = logging.getLogger("agentic_rag")

    if logger.handlers:
        return

    logger.setLevel(logging.DEBUG)
    logger.propagate = False

    log_dir = PROJECT_ROOT / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(message)s"
    )

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    file_handler = RotatingFileHandler(
        log_dir / "app.log",
        maxBytes=2_000_000,
        backupCount=3,
        encoding="utf-8",
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)