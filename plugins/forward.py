import logging
import re
import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message
from info import API_ID, API_HASH, USER_STRING_SESSION, SOURCE_CHANNELS1, SOURCE_CHANNELS2, SOURCE_CHANNELS3, SOURCE_CHANNELS4, SOURCE_CHANNELS5, SOURCE_CHANNELS6, SOURCE_CHANNELS7, ADMINS
from database.users_chats_db import db

logger = logging.getLogger(__name__)

# Initialize user client
user_client = None

async def init_user_client():
    """Initialize the user client for forwarding"""
    global user_client
    try:
        user_client = Client(
            "user_session",
            api_id=API_ID,
            api_hash=API_HASH,
            session_string=USER_STRING_SESSION
        )
        await user_client.start()
        logger.info("User client started successfully")
        return user_client
    except Exception as e:
        logger.error(f"Error initializing user client: {str(e)}")
        return None

async def replace_links_in_message(message, web_link, my_link, my_username, original_text, replace_text):
    """Replace links and text in message"""
    if web_link:
        message = re.sub(r'https?://tcvvip5\.com/#/register\?r_code=44YWW823408', web_link, message)
    if my_link:
        message = re.sub(r'https?://t\.me/\S*|t\.me/\S*', my_link, message)
    if my_username:
        message = re.sub(r'@[\w]+', my_username, message)
    if original_text and replace_text:
        message = message.replace(original_text, replace_text)
    return message

async def forward_message_handler(client: Client, message: Message, command_type: int):
    """Handle message forwarding based on command type"""
    try:
        # Skip bot start messages
        if message.text == "Bot Started!":
            return
        
        # Get channel configuration from database
        channel_data = await db.get_channel(command_type)
        if not channel_data:
            logger.error(f"No data found for command_type: {command_type}")
            return
        
        destination_channels = channel_data.get("destination_channel_ids", [])
        original_text = channel_data.get("original_text", "")
        replace_text = channel_data.get("replace_text", "")
        my_link = channel_data.get("my_link", "")
        web_link = channel_data.get("web_link", "")
        my_username = channel_data.get("my_username", "")

        if not destination_channels:
            logger.warning(f"No destination channels found for command_type {command_type}")
            return
        
        logger.info(f"Handling command_type {command_type}: destination_channels={destination_channels}")
        
        # Handle media messages
        if message.media:
            # Copy the message and replace caption if exists
            for destination_channel_id in destination_channels:
                try:
                    destination_channel_id = int(destination_channel_id)
                    
                    # Get original caption
                    caption = message.caption if message.caption else ""
                    
                    # Replace links in caption
                    if caption:
                        caption = await replace_links_in_message(
                            caption, web_link, my_link, my_username, original_text, replace_text
                        )
                    
                    # Forward message with modified caption
                    await message.copy(
                        chat_id=destination_channel_id,
                        caption=caption if caption else None
                    )
                    logger.info(f"Message forwarded to {destination_channel_id}")
                except ValueError as e:
                    logger.error(f"Invalid entity ID for {destination_channel_id}: {e}")
                except Exception as e:
                    logger.error(f"Failed to forward message to {destination_channel_id}: {e}")
        else:
            # Handle text messages
            replaced_message = await replace_links_in_message(
                message.text, web_link, my_link, my_username, original_text, replace_text
            )
            
            for destination_channel_id in destination_channels:
                try:
                    destination_channel_id = int(destination_channel_id)
                    await client.send_message(destination_channel_id, replaced_message)
                    logger.info(f"Message forwarded to {destination_channel_id}")
                except ValueError as e:
                    logger.error(f"Invalid entity ID for {destination_channel_id}: {e}")
                except Exception as e:
                    logger.error(f"Failed to forward message to {destination_channel_id}: {e}")
    
    except Exception as e:
        logger.error(f"Error in forward_message_handler: {e}")

# Register handlers for each source channel
def register_forward_handlers(app: Client):
    """Register message handlers for forwarding"""
    
    @app.on_message(filters.chat(SOURCE_CHANNELS1) & (filters.text | filters.media))
    async def forward_from_source1(client, message):
        await forward_message_handler(client, message, 1)
    
    @app.on_message(filters.chat(SOURCE_CHANNELS2) & (filters.text | filters.media))
    async def forward_from_source2(client, message):
        await forward_message_handler(client, message, 2)
    
    @app.on_message(filters.chat(SOURCE_CHANNELS3) & (filters.text | filters.media))
    async def forward_from_source3(client, message):
        await forward_message_handler(client, message, 3)
    
    @app.on_message(filters.chat(SOURCE_CHANNELS4) & (filters.text | filters.media))
    async def forward_from_source4(client, message):
        await forward_message_handler(client, message, 4)
    
    @app.on_message(filters.chat(SOURCE_CHANNELS5) & (filters.text | filters.media))
    async def forward_from_source5(client, message):
        await forward_message_handler(client, message, 5)
    
    @app.on_message(filters.chat(SOURCE_CHANNELS6) & (filters.text | filters.media))
    async def forward_from_source6(client, message):
        await forward_message_handler(client, message, 6)
    
    @app.on_message(filters.chat(SOURCE_CHANNELS7) & (filters.text | filters.media))
    async def forward_from_source7(client, message):
        await forward_message_handler(client, message, 7)

# Start the user client when the bot starts
async def start_forward_service():
    """Start the forwarding service with user client"""
    global user_client
    if USER_STRING_SESSION:
        try:
            user_client = await init_user_client()
            if user_client:
                logger.info("Forward service initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize forward service: {e}")
    else:
        logger.warning("USER_STRING_SESSION not configured, forwarding service disabled")
