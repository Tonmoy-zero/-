import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from commands import start_command, help_command
from chat_handler import ChatHandler
from bot_utils import format_response

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Initialize chat handler
chat_handler = ChatHandler()

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle incoming messages and generate responses"""
    try:
        user_message = update.message.text
        logger.info(f"Received message from {update.effective_user.id}: {user_message}")

        # Get response from chat handler
        response = chat_handler.get_response(user_message)
        logger.info(f"Generated response for message: {user_message[:50]}...")

        # Format response for Telegram
        formatted_response = format_response(response)
        logger.info("Sending formatted response to user")

        await update.message.reply_text(formatted_response)

    except Exception as e:
        logger.error(f"Error handling message: {str(e)}")
        await update.message.reply_text(
            "Sorry, I encountered an error processing your request. Please try again."
        )

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Log errors caused by updates"""
    logger.error(f"Update {update} caused error {context.error}")

def main() -> None:
    """Start the bot"""
    # Get token from environment variable
    token = os.getenv('TELEGRAM_BOT_TOKEN')
    if not token:
        raise ValueError("TELEGRAM_BOT_TOKEN environment variable not set")

    # Create application
    app = Application.builder().token(token).build()

    # Add handlers
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Add error handler
    app.add_error_handler(error_handler)

    # Start the bot
    logger.info("Starting bot...")
    app.run_polling()

if __name__ == '__main__':
    main()