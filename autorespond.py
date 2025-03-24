# Telegram Auto-Reply Bot
# When I'm offline, replies to messages on my behalf
# Created: 2025-03-24
# Updated: 

import os
import time
import random
from datetime import datetime
from dotenv import load_dotenv
from telethon import TelegramClient, events

# Load settings from .env file
load_dotenv()

# Basic setup - fill these in your .env file
api_id = int(os.getenv('API_ID', 0))
api_hash = os.getenv('API_HASH', '')
phone_number = os.getenv('PHONE_NUMBER', '')
my_user_id = int(os.getenv('MASTER_USER_ID', 0))  # My personal account ID

# How often to check if I'm online (in seconds)
check_interval = 5 * 60  

# Simple logging to track what's happening
def log_message(text):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f"[{timestamp}] {text}")

# My custom responses when people message me
RESPONSES = {
    'greeting': "Hey! I'm currently away. I'll get back to you when I can!",
    'question': "Thanks for your message! I'm not available right now but will reply later.",
    'urgent': "I'm offline at the moment. For urgent matters, please call me!",
    'default': "Got your message! I'll respond as soon as I'm back online."
}

# Connect to Telegram
client = TelegramClient('my_auto_reply', api_id, api_hash)

# Track if I'm currently online
am_i_online = False
last_seen_time = None

async def check_my_status():
    """Periodically check if I'm online"""
    global am_i_online, last_seen_time
    
    while True:
        try:
            me = await client.get_entity(my_user_id)
            
            if me.status is None:
                # Sometimes status isn't available
                am_i_online = False
                last_seen_time = "a while ago"
            elif hasattr(me.status, 'was_online'):
                # I'm definitely offline
                am_i_online = False
                last_online = me.status.was_online
                last_seen_time = last_online.strftime('%Y-%m-%d %H:%M')
            else:
                # I'm online or recently online
                am_i_online = True
                last_seen_time = "just now"
                
            log_message(f"Status check: {'Online' if am_i_online else 'Offline'} (Last seen: {last_seen_time})")
            
        except Exception as e:
            log_message(f"Error checking status: {e}")
        
        await asyncio.sleep(check_interval)

async def handle_new_message(event):
    """Reply to messages when I'm offline"""
    # Don't reply to myself or in group chats
    if event.out or not event.is_private:
        return
    
    sender = await event.get_sender()
    if sender.id == my_user_id:
        return
    
    message_text = event.raw_text.lower()
    log_message(f"New message from {sender.first_name}: {message_text[:50]}...")
    
    # Only reply if I'm offline
    if not am_i_online:
        # Make it look like I'm typing
        async with client.action(event.chat_id, 'typing'):
            await asyncio.sleep(random.uniform(1, 3))  # Random typing delay
            
        # Choose appropriate response
        if any(word in message_text for word in ['hi', 'hello', 'hey']):
            reply = RESPONSES['greeting']
        elif '?' in message_text:
            reply = RESPONSES['question']
        elif any(word in message_text for word in ['urgent', 'emergency', 'important']):
            reply = RESPONSES['urgent']
            # Forward really urgent messages to me
            await client.forward_messages(my_user_id, event.message)
            log_message("Forwarded urgent message!")
        else:
            reply = RESPONSES['default']
            
        await event.reply(reply)

async def run_bot():
    """Start everything up"""
    try:
        await client.start(phone_number)
        log_message("Bot started successfully!")
        
        # Start checking my status in the background
        asyncio.create_task(check_my_status())
        
        # Set up the message handler
        client.add_event_handler(
            handle_new_message,
            events.NewMessage(incoming=True)
        )
        
        # Keep running until disconnected
        await client.run_until_disconnected()
        
    except Exception as e:
        log_message(f"Bot crashed: {e}")
    finally:
        log_message("Bot stopped")

if __name__ == '__main__':
    # Quick check for required settings
    if not all([api_id, api_hash, phone_number]):
        print("Missing required settings in .env file!")
        exit(1)
        
    # Start the bot
    log_message("Starting up...")
    asyncio.run(run_bot())