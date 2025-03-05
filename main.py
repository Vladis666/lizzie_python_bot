from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN: Final = '7835200205:AAHn-BXuMG8Rzhlg8MPzR0kz0D8XLVQ4uAY'
BOT_USERNAME: Final = '@Lizzie_girlbot'


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hey! Fancy sharpening your eloquence?")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = (
        "Here are some things I can do:\n"
        "/start - Begin your journey to eloquence\n"
        "/help - Get this help message\n\n"
        "Just send me a message, and I'll respond based on its content!"
    )
    await update.message.reply_text(help_text)


def handle_response(text: str) -> str:
    processed: str = text.lower()

    # AI is here

    if 'hi' in processed:
        return 'Hello'

    return 'OK'


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    user_message = update.message.text

    print(f"user ({update.message.chat.id}) in {message_type}: '{user_message}'")

    if message_type in ['group', 'supergroup']:  # Handle both types of group chats
        if BOT_USERNAME in user_message:
            new_text: str = user_message.replace(BOT_USERNAME, "").strip()
            response: str = handle_response(new_text)  # Corrected variable name
        else:
            return  # Exit if bot is not mentioned
    else:
        response: str = handle_response(user_message)

    print("bot:", response)  # Fixed variable name
    await update.message.reply_text(response)


async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"update {update} caused error {context.error}")


def main():
    print('Starting')
    app = Application.builder().token(TOKEN).build()

    # Add command handlers
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))

    # Add message handler for text messages
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Add error handler
    app.add_error_handler(error)

    # Start polling for updates
    print("Bot is running...")
    app.run_polling(poll_interval=3)


# Run the bot
if __name__ == "__main__":
    main()
