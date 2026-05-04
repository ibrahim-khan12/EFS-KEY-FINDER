import logging
from pathlib import Path

from core.config import APP_NAME, APP_VERSION, LOG_DIR


def setup_logging(log_name: str = "efs_key_finder.log") -> Path:
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    log_path = LOG_DIR / log_name

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        handlers=[
            logging.FileHandler(log_path, encoding="utf-8"),
            logging.StreamHandler(),
        ],
    )
    logging.getLogger(__name__).info("%s %s logging initialized", APP_NAME, APP_VERSION)
    return log_path
