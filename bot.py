import os
import logging
from telegram import Update, ParseMode
from telegram.ext import (
    Updater, CommandHandler, MessageHandler, Filters, 
    CallbackQueryHandler, ConversationHandler, CallbackContext
)
from config import TOKEN, COMMANDS, ADMIN_IDS, logger
from handlers import get_all_handlers
from models import Session, User, CustomCommand
from utils.helpers import get_user_by_telegram_id

def register_commands(updater):
    """Register bot commands with Telegram"""
    try:
        bot = updater.bot
        bot.set_my_commands([(cmd, desc) for cmd, desc in COMMANDS.items()])
        logger.info("Bot commands registered successfully")
    except Exception as e:
        logger.error(f"Error registering bot commands: {e}")

def handle_custom_commands(update: Update, context: CallbackContext) -> None:
    """Handle custom commands created by admins"""
    command_text = update.message.text[1:]  # Remove the / prefix
    
    # Skip built-in commands
    if command_text in COMMANDS:
        return
    
    session = Session()
    try:
        command = session.query(CustomCommand).filter(
            CustomCommand.command == command_text,
            CustomCommand.is_active == True
        ).first()
        
        if command:
            update.message.reply_text(
                command.response_text,
                parse_mode=ParseMode.MARKDOWN
            )
    except Exception as e:
        logger.error(f"Error in handle_custom_command: {e}")
    finally:
        session.close()

def error_handler(update: Update, context: CallbackContext) -> None:
    """Handle errors in the bot"""
    logger.error(f"Update {update} caused error {context.error}")
    
    try:
        if update and update.effective_message:
            update.effective_message.reply_text(
                "Произошла ошибка при обработке вашего запроса. Пожалуйста, попробуйте еще раз позже."
            )
    except Exception as e:
        logger.error(f"Error in error_handler while sending error message: {e}")

def main():
    """Start the bot"""
    # Initialize the updater with the bot token
    updater = Updater(TOKEN)
    
    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher
    
    # Register error handler
    dispatcher.add_error_handler(error_handler)
    
    # Add all handlers from the handlers package
    for handler in get_all_handlers():
        dispatcher.add_handler(handler)
    
    # Add catch-all handler for custom commands
    dispatcher.add_handler(MessageHandler(
        Filters.regex(r'^/[a-zA-Z0-9_]+$') & (~Filters.command),
        handle_custom_commands
    ))
    
    # Register commands with Telegram
    register_commands(updater)
    
    # Start the bot
    updater.start_polling()
    logger.info("Bot started successfully")
    
    # Run the bot until you send a signal to stop
    updater.idle()

if __name__ == '__main__':
    main()
