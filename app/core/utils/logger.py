import logging
from app.config import LOGGER_LEVEL

logging.basicConfig(level=LOGGER_LEVEL)
logger = logging.getLogger(__name__)