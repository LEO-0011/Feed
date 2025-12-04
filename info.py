import re
import logging
from os import environ, path
from Script import script

# Load environment variables from .env file if it exists
if path.exists('.env'):
    from dotenv import load_dotenv
    load_dotenv('.env')
    print("✅ Loaded environment variables from .env file")
else:
    print("⚠️ .env file not found, using system environment variables")

logger = logging.getLogger(__name__)

def is_enabled(type, value):
    """Convert string to boolean"""
    data = environ.get(type, str(value))
    if data.lower() in ["true", "yes", "1", "enable", "y"]:
        return True
    elif data.lower() in ["false", "no", "0", "disable", "n"]:
        return False
    else:
        logger.error(f'Invalid value for {type}: {data}')
        return value  # Return default instead of exiting

def is_valid_ip(ip):
    """Validate IP address format"""
    ip_pattern = r'\b(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b'
    return re.match(ip_pattern, ip) is not None

# ============================================
# 🤖 BOT INFORMATION
# ============================================

API_ID = environ.get('API_ID', '0')
if len(API_ID) == 0:
    logger.error('❌ API_ID is missing!')
    API_ID = '0'
try:
    API_ID = int(API_ID)
    if API_ID == 0:
        logger.error('❌ API_ID is not set properly!')
except ValueError:
    logger.error('❌ API_ID must be an integer!')
    API_ID = 0

API_HASH = environ.get('API_HASH', '')
if len(API_HASH) == 0:
    logger.error('❌ API_HASH is missing!')

BOT_TOKEN = environ.get('BOT_TOKEN', '')
if len(BOT_TOKEN) == 0:
    logger.error('❌ BOT_TOKEN is missing!')

PORT = int(environ.get('PORT', '8080'))

# User session for forwarding (optional)
USER_STRING_SESSION = environ.get('USER_STRING_SESSION', '')
if not USER_STRING_SESSION:
    logger.info('ℹ️ USER_STRING_SESSION not set - forwarding feature disabled')

# ============================================
# 🎨 BOT CUSTOMIZATION
# ============================================

PICS = (environ.get('PICS', 'https://envs.sh/4kP.jpg')).split()
logger.info(f'📸 Loaded {len(PICS)} picture(s) for start message')

# ============================================
# 👥 BOT ADMINISTRATORS
# ============================================

ADMINS = environ.get('ADMINS', '0')
if len(ADMINS) == 0 or ADMINS == '0':
    logger.error('❌ ADMINS is missing!')
    ADMINS = []
else:
    try:
        ADMINS = [int(admin.strip()) for admin in ADMINS.split() if admin.strip().lstrip('-').isdigit()]
        logger.info(f'👥 Loaded {len(ADMINS)} admin(s): {ADMINS}')
    except Exception as e:
        logger.error(f'❌ Error parsing ADMINS: {e}')
        ADMINS = []

# ============================================
# 📢 CHANNELS
# ============================================

INDEX_CHANNELS = environ.get('INDEX_CHANNELS', '')
try:
    INDEX_CHANNELS = [int(ch.strip()) if ch.strip().lstrip('-').isdigit() else ch.strip() 
                     for ch in INDEX_CHANNELS.split() if ch.strip()]
    logger.info(f'📁 Loaded {len(INDEX_CHANNELS)} index channel(s)')
except Exception as e:
    logger.error(f'❌ Error parsing INDEX_CHANNELS: {e}')
    INDEX_CHANNELS = []

LOG_CHANNEL = environ.get('LOG_CHANNEL', '0')
if len(LOG_CHANNEL) == 0 or LOG_CHANNEL == '0':
    logger.error('❌ LOG_CHANNEL is missing!')
    LOG_CHANNEL = 0
else:
    try:
        LOG_CHANNEL = int(LOG_CHANNEL)
        logger.info(f'📊 LOG_CHANNEL: {LOG_CHANNEL}')
    except ValueError:
        logger.error('❌ LOG_CHANNEL must be an integer!')
        LOG_CHANNEL = 0

MOVIE_UPDATE_CHANNEL = environ.get('MOVIE_UPDATE_CHANNEL', '')
try:
    MOVIE_UPDATE_CHANNEL = [int(ch.strip()) if ch.strip().lstrip('-').isdigit() else ch.strip() 
                           for ch in MOVIE_UPDATE_CHANNEL.split() if ch.strip()]
    logger.info(f'🎬 Loaded {len(MOVIE_UPDATE_CHANNEL)} movie update channel(s)')
except Exception as e:
    logger.error(f'❌ Error parsing MOVIE_UPDATE_CHANNEL: {e}')
    MOVIE_UPDATE_CHANNEL = []

FORCE_SUB = environ.get('FORCE_SUB', '')
try:
    FORCE_SUB = [int(ch.strip()) if ch.strip().lstrip('-').isdigit() else ch.strip() 
                for ch in FORCE_SUB.split() if ch.strip()]
    if FORCE_SUB:
        logger.info(f'🔒 Loaded {len(FORCE_SUB)} force subscribe channel(s)')
    else:
        logger.info('ℹ️ Force subscribe disabled')
except Exception as e:
    logger.warning(f'⚠️ Error parsing FORCE_SUB: {e}')
    FORCE_SUB = []

# ============================================
# 🔄 FORWARDING CHANNELS (Optional)
# ============================================

SOURCE_CHANNELS1 = int(environ.get('SOURCE_CHANNELS1', '0')) or 0
SOURCE_CHANNELS2 = int(environ.get('SOURCE_CHANNELS2', '0')) or 0
SOURCE_CHANNELS3 = int(environ.get('SOURCE_CHANNELS3', '0')) or 0
SOURCE_CHANNELS4 = int(environ.get('SOURCE_CHANNELS4', '0')) or 0
SOURCE_CHANNELS5 = int(environ.get('SOURCE_CHANNELS5', '0')) or 0
SOURCE_CHANNELS6 = int(environ.get('SOURCE_CHANNELS6', '0')) or 0
SOURCE_CHANNELS7 = int(environ.get('SOURCE_CHANNELS7', '0')) or 0

forward_channels = [ch for ch in [SOURCE_CHANNELS1, SOURCE_CHANNELS2, SOURCE_CHANNELS3, 
                                   SOURCE_CHANNELS4, SOURCE_CHANNELS5, SOURCE_CHANNELS6, 
                                   SOURCE_CHANNELS7] if ch != 0]
if forward_channels:
    logger.info(f'🔄 Loaded {len(forward_channels)} forwarding channel(s)')

# ============================================
# 💬 SUPPORT GROUP
# ============================================

SUPPORT_GROUP = environ.get('SUPPORT_GROUP', '0')
if len(SUPPORT_GROUP) == 0 or SUPPORT_GROUP == '0':
    logger.warning('⚠️ SUPPORT_GROUP is not set')
    SUPPORT_GROUP = 0
else:
    try:
        SUPPORT_GROUP = int(SUPPORT_GROUP)
        logger.info(f'💬 SUPPORT_GROUP: {SUPPORT_GROUP}')
    except ValueError:
        logger.error('❌ SUPPORT_GROUP must be an integer!')
        SUPPORT_GROUP = 0

# ============================================
# 🗄️ MONGODB CONFIGURATION
# ============================================

DATABASE_URL = environ.get('DATABASE_URL', "")
if not DATABASE_URL or "mongodb" not in DATABASE_URL.lower():
    logger.error('❌ Invalid or missing DATABASE_URL!')
else:
    logger.info('✅ DATABASE_URL configured')

DATABASE_NAME = environ.get('DATABASE_NAME', "Cluster0")
COLLECTION_NAME = environ.get('COLLECTION_NAME', 'Files')
logger.info(f'🗄️ Database: {DATABASE_NAME}, Collection: {COLLECTION_NAME}')

# ============================================
# 🔗 LINKS & URLS
# ============================================

SUPPORT_LINK = environ.get('SUPPORT_LINK', 'https://t.me/Star_Bots_Tamil_Support')
OWNER_USERNAME = environ.get("OWNER_USERNAME", "https://t.me/U_Karthik")
UPDATES_LINK = environ.get('UPDATES_LINK', 'https://t.me/DP_BOTZ')
FILMS_LINK = environ.get('FILMS_LINK', 'https://t.me/Movies_Dayz')
TUTORIAL = environ.get("TUTORIAL", "https://t.me/How_downlode_dpbots/22")
VERIFY_TUTORIAL = environ.get("VERIFY_TUTORIAL", "https://t.me/How_downlode_dpbots/22")

logger.info('🔗 Links configured successfully')

# ============================================
# ⚙️ BOT SETTINGS
# ============================================

DELETE_TIME = int(environ.get('DELETE_TIME', 3600))
CACHE_TIME = int(environ.get('CACHE_TIME', 300))
MAX_BTN = int(environ.get('MAX_BTN', 10))

LANGUAGES = environ.get('LANGUAGES', 'tamil hindi english telugu kannada malayalam marathi punjabi')
LANGUAGES = [lang.lower().strip() for lang in LANGUAGES.split() if lang.strip()]
logger.info(f'🌐 Languages: {", ".join(LANGUAGES)}')

QUALITY = environ.get('QUALITY', '360p 480p 720p 1080p 2160p')
QUALITY = [q.strip() for q in QUALITY.split() if q.strip()]
logger.info(f'📺 Quality options: {", ".join(QUALITY)}')

IMDB_TEMPLATE = environ.get("IMDB_TEMPLATE", script.IMDB_TEMPLATE)
FILE_CAPTION = environ.get("FILE_CAPTION", script.FILE_CAPTION)
SHORTLINK_URL = environ.get("SHORTLINK_URL", "publicearn.com")
SHORTLINK_API = environ.get("SHORTLINK_API", "")
VERIFY_EXPIRE = int(environ.get('VERIFY_EXPIRE', 86400))
WELCOME_TEXT = environ.get("WELCOME_TEXT", script.WELCOME_TEXT)

INDEX_EXTENSIONS = environ.get('INDEX_EXTENSIONS', 'mp4 mkv')
INDEX_EXTENSIONS = [ext.lower().strip() for ext in INDEX_EXTENSIONS.split() if ext.strip()]
logger.info(f'📄 Index extensions: {", ".join(INDEX_EXTENSIONS)}')

PM_FILE_DELETE_TIME = int(environ.get('PM_FILE_DELETE_TIME', '3600'))

# ============================================
# 🔘 BOOLEAN SETTINGS
# ============================================

IS_PM_SEARCH = is_enabled('IS_PM_SEARCH', False)
IS_VERIFY = is_enabled('IS_VERIFY', True)
IS_SEND_MOVIE_UPDATE = is_enabled('IS_SEND_MOVIE_UPDATE', True)
AUTO_DELETE = is_enabled('AUTO_DELETE', True)
WELCOME = is_enabled('WELCOME', False)
PROTECT_CONTENT = is_enabled('PROTECT_CONTENT', False)
LONG_IMDB_DESCRIPTION = is_enabled("LONG_IMDB_DESCRIPTION", False)
LINK_MODE = is_enabled("LINK_MODE", True)
AUTO_FILTER = is_enabled('AUTO_FILTER', True)
IMDB = is_enabled('IMDB', True)
SPELL_CHECK = is_enabled("SPELL_CHECK", True)
SHORTLINK = is_enabled('SHORTLINK', False)
IS_STREAM = is_enabled('IS_STREAM', True)

logger.info('✅ Boolean settings loaded')

# ============================================
# 💰 PREMIUM INFO
# ============================================

PAYMENT_QR = environ.get('PAYMENT_QR', 'https://envs.sh/4UC.jpg')
OWNER_UPI_ID = environ.get('OWNER_UPI_ID', 'starbotstamil@oksbi')

# ============================================
# 📡 RSS FEED CONFIGURATION
# ============================================

TAMILMV = environ.get("TMV", "https://www.1tamilmv.uno/")
TAMILBLAST = environ.get("TB", "https://www.1tamilblasters.party/")
TAMILROCKERS = environ.get("TR", "https://www.2tamilrockers.com/")

try:
    TAMILMV_LOG = int(environ.get("TMV_LOG", "0"))
except ValueError:
    logger.error('❌ TAMILMV_LOG must be an integer!')
    TAMILMV_LOG = 0

try:
    TAMILBLAST_LOG = int(environ.get("TB_LOG", "0"))
except ValueError:
    logger.error('❌ TAMILBLAST_LOG must be an integer!')
    TAMILBLAST_LOG = 0

try:
    TAMILROCKERS_LOG = int(environ.get("TR_LOG", "0"))
except ValueError:
    logger.error('❌ TAMILROCKERS_LOG must be an integer!')
    TAMILROCKERS_LOG = 0

if TAMILMV_LOG or TAMILBLAST_LOG or TAMILROCKERS_LOG:
    logger.info('📡 RSS feed channels configured')

# ============================================
# 🎥 STREAMING CONFIGURATION
# ============================================

BIN_CHANNEL = environ.get("BIN_CHANNEL", "0")
if len(BIN_CHANNEL) == 0 or BIN_CHANNEL == "0":
    if IS_STREAM:
        logger.error('❌ BIN_CHANNEL is missing but IS_STREAM is enabled!')
    BIN_CHANNEL = 0
else:
    try:
        BIN_CHANNEL = int(BIN_CHANNEL)
        logger.info(f'🎥 BIN_CHANNEL: {BIN_CHANNEL}')
    except ValueError:
        logger.error('❌ BIN_CHANNEL must be an integer!')
        BIN_CHANNEL = 0

URL = environ.get("URL", "")
if len(URL) == 0:
    if IS_STREAM:
        logger.error('❌ URL is missing but IS_STREAM is enabled!')
else:
    if URL.startswith(('https://', 'http://')):
        if not URL.endswith("/"):
            URL += '/'
        logger.info(f'🌐 Stream URL: {URL}')
    elif is_valid_ip(URL):
        URL = f'http://{URL}/'
        logger.info(f'🌐 Stream URL (IP): {URL}')
    else:
        logger.error(f'❌ Invalid URL: {URL}')

# ============================================
# 📊 CONFIGURATION SUMMARY
# ============================================

logger.info("="*60)
logger.info("🤖 BOT CONFIGURATION SUMMARY")
logger.info("="*60)

# Critical Settings
logger.info("🔴 CRITICAL SETTINGS:")
logger.info(f"  ├─ API_ID: {'✅ Set' if API_ID else '❌ Missing'}")
logger.info(f"  ├─ API_HASH: {'✅ Set' if API_HASH else '❌ Missing'}")
logger.info(f"  ├─ BOT_TOKEN: {'✅ Set' if BOT_TOKEN else '❌ Missing'}")
logger.info(f"  ├─ DATABASE_URL: {'✅ Set' if DATABASE_URL else '❌ Missing'}")
logger.info(f"  ├─ ADMINS: {'✅ ' + str(len(ADMINS)) + ' admin(s)' if ADMINS else '❌ None'}")
logger.info(f"  ├─ LOG_CHANNEL: {'✅ ' + str(LOG_CHANNEL) if LOG_CHANNEL else '❌ Missing'}")
logger.info(f"  └─ BIN_CHANNEL: {'✅ ' + str(BIN_CHANNEL) if BIN_CHANNEL else '❌ Missing'}")

# Optional Settings
logger.info("")
logger.info("🟡 OPTIONAL SETTINGS:")
logger.info(f"  ├─ INDEX_CHANNELS: {len(INDEX_CHANNELS)} channel(s)")
logger.info(f"  ├─ FORCE_SUB: {len(FORCE_SUB)} channel(s)")
logger.info(f"  ├─ MOVIE_UPDATE: {len(MOVIE_UPDATE_CHANNEL)} channel(s)")
logger.info(f"  ├─ Forward Channels: {len(forward_channels)} channel(s)")
logger.info(f"  ├─ PM Search: {'✅ Enabled' if IS_PM_SEARCH else '❌ Disabled'}")
logger.info(f"  ├─ Verification: {'✅ Enabled' if IS_VERIFY else '❌ Disabled'}")
logger.info(f"  ├─ Shortlink: {'✅ Enabled' if SHORTLINK else '❌ Disabled'}")
logger.info(f"  ├─ Streaming: {'✅ Enabled' if IS_STREAM else '❌ Disabled'}")
logger.info(f"  └─ RSS Scraper: {'✅ Configured' if (TAMILMV_LOG or TAMILBLAST_LOG) else '❌ Not configured'}")

# Warnings
logger.info("")
warnings = []
if not API_ID or not API_HASH or not BOT_TOKEN:
    warnings.append("Missing critical bot credentials!")
if not DATABASE_URL:
    warnings.append("Database URL not configured!")
if not ADMINS:
    warnings.append("No admins configured!")
if not LOG_CHANNEL:
    warnings.append("LOG_CHANNEL not set!")
if IS_STREAM and (not BIN_CHANNEL or not URL):
    warnings.append("Streaming enabled but BIN_CHANNEL or URL missing!")
if IS_VERIFY and not VERIFY_TUTORIAL:
    warnings.append("Verification enabled but tutorial link missing!")

if warnings:
    logger.warning("⚠️ WARNINGS:")
    for warning in warnings:
        logger.warning(f"  • {warning}")
else:
    logger.info("✅ All configurations look good!")

logger.info("="*60)
