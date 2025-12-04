import os
import asyncio
import logging
from logging.handlers import RotatingFileHandler

# Pyrogram imports
from pyrogram import Client
from pyrogram.errors import FloodWait

# aiohttp imports
from aiohttp import web

# local imports
from web import web_app
from info import LOG_CHANNEL, API_ID, API_HASH, BOT_TOKEN, PORT, BIN_CHANNEL, ADMINS, DATABASE_URL, TAMILMV_LOG, TAMILBLAST_LOG
from utils import temp, get_readable_time
from plugins.scrapper.tools.rss_feed import tamilmv_rss_feed, tamilblasters_rss_feed

# pymongo and database imports
from database.users_chats_db import db
from database.ia_filterdb import Media
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s - %(levelname)s] - %(name)s - %(message)s',
    datefmt='%d-%b-%y %H:%M:%S',
    handlers=[
        RotatingFileHandler(
            'bot.log',
            maxBytes=50000000,
            backupCount=10
        ),
        logging.StreamHandler()
    ]
)
logging.getLogger("pyrogram").setLevel(logging.WARNING)
logging.getLogger("pymongo").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

class Bot(Client):
    def __init__(self):
        super().__init__(
            name='Auto-Filter-Bot',
            api_id=API_ID,
            api_hash=API_HASH,
            bot_token=BOT_TOKEN,
            plugins={"root": "plugins"}
        )

    async def start(self):
        try:
            # Get banned users and chats
            b_users, b_chats = await db.get_banned()
            temp.BANNED_USERS = b_users
            temp.BANNED_CHATS = b_chats
            logger.info(f"Loaded {len(b_users)} banned users and {len(b_chats)} banned chats")
            
            # Connect to MongoDB
            client = MongoClient(DATABASE_URL, server_api=ServerApi('1'))
            
            try:
                client.admin.command('ping')
                logger.info("✅ Successfully connected to MongoDB!")
            except Exception as e:
                logger.error(f"❌ MongoDB Connection Failed: {e}")
                exit()

            await super().start()

            # Handle restart
            if os.path.exists('restart.txt'):
                with open("restart.txt") as file:
                    chat_id, msg_id = map(int, file)
                try:
                    await self.edit_message_text(
                        chat_id=chat_id, 
                        message_id=msg_id, 
                        text='✅ Restarted Successfully!'
                    )
                    logger.info("Restart notification sent")
                except Exception as e:
                    logger.error(f"Failed to send restart notification: {e}")
                os.remove('restart.txt')
            
            # Set bot info in temp
            temp.BOT = self
            await Media.ensure_indexes()
            me = await self.get_me()
            temp.ME = me.id
            temp.U_NAME = me.username
            temp.B_NAME = me.first_name
            
            logger.info(f"🤖 Bot Started: @{me.username}")
            
            # Start web server
            app = web.AppRunner(web_app)
            await app.setup()
            await web.TCPSite(app, "0.0.0.0", PORT).start()
            logger.info(f"🌐 Web server started on port {PORT}")
            
            # Verify LOG_CHANNEL access
            try:
                await self.send_message(
                    chat_id=LOG_CHANNEL, 
                    text=f"<b>✅ {me.mention} Restarted Successfully! 🤖</b>"
                )
                logger.info(f"✅ LOG_CHANNEL verified: {LOG_CHANNEL}")
            except Exception as e:
                logger.error(f"❌ Cannot access LOG_CHANNEL ({LOG_CHANNEL}): {e}")
                logger.error("Please make sure bot is admin in LOG_CHANNEL")
                exit()
            
            # Verify BIN_CHANNEL access
            try:
                m = await self.send_message(chat_id=BIN_CHANNEL, text="Test")
                await m.delete()
                logger.info(f"✅ BIN_CHANNEL verified: {BIN_CHANNEL}")
            except Exception as e:
                logger.error(f"❌ Cannot access BIN_CHANNEL ({BIN_CHANNEL}): {e}")
                logger.error("Please make sure bot is admin in BIN_CHANNEL")
                exit()
            
            # Notify admins
            for admin in ADMINS:
                try:
                    await self.send_message(
                        chat_id=admin, 
                        text="<b>✅ ʙᴏᴛ ʀᴇsᴛᴀʀᴛᴇᴅ sᴜᴄᴄᴇssꜰᴜʟʟʏ</b>"
                    )
                except Exception as e:
                    logger.warning(f"Failed to notify admin {admin}: {e}")
            
            # Send startup messages to log channels
            for chat in [TAMILMV_LOG, TAMILBLAST_LOG]:
                try:
                    await self.send_message(chat, "🤖 Bot Started Successfully!")
                    logger.info(f"✅ Notified channel: {chat}")
                except Exception as e:
                    logger.warning(f"Failed to notify channel {chat}: {e}")
            
            logger.info("🚀 Bot initialization completed successfully!")
            
        except Exception as e:
            logger.error(f"❌ Error during bot startup: {e}", exc_info=True)
            raise

async def main():
    bot = Bot()
    
    try:
        # Start bot
        await bot.start()
        logger.info("✅ Bot started successfully")
        
        # Start RSS feed scrapers in background
        asyncio.create_task(rss_scraper_loop(bot))
        logger.info("📡 RSS scraper task started")
        
        # Keep bot running
        await bot.idle()
        
    except FloodWait as e:
        wait_time = get_readable_time(e.value)
        logger.warning(f"⏳ Flood Wait: Sleeping for {wait_time}")
        await asyncio.sleep(e.value)
        logger.info("✅ Ready after flood wait, restarting...")
        await bot.start()
        
    except Exception as e:
        logger.error(f"❌ Critical error in main: {e}", exc_info=True)
        
    finally:
        await bot.stop()
        logger.info("Bot stopped")

async def rss_scraper_loop(bot):
    """Background task for RSS feed scraping with error handling"""
    await asyncio.sleep(60)  # Wait 1 minute after bot starts
    
    while True:
        try:
            logger.info("🔄 Starting TamilMV RSS scraper...")
            await tamilmv_rss_feed(bot)
            logger.info("✅ TamilMV scraper completed")
            
            await asyncio.sleep(10)  # Small delay between scrapers
            
            logger.info("🔄 Starting TamilBlasters RSS scraper...")
            await tamilblasters_rss_feed(bot)
            logger.info("✅ TamilBlasters scraper completed")
            
            # Wait 30 minutes before next scrape
            logger.info("⏳ Waiting 30 minutes before next scrape cycle...")
            await asyncio.sleep(1800)
            
        except Exception as e:
            logger.error(f"❌ Error in RSS scraper: {e}", exc_info=True)
            # Wait 5 minutes on error before retrying
            logger.info("⏳ Waiting 5 minutes before retry due to error...")
            await asyncio.sleep(300)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
