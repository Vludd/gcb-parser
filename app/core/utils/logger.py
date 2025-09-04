import logging
import colorlog
from app.config import LOGGER_LEVEL

LOG_LEVEL_COLORS = {
    "DEBUG": "cyan",
    "INFO": "green",
    "WARNING": "yellow",
    "ERROR": "red",
    "CRITICAL": "bold_red",
}

formatter = colorlog.ColoredFormatter(
    fmt="%(log_color)s%(levelname)-9s%(reset)s (%(cyan)s%(name)s%(reset)s) %(message)s",
    log_colors=LOG_LEVEL_COLORS,
    reset=True,
    style="%",
)

handler = logging.StreamHandler()
handler.setFormatter(formatter)

logger = logging.getLogger()
logger.setLevel(LOGGER_LEVEL)
logger.addHandler(handler)
logger.propagate = False

logging.getLogger("telethon").setLevel(logging.WARNING)
logging.getLogger("watchfiles").setLevel(logging.WARNING)