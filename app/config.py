import os
from dotenv import load_dotenv
from app.models.app_data import MAppData

load_dotenv()

# ============ APP CONFIG ============

API_HOST = os.getenv("API_HOST", "localhost")
API_PORT = int(os.getenv("API_PORT", 8000))
API_MAIN_MODULE = os.getenv("API_MAIN_MODULE", "app.main:app")
LOGGER_LEVEL = os.getenv("LOGGER_LEVEL", "INFO")

ALLOW_ORIGINS = os.getenv("ALLOW_ORIGINS", "*").split(',')
ALLOW_CREDENTIALS = os.getenv("ALLOW_CREDENTIALS", "True").lower() == "true"
ALLOW_METHODS = os.getenv("ALLOW_METHODS", "*").split(',')
ALLOW_HEADERS = os.getenv("ALLOW_HEADERS", "*").split(',')

# ============ GKB CONFIG ============

GKB_TL_BOT = os.getenv("GKB_TL_BOT")

# ============ TL CLIENTS CONFIG ============

APP_TITLES = os.getenv("APP_TITLES", "").split(',')
APP_SHORT_NAMES = os.getenv("APP_SHORT_NAMES", "").split(',')
APP_API_IDS = os.getenv("APP_API_IDS", "").split(',')
APP_API_HASHES = os.getenv("APP_API_HASHES", "").split(',')

API_KEYS: list[MAppData] = [
    MAppData(
        title=APP_TITLES[i],
        short_name=APP_SHORT_NAMES[i],
        api_id=int(APP_API_IDS[i]),
        api_hash=APP_API_HASHES[i]
    )
    for i in range(len(APP_API_IDS))
]

# ============ REDIS CONFIG ============

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = os.getenv("REDIS_PORT", "6379")
REDIS_USERNAME = os.getenv("REDIS_USERNAME", "admin")
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD", "")
REDIS_SESSION_TTL = int(os.getenv("REDIS_SESSION_TTL", 300))