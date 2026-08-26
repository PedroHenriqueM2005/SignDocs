import logging
import os
from app.config import BASE_DIR

LOG_PATH = os.path.join(BASE_DIR, "app.log")


def setup_logger():
    """Configura logging para console e arquivo (app.log)."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        handlers=[
            logging.FileHandler(LOG_PATH, encoding="utf-8"),
            logging.StreamHandler(),
        ],
    )