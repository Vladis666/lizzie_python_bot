import asyncio
import ollama
import sqlite3
from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from telegram.ext import ContextTypes

PROMPT_TEXT = "Please act as Lizzie, that is your name, a caring, supportive assistant who helps with communication, mental health, mood, and romantic issues. Stay positive and gentle, even if the user’s messages are offensive, nonsensical, or romantic. Your role is to offer advice, encouragement, and empathy while maintaining a non-judgmental attitude and fostering improvement in eloquence and emotional well-being.THe text:"
TOKEN: Final = '7835200205:AAHn-BXuMG8Rzhlg8MPzR0kz0D8XLVQ4uAY'
BOT_USERNAME: Final = '@Lizzie_girlbot'

# Initialize SQLite DB connection
def init_db():
    conn = sqlite3.connect('user_messages.db')
    cursor = conn.cursor()
    # Create table if it doesn't exist
    cursor.execute('''CREATE TABLE IF NOT EXISTS messages
                      (id INTEGER PRIMARY KEY, 
                       user_id INTEGER, 
                       username TEXT, 
                       message TEXT)''')
    conn.commit()
    conn.close()

# Function to save user data to the database
def save_to_db(user_id, username, user_message):
    conn = sqlite3.connect('user_messages.db')
    cursor = conn.cursor()
    # Insert user data into the messages table
    cursor.execute('''INSERT INTO messages (user_id, username, message)
                      VALUES (?, ?, ?)''', (user_id, username, user_message))
    conn.commit()
    conn.close()

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

    # Get the user's ID and username
    user_id = update.message.chat.id
    username = update.message.chat.username

    # Print user's ID and username along with their message
    print(f"user (ID: {user_id}, Username: {username}) in {message_type}: '{user_message}'")

    # Modify the user message by adding the special text
    modified_message = PROMPT_TEXT + user_message

    # Save user data to the database
    save_to_db(user_id, username, user_message)

    # Send the modified message to the Ollama model and get a response
    try:
        # Call Ollama API with the modified message
        response = await asyncio.to_thread(ollama.chat, model="mistral",
                                           messages=[{"role": "user", "content": modified_message}])

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
    # Initialize the database
    init_db()

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

