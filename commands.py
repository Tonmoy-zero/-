from telegram import Update
from telegram.ext import ContextTypes
from bot_config import WELCOME_TEXT, HELP_TEXT

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the /start command"""
    await update.message.reply_text(WELCOME_TEXT)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the /help command"""
    await update.message.reply_text(HELP_TEXT)