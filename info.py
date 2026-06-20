import re
import os
import logging
from os import environ
from Script import script

logger = logging.getLogger(__name__)

# ─────────────────────────────────────────────
# 🧠 HELPERS & BOOLEAN PARSERS
# ─────────────────────────────────────────────
def is_enabled(key, default=False):
    val = environ.get(key, str(default)).lower()
    if val in ("true", "1", "yes", "y", "enable"): return True
    if val in ("false", "0", "no", "n", "disable"): return False
    logger.error(f"❌ {key} has invalid value")
    exit(1)

def is_valid_ip(ip):
    ip_pattern = (
        r'\b(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.'
        r'(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.'
        r'(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.'
        r'(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b'
    )
    return re.match(ip_pattern, ip) is not None

def get_channels(env_var):
    val = environ.get(env_var, "").replace(",", " ").strip()
    if not val: return []
    return [int(x) for x in val.split() if x.replace("-", "").isnumeric()]

# ─────────────────────────────────────────────
# 🤖 BOT CREDENTIALS
# ─────────────────────────────────────────────
API_ID = int(environ.get("API_ID", "0"))
API_HASH = environ.get("API_HASH", "")
BOT_TOKEN = environ.get("BOT_TOKEN", "")

if not API_ID or not API_HASH or not BOT_TOKEN:
    logger.error("❌ API_ID / API_HASH / BOT_TOKEN missing")
    exit(1)

BOT_ID = int(BOT_TOKEN.split(":")[0])
PORT = int(environ.get("PORT", 8080)) 

# ─────────────────────────────────────────────
# 👑 ADMINS & SECURITY (STRICTLY ADMIN ONLY)
# ─────────────────────────────────────────────
ADMINS = environ.get("ADMINS", "")
if not ADMINS:
    logger.error("❌ ADMINS environment variable missing")
    exit(1)
ADMINS = [int(x) for x in ADMINS.split() if x.isnumeric()]

# ─────────────────────────────────────────────
# 🖼️ IMAGES & CORE AI KEYS
# ─────────────────────────────────────────────
PICS = environ.get("PICS", "https://i.postimg.cc/8C15CQ5y/1.png").split()

# ─────────────────────────────────────────────
# 📢 STORAGE CHANNELS SYNC & ADVANCED ARCHITECTURE
# ─────────────────────────────────────────────
LOG_CHANNEL = int(environ.get("LOG_CHANNEL", "0"))
if not LOG_CHANNEL:
    logger.error("❌ LOG_CHANNEL missing")
    exit(1)

BIN_CHANNEL = int(environ.get("BIN_CHANNEL", "0")) 
if not BIN_CHANNEL:
    logger.error("❌ BIN_CHANNEL missing")
    exit(1)

PRIMARY_CHANNEL = int(environ.get("PRIMARY_CHANNEL", "-1000000000000"))
CLOUD_CHANNEL   = int(environ.get("CLOUD_CHANNEL", "-1000000000000"))
ARCHIVE_CHANNEL = int(environ.get("ARCHIVE_CHANNEL", "-1000000000000"))

THUMB_CHANNEL = int(environ.get("THUMB_CHANNEL", "-1000000000000")) 
TRASH_CHANNEL = int(environ.get("TRASH_CHANNEL", "-1000000000000")) 
ACTOR_CHANNEL = int(environ.get("ACTOR_CHANNEL", "-1000000000000")) 

# 📢 सपोर्ट / ऑडिट लॉग ग्रुप (ऑप्शनल)
SUPPORT_CHAT_ID = environ.get("SUPPORT_CHAT_ID", None)
if SUPPORT_CHAT_ID:
    SUPPORT_CHAT_ID = int(SUPPORT_CHAT_ID)

# ─────────────────────────────────────────────
# 🗄️ DATABASE CONNECTION URL
# ─────────────────────────────────────────────
DATABASE_URL = environ.get("DATABASE_URL", "")
DATABASE_NAME = environ.get("DATABASE_NAME", "Cluster0")

if not DATABASE_URL:
    logger.error("❌ DATABASE_URL missing")
    exit(1)

# ─────────────────────────────────────────────
# ⚙️ GLOBAL SETTINGS & ADAPTIVE RESULTS SYNC
# ─────────────────────────────────────────────
TIME_ZONE = environ.get("TIME_ZONE", "Asia/Kolkata")
MAX_BOT_RESULTS = int(environ.get("MAX_BOT_RESULTS", 12)) 
MAX_WEB_RESULTS = int(environ.get("MAX_WEB_RESULTS", 21)) 

# ─────────────────────────────────────────────
# ⏳ TIMERS ENGINE
# ─────────────────────────────────────────────
DELETE_TIME = int(environ.get("DELETE_TIME", 300)) 
PM_FILE_DELETE_TIME = int(environ.get("PM_FILE_DELETE_TIME", 600)) 
THUMB_DELETE_TIME = int(environ.get("THUMB_DELETE_TIME", 5))

# ─────────────────────────────────────────────
# ⚡ SPEED, BUFFER & ANTI-SPAM THRU LMT
# ─────────────────────────────────────────────
SEARCH_LIMIT_PER_SEC = int(environ.get("SEARCH_LIMIT_PER_SEC", 2))
MAX_THUMB_CACHE = int(environ.get("MAX_THUMB_CACHE", 500))

# ─────────────────────────────────────────────
# 🧩 FEATURE FLAGS
# ─────────────────────────────────────────────
USE_CAPTION_FILTER = is_enabled("USE_CAPTION_FILTER", True)
AUTO_DELETE = is_enabled("AUTO_DELETE", True)
PROTECT_CONTENT = is_enabled("PROTECT_CONTENT", False) 
SPELL_CHECK = is_enabled("SPELL_CHECK", True)
IS_STREAM = is_enabled("IS_STREAM", True)

# ─────────────────────────────────────────────
# 📝 TEXT FILE CAPTION TEMPLATE
# ─────────────────────────────────────────────
FILE_CAPTION = environ.get("FILE_CAPTION", script.FILE_CAPTION)

# ─────────────────────────────────────────────
# 🎥 STREAM ENGINE & WEB APP DOMAIN CONVERTER
# ─────────────────────────────────────────────
URL = environ.get("URL", "").strip()
if not URL:
    logger.error("❌ Web URL environment variable missing")
    exit(1)

if URL.startswith("http://"):
    URL = "https://" + URL[len("http://"):]

if URL.startswith("https://"):
    if not URL.endswith("/"): URL += "/"
elif is_valid_ip(URL):
    URL = f"https://{URL}/"
else:
    if not URL.startswith("https://") and "." in URL:
        URL = "https://" + URL.rstrip("/") + "/"
    else:
        logger.error("❌ Invalid URL - must start with https:// for Telegram Mini App support")
        exit(1)
