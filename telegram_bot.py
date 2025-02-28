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

# Dictionary of questions and answers
QA_PAIRS = {
    "job sector": "Private sector",
    "employee in usa": "500-1000",
    "total employee, all location/outside america": "2500 to less than 5000",
    "political party": "Republican / Democrat",
    "political view": "Moderate",
    "dietary restrictions": "I do not have any dietary restrictions",
    "do you or does anyone in your household work in any of the following industries?": "None of the above",
    "are you or anyone in your household employed in any of the following sectors?": "None of the above",
    "what types of vehicles do you own": "Gasoline/hybrid/full electric",
    "food allergy": "Do not have any food allergy",
    "how many surveys have you taken previously": "0 or 1-2",
    "cannabis use": "Use for medical conditions",
    "which of the following areas of it administration do you manage for your organization?": "Software administration, Network infrastructure, database, server maintenance",
    "which of the following types of business software products do you manage or oversee?": "Operating system management, Productivity software, cloud storage, security software",
    "activities done in the past 12/6 months": "Hiking, camping, golf, fishing",
    "what kind of gambling do you participate in? do you participate in online sport betting": "Online lottery, online poker/casino, casino poker (offline), or slot machines",
    "day to day it responsibility": "Networking, Endpoint device, Cyber security/information security, Data protection",
    "any types of responsibility regarding household decision": "I am the sole decision maker",
    "which culture do you most associate with": "Both Hispanic and American equally",
    "types of medical insurance": "Private life insurance (you bought yourself from a company)",
    "illness": "Prostate cancer, Migraine, High blood pressure, Depression, Arthritis",
    "health coverage type": "Individual health insurance plan",
    "how long have you been working for your organization": "5 to 10 years",
    "do you identify as a lgbtqa2+ member?": "No",
}

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle incoming messages and generate responses"""
    try:
        user_message = update.message.text.lower()  # Convert to lowercase for easier matching
        logger.info(f"Received message from {update.effective_user.id}: {user_message}")

        # Check if the user's message matches any question in the QA_PAIRS dictionary
        response = None
        for question, answer in QA_PAIRS.items():
            if question in user_message:
                response = answer
                break

        # If no matching question, use the chat handler to generate a response
        if not response:
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
