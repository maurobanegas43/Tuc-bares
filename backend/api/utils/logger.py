import logging
from typing import Any

# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

logger = logging.getLogger("tuc-bares")


def log_info(message: str, **kwargs: Any) -> None:
    """Log de información."""
    extra = " ".join([f"{k}={v}" for k, v in kwargs.items()]) if kwargs else ""
    logger.info(f"{message} {extra}".strip())


def log_error(message: str, **kwargs: Any) -> None:
    """Log de error."""
    extra = " ".join([f"{k}={v}" for k, v in kwargs.items()]) if kwargs else ""
    logger.error(f"{message} {extra}".strip())


def log_warning(message: str, **kwargs: Any) -> None:
    """Log de advertencia."""
    extra = " ".join([f"{k}={v}" for k, v in kwargs.items()]) if kwargs else ""
    logger.warning(f"{message} {extra}".strip())