# instawcbot
automatically wellcome every user joined insta group

# Insta WC Bot

## Overview
Insta WC Bot is a Telegram bot that welcomes new members in an Instagram group chat. The bot allows users to set their Instagram login credentials, specify a group chat ID, and define a custom welcome message. It continuously monitors the group and sends a welcome message to new members.


## Using the Telegram Bot version

## Features
- 📌 **Set Instagram Login** (`/setlogin`): Save Instagram username and password.
- 📌 **Set Group Chat ID** (`/setgroup`): Define the Instagram group chat to monitor.
- 📌 **Start/Stop Bot** (`/startbot`, `/stopbot`): Begin or halt the monitoring process.
- 📌 **Set Custom Welcome Message** (`/WellcomeMessage`): Customize the welcome message.
- 📌 **Check Bot Status** (`/status`): View whether the bot is running.
- 📌 **View Saved Settings** (`/mysettings`): Check stored Instagram credentials and group ID.

## Installation
### Prerequisites
Ensure you have Python installed along with the required dependencies:
```bash
pip install telebot instagrapi
```

### Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/Insta-WC-Bot.git
   cd Insta-WC-Bot
   ```
2. Create a `configuration.txt` file and add your Telegram bot token.
3. Run the bot:
   ```bash
   python bot.py
   ```

## Usage
1. Start the bot by sending `/start` in your Telegram chat.
2. Use `/setlogin` to provide your Instagram username and password.
3. Use `/setgroup` to set the Instagram group chat ID.
4. Start monitoring the group with `/startbot`.
5. Optionally, set a custom welcome message using `/WellcomeMessage`.

## Configuration
- The bot saves user credentials in `user_data.json`.
- Ensure valid Instagram credentials are provided.
- The bot polls Instagram every 5 seconds to check for new members.

## Notes
- Instagram may temporarily block frequent logins. Use trusted accounts.
- Keep your Telegram bot token secure.

## Credits
🫡 Made by [@tipsandgamer](https://t.me/tipsandgamer)

## License
This project is licensed under the MIT License.

