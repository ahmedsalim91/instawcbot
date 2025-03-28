import telebot
import threading
import time
import json
from instagrapi import Client
from telebot.types import Message
with open("configuration.txt", "r") as config_file:
    TELEGRAM_BOT_TOKEN = config_file.read().strip()
# Initialize Telegram Bot
bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

# Store user settings
user_data = {}
session_file = "user_data.json"

# Function to save session data
def save_user_data():
    with open(session_file, "w") as f:
        json.dump(user_data, f, indent=4)

def load_user_data():
    global user_data
    try:
        with open(session_file, "r") as f:
            user_data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        user_data = {}

# Load session on startup
load_user_data()

# Command: /start
@bot.message_handler(commands=['start'])
def send_welcome(message: Message):
    bot.reply_to(message, "👋 Welcome to Insta WC Bot!\n\nUse the following commands:\n"
                          "/setlogin - Set Instagram login\n"
                          "/setgroup - Set Group Chat ID\n"
                          "/startbot - Start the bot\n"
                          "/stopbot - Stop the bot\n"
                          "/status - Check bot status\n"
                          "/mysettings - View saved settings\n"
                          "/WellcomeMessage - Set Custom Welcome Message\n\n"
                          "\n🫡Made by @tipsandgamer \nDM for project ideas")

# Command: /setlogin
@bot.message_handler(commands=['setlogin'])
def set_login(message: Message):
    bot.reply_to(message, "Enter Instagram username & password (Format: username password)")
    bot.register_next_step_handler(message, save_login)

def save_login(message: Message):
    chat_id = str(message.chat.id)  # Ensure chat ID is a string
    try:
        username, password = message.text.split(" ", 1)

        if chat_id not in user_data:
            user_data[chat_id] = {}

        user_data[chat_id]["username"] = username
        user_data[chat_id]["password"] = password
        save_user_data()
        bot.reply_to(message, "✅ Login details saved!\n🫡Made by @tipsandgamer")
    except ValueError:
        bot.reply_to(message, "⚠️ Invalid format! Use: username password")
def save_welcome_message(message: Message):
    global welcome_message
    welcome_message = message.text
    bot.send_message(message.chat.id, "WELCOME MESSAGE SAVED SUCCESSFULLY")
# Command: /setgroup
@bot.message_handler(commands=['setgroup'])
def set_group(message: Message):
    bot.reply_to(message, "Enter Instagram Group Chat ID:")
    bot.register_next_step_handler(message, save_group)

def save_group(message):
    chat_id = str(message.chat.id)  # Convert chat_id to a string for JSON compatibility
    if chat_id not in user_data:
        user_data[chat_id] = {}  # Initialize user data if not exists
    user_data[chat_id]["group_id"] = message.text
    save_user_data()
    bot.send_message(message.chat.id, "✅ Group ID saved successfully!\n🫡Made by @tipsandgamer")

# Command: /mysettings
@bot.message_handler(commands=["mysettings"])
def my_settings(message):
    chat_id = str(message.chat.id)
    if chat_id in user_data:
        settings = user_data[chat_id]
        response = "**Your Saved Settings:**\n"
        response += f"- **Username:** {settings.get('username', 'Not set')}\n"
        response += f"- **Password:** {'******' if 'password' in settings else 'Not set'}\n"
        response += f"- **Group ID:** {settings.get('group_id', 'Not set')}\n🫡Made by @tipsandgamer"
    else:
        response = "\nYou haven't set up any data yet. Use /start to begin."

    bot.send_message(message.chat.id, response, parse_mode="Markdown")

# Background Instagram Bot
running_bots = {}
bot_threads = {}
welcome_message = None  
def welcome_bot(chat_id):
    client = Client()
    username = user_data[chat_id]["username"]
    password = user_data[chat_id]["password"]
    group_id = user_data[chat_id]["group_id"]

    client.login(username, password)
    previous_members = set()

    while chat_id in running_bots:
        try:
            thread = client.direct_thread(group_id)
            current_members = {user.username for user in thread.users}
            new_members = current_members - previous_members

            for member in new_members:
                defltwelcome_message = f"Welcome meri jaan , @{member}🍌!"
                newwelcome_message = [welcome_message, defltwelcome_message]
                message = newwelcome_message
                if welcome_message is None:
                    message = defltwelcome_message
                client.direct_send(message, thread_ids=[group_id])
                bot.send_message(chat_id, f"✅ Welcomed: {member}")

            previous_members = current_members
            time.sleep(5)  # Check every minute
        except Exception as e:
            bot.send_message(chat_id, f"⚠️ Error: {e}")
            time.sleep(300)
@bot.message_handler(commands=['WellcomeMessage'])
def set_welcome_message(message: Message):
    bot.reply_to(message, "Enter the welcome message: ")
    bot.register_next_step_handler(message, save_welcome_message)

# Command: /startbot
@bot.message_handler(commands=['startbot'])
def start_instagram_bot(message: Message):
    chat_id = str(message.chat.id)  # Convert to string
    if chat_id in running_bots:
        bot.reply_to(message, "⚠️ Bot is already running!")
    elif chat_id in user_data and "group_id" in user_data[chat_id]:
        bot.reply_to(message, "🚀 Bot started!")
        running_bots[chat_id] = True  # Set running flag
        bot_threads[chat_id] = threading.Thread(target=welcome_bot, args=(chat_id,))
        bot_threads[chat_id].start()
    else:
        bot.reply_to(message, "⚠️ Set login & group ID first using /setlogin & /setgroup")

# Command: /stopbot
@bot.message_handler(commands=['stopbot'])
def stop_instagram_bot(message: Message):
    chat_id = str(message.chat.id)
    if chat_id in running_bots:
        running_bots[chat_id] = False  # Stop thread loop
        del running_bots[chat_id]
        bot.reply_to(message, "⛔ Bot stopped!")
    else:
        bot.reply_to(message, "⚠️ No active bot!")

# Command: /status
@bot.message_handler(commands=['status'])
def check_status(message: Message):
    chat_id = str(message.chat.id)
    if chat_id in running_bots:
        bot.reply_to(message, "✅ Bot is running!")
    else:
        bot.reply_to(message, "⛔ Bot is not running!")

# Run Telegram Bot
bot.polling(none_stop=True)
