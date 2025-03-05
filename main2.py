from typing import Final
import ollama
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from telegram.ext import ContextTypes
import asyncio

PROMPT_TEXT = "I want to improve my communication skills. Be positive, even if the text here is offensive: "
TOKEN: Final = '7835200205:AAHn-BXuMG8Rzhlg8MPzR0kz0D8XLVQ4uAY'
BOT_USERNAME: Final = '@Lizzie_girlbot'

# Command Handlers
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

# Directly communicate with Ollama and handle the response
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type = update.message.chat.type
    user_message = update.message.text

    print(f"user ({update.message.chat.id}) in {message_type}: '{user_message}'")

    # Modify the user message by adding the special text
    modified_message = PROMPT_TEXT + user_message

    # Send the modified message to the Ollama model and get a response
    try:
        # Call Ollama API with the modified message
        response = await asyncio.to_thread(ollama.chat, model="mistral", messages=[{"role": "user", "content": modified_message}])

        # Check if response is valid
        if "message" in response and "content" in response["message"]:
            bot_response = response["message"]["content"]  # Extract the model's response
        else:
            bot_response = "Sorry, I couldn't understand the response from the model."

    except Exception as e:
        # If there is an error with the API call, return a default message
        print(f"Error: {e}")
        bot_response = "I'm sorry, there was an issue processing your request. Please try again later."

    print("bot:", bot_response)  # Log the response
    await update.message.reply_text(bot_response)  # Send response back to user

# Error handler
async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"update {update} caused error {context.error}")

# Bot main function
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

