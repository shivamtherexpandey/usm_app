import logging
import sys
from pathlib import Path


def init_logger(
    log_file: str = "file.log", level: int = logging.INFO
) -> logging.Logger:
    logger = logging.getLogger("service")
    logger.setLevel(level)

    if not logger.handlers:
        # Create log directory if needed
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)

        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        # File handler
        file_handler = logging.FileHandler(log_file)

        # Unified formatter (includes filename)
        formatter = logging.Formatter(
            "%(asctime)s - %(filename)s - %(levelname)s - %(message)s"
        )

        console_handler.setFormatter(formatter)
        file_handler.setFormatter(formatter)

        # Attach both handlers
        logger.addHandler(console_handler)
        logger.addHandler(file_handler)

        logger.propagate = False

    return logger


# Initialize once here so all modules can just import it
logger = init_logger()
