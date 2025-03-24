
# Telegram Auto-Reply Bot

 A simple bot that replies to messages when you're offline  
*"Because sometimes you need a digital secretary"*

## What This Does

When you're not available on Telegram, this bot will:
- Automatically reply to private messages
- Let people know you'll get back to them later
- Forward urgent messages to you immediately
- Pretend to be typing (like a real person would)

## Setup Guide

### 1. Prerequisites
- Python 3.8 or newer
- A Telegram account (the one you want to monitor)
- [Telegram API credentials](https://my.telegram.org/apps)

### 2. Installation

First, clone this repo and install requirements:
```bash
git clone https://github.com/yourusername/telegram-auto-reply.git
cd telegram-auto-reply
pip install -r requirements.txt
```

### 3. Configuration

Create a `.env` file with these details:
```ini
API_ID=1234567                          # From my.telegram.org
API_HASH="your_api_hash_here"           # From my.telegram.org
PHONE_NUMBER="+1234567890"              # Your phone number with country code
MASTER_USER_ID=987654321                # Your Telegram user ID
```

To find your user ID:
1. Forward a message to @userinfobot
2. It will reply with your ID

### 4. Running the Bot

```bash
python bot.py
```

On first run, you'll need to:
1. Enter your phone number
2. Input the verification code sent to Telegram
3. Optionally set a password if you have 2FA enabled

## Features

   **Smart Online Detection**  
   Knows when you're actually offline (not just "last seen")

  **Natural Responses**  
   Replies don't sound robotic:
   - "Hey! I'm currently away..."
   - "Got your message! I'll respond soon."

  **Urgent Message Handling**  
   Forwards messages containing "urgent" or "emergency"

  **Typing Indicators**  
   Simulates human typing before replying

## Customizing Responses

Edit the `RESPONSES` dictionary in `bot.py`:
```python
RESPONSES = {
    'greeting': "Your custom hello message",
    'question': "How to reply when someone asks something",
    'urgent': "Urgent message response",
    'default': "Standard reply when nothing else matches"
}
```

## Keeping It Running

For 24/7 operation:
```bash
nohup python bot.py > bot.log 2>&1 &
```

Check logs:
```bash
tail -f bot.log
```

## Troubleshooting

  **Not receiving replies?**  
   - Make sure your account shows as offline (close all Telegram clients)
   - Check bot.log for errors

  **Login issues?**  
   - Delete the `my_auto_reply.session` file and try again

  **Other problems?**  
   - Check if Telegram is blocking new logins (wait 24 hours if so)

## Disclaimer

⚠ Use at your own risk! Telegram may limit accounts that send too many automated messages.  
This is meant for personal use with reasonable message volumes.

---

Made with ❤️ by [dulagudeta](https://github.com/dulagudeta)  
Feel free to tweak this for your needs!
```
