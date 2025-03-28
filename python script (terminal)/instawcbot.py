from instagrapi import Client
import time
import json
from typing import Set
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Instagram credentials
USERNAME = input("Enter insta account username:")
PASSWORD = input("Enter insta account password:  ")
GROUP_CHAT_ID = input("Enter group chat ID:  ")
SESSION_FILE = "session.json"  # File to save session
PARTICIPANTS_FILE = "participants.json"

# Welcome message
WELCOME_MESSAGE = "Welcome to the group, {username}! We're glad you're here!"

def load_session(client: Client):
    """Load session from file to avoid re-login."""
    try:
        with open(SESSION_FILE, "r") as f:
            session = json.load(f)
            client.set_settings(session)
            client.login(USERNAME, PASSWORD)  # Re-authenticate with session
            logging.info("Session loaded successfully!")
    except FileNotFoundError:
        client.login(USERNAME, PASSWORD)
        with open(SESSION_FILE, "w") as f:
            json.dump(client.get_settings(), f)
        logging.info("New session created and saved!")

def load_previous_participants() -> Set[str]:
    """Load the previous set of participants from a file."""
    try:
        with open(PARTICIPANTS_FILE, "r") as f:
            return set(json.load(f))
    except (FileNotFoundError, json.JSONDecodeError):
        return set()

def save_participants(participants: Set[str]):
    """Save the current set of participants to a file."""
    with open(PARTICIPANTS_FILE, "w") as f:
        json.dump(list(participants), f)

def get_group_participants(client: Client, group_id: str) -> Set[str]:
    """Fetch current participants in the group chat."""
    try:
        thread = client.direct_thread(group_id)
        return {user.username for user in thread.users}
    except Exception as e:
        logging.error(f"Failed to fetch participants: {e}")
        raise

def send_welcome_message(client: Client, group_id: str, username: str):
    """Send a welcome message to the group chat."""
    message = WELCOME_MESSAGE.format(username=username)
    try:
        client.direct_send(message, thread_ids=[group_id])
        logging.info(f"Sent welcome message to {username}")
    except Exception as e:
        logging.error(f"Failed to send message: {e}")
        raise

def main():
    # Initialize Instagram client
    client = Client()
    load_session(client)
    
    # Load previous participants
    previous_participants = load_previous_participants()

    while True:
        try:
            # Get current participants
            current_participants = get_group_participants(client, GROUP_CHAT_ID)

            # Detect new users
            new_users = current_participants - previous_participants
            for username in new_users:
                logging.info(f"New user detected: {username}")
                send_welcome_message(client, GROUP_CHAT_ID, username)

            # Update previous participants
            previous_participants = current_participants
            save_participants(current_participants)

            # Wait before checking again
            time.sleep(60)

        except Exception as e:
            logging.error(f"Main loop error: {e}")
            time.sleep(300)  # Wait longer if there's an error

if __name__ == "__main__":
    main()