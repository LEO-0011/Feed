from pyrogram import Client, filters, enums
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from database.users_chats_db import db as u_db
from info import ADMINS

@Client.on_message(filters.command("links") & filters.private)
async def links(c: Client, m: Message):
    ''' Start Message of the Bot !!'''

    await m.reply_text(
        text='''
<b>🔰 Hello, I am TamilMVAutoRss and Multi-Tasking Bot! 🔰</b>

<b>Get All RSS Feed Channel Links</b>''',
        quote=True,
        parse_mode=enums.ParseMode.HTML,
        disable_web_page_preview=True,
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("1TamilMV", url="https://t.me/+1gSCxb28yHk3YmU1")],
            [InlineKeyboardButton("1TamilBlasters", url="https://t.me/+1gSCxb28yHk3YmU1")],
            [InlineKeyboardButton("2TamilRockers", url="https://t.me/+1gSCxb28yHk3YmU1")]
        ])
    )
    
# Add multiple domains
@Client.on_message(filters.command("set_domains") & filters.user(ADMINS))
async def add_domains(client: Client, message: Message):
    """
    Adds multiple domains and associates each with its website.
    Usage: /add_domains <url1> <url2> <url3>
    """
    args = message.text.split(maxsplit=3)
    
    if len(args) != 4:
        await message.reply(
            "<b>Usage :- </b><code>/set_domains [url1] [url2] [url3]</code>",
            parse_mode=enums.ParseMode.HTML,
            disable_web_page_preview=True
        )
        return

    # Extract URLs
    url1, url2, url3 = args[1], args[2], args[3]
    
    try:
        # Add domains to the database with appropriate names
        await u_db.add_or_update_domain("1TamilMV", url1)
        await u_db.add_or_update_domain("1TamilBlasters", url2)
        await u_db.add_or_update_domain("2TamilRockers", url3)

        # Send a confirmation message
        await message.reply(
            f"<b>Domains have been added/updated:</b>\n"
            f"<b>1TamilMV :- {url1}</b>\n"
            f"<b>1TamilBlasters :- {url2}</b>\n"
            f"<b>2TamilRockers :- {url3}</b>",
            parse_mode=enums.ParseMode.HTML,
            disable_web_page_preview=True
        )
    except Exception as e:
        # Log the error and notify the user
        await message.reply(
            f"<b>An error occurred while adding domains:</b> <code>{e}</code>",
            parse_mode=enums.ParseMode.HTML,
            disable_web_page_preview=True
        )

@Client.on_message(filters.command("get_domains") & filters.user(ADMINS))
async def get_domains(client: Client, message: Message):
    """
    Fetches and displays all available domains from the database.
    """
    try:
        # Fetch all domains from the database
        domains = await u_db.get_all_domains()
        
        if not domains:
            await message.reply("<b>No domains found in the database.</b>", disable_web_page_preview=True)
            return
        
        # Create a formatted response
        response = "<b>Available Website Domains :-</b>\n"
        for key, url in domains.items():
            response += f"<b>{key} :- {url}</b>\n"
        
        await message.reply(response, parse_mode=enums.ParseMode.HTML, disable_web_page_preview=True)
    except Exception as e:
        # Log the error and notify the user
        await message.reply(
            f"<b>An error occurred while fetching domains:</b> <code>{e}</code>",
            parse_mode=enums.ParseMode.HTML,
            disable_web_page_preview=True
        )
        
