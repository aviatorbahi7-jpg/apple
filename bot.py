import logging
import asyncio
import os
from threading import Thread
from flask import Flask, request
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters,
    ConversationHandler
)
from telegram.error import BadRequest

# ================= কনফিগারেশন =================
BOT_TOKEN = os.getenv("8511299158:AAHJL-7NTPcc0Dt4rGt3ixHcpOwUGAQ1lQA")
WEBHOOK_URL = os.getenv("https://signaapplel_bot.render.com/")
PORT = int(os.environ.get("PORT", 10000))

ADMIN_ID = 7406442919  
REQUIRED_CHANNEL_ID = "-1001481593780"

LINK_REGISTRATION = "https://bit.ly/BLACK220" 
PROMO_CODE = "BLACK220" 

CHANNEL_INVITE_LINK = "https://t.me/+3U0nMzWs4Aw0YjFl"
ADMIN_USER_LINK = "https://t.me/SUNNY_BRO1"

IMG_START = "https://i.ibb.co.com/23VVWgSS/file-00000000d21472088a8b84f9b1faa902.png"
IMG_LANG = "https://i.ibb.co.com/23VVWgSS/file-00000000d21472088a8b84f9b1faa902.png"
IMG_CHOOSE_PLATFORM = "https://i.ibb.co.com/NdFDsT4P/file-000000005308720880754a5daa131c74.png"
IMG_REGISTRATION = "https://i.ibb.co.com/NdFDsT4P/file-000000005308720880754a5daa131c74.png"
FINAL_IMAGE_URL = "https://i.ibb.co.com/vxfM0vv5/file-00000000f15071fa8c883abb1421fa69.png"

WEBAPP_URL = "https://1xbet-melbet-apple.unaux.com/"

USER_FILE = "users.txt"

TEXTS = {
    'en': {
        'choose_platform_caption': "🎮 <b>CHOOSE YOUR PLATFORM</b>\n\nWhich casino do you want to hack? Select below 👇",
        'btn_help': "🆘 Help / Support",
        'reg_title': "🚀 <b>{platform} REGISTRATION</b>",
        'reg_msg': (
            "⚠️ <b>WARNING:</b> Hack works ONLY with our Link!\n\n"
            "1️⃣ Delete old account.\n"
            "2️⃣ Click 'Register' below (Use promo <code>{promo}</code>).\n"
            "3️⃣ Create account and send ID.\n\n"
            "🛑 <i>If you don't use the link below, the bot will REJECT your ID.</i>"
        ),
        'btn_reg_link': "🔗 Register {platform}",
        'btn_next': "✅ I Registered (Verify ID)",
        'wait_msg': "⏳ <b>Connecting to Server...</b>\nChecking if ID was created via our link...",
        'ask_id': "📩 <b>SEND YOUR NEW ID</b>\n\nPlease send the <b>10-digit User ID</b> now.",
        'error_digit': "❌ <b>Error:</b> Digits only.",
        'error_length': "❌ <b>Invalid ID:</b> Must be 9 or 10 digits.",
        'fake_error': "❌ <b>VERIFICATION FAILED!</b>\n\nThis ID was NOT created using our Promo Link.\nPlease delete account and register using the button above.",
        'success_caption': "✅ <b>VERIFIED SUCCESS!</b>\n🆔 ID: <code>{uid}</code>\n\nAccount matched with Promo Code <b>{promo}</b>.\nClick below to Open Hack! 🤑",
        'btn_open_hack': "🍎 OPEN HACK (WebApp)",
        'btn_contact': "👨‍💻 Contact Admin"
    },
    'bn': {
        'choose_platform_caption': "🎮 <b>প্ল্যাটফর্ম নির্বাচন করুন</b>\nনিচে থেকে ক্যাসিনো সিলেক্ট করুন 👇",
        'btn_help': "🆘 সাহায্য / সাপোর্ট",
        'reg_title': "🚀 <b>{platform} রেজিস্ট্রেশন</b>",
        'reg_msg': (
            "⚠️ <b>সতর্কতা:</b> হ্যাকটি শুধুমাত্র আমাদের লিংকে কাজ করবে!\n\n"
            "1️⃣ পুরনো একাউন্ট ডিলিট করুন।\n"
            "2️⃣ নিচের 'Register' বাটনে ক্লিক করে একাউন্ট খুলুন (প্রোমো: <code>{promo}</code>)।\n"
            "3️⃣ আইডি আমাদের পাঠান।\n\n"
            "🛑 <i>আপনি যদি নিচের লিংক দিয়ে একাউন্ট না করেন, বট আপনার আইডি বাতিল করে দেবে।</i>"
        ),
        'btn_reg_link': "🔗 {platform} রেজিস্ট্রেশন লিংক",
        'btn_next': "✅ রেজিস্ট্রেশন করেছি (ভেরিফাই)",
        'wait_msg': "⏳ <b>সার্ভারে কানেক্ট হচ্ছে...</b>\nচেক করা হচ্ছে আইডিটি আমাদের লিংকে খোলা কিনা...",
        'ask_id': "📩 <b>আপনার আইডি পাঠান</b>\n\nআপনার নতুন একাউন্টের <b>১০ সংখ্যার আইডি</b> টি পাঠান।",
        'error_digit': "❌ <b>ভুল!</b> শুধুমাত্র ইংরেজি সংখ্যা পাঠান।",
        'error_length': "❌ <b>ভুল আইডি!</b> ৯ অথবা ১০ সংখ্যার আইডি হতে হবে।",
        'fake_error': "❌ <b>ভেরিফিকেশন ব্যর্থ হয়েছে!</b>\n\nএই আইডিটি আমাদের লিংক বা প্রোমো কোড দিয়ে খোলা হয়নি।\nদয়া করে নতুন করে একাউন্ট খুলুন।",
        'success_caption': "✅ <b>ভেরিফাইড সফল!</b>\n🆔 ID: <code>{uid}</code>\n\nআইডিটি প্রোমো কোড <b>{promo}</b> এর সাথে মিলেছে।\nহ্যাক চালু করতে নিচে ক্লিক করুন! 🤑",
        'btn_open_hack': "🍎 হ্যাক চালু করুন (WebApp)",
        'btn_contact': "👨‍💻 এডমিন সাপোর্ট"
    }
}

CHECK_JOIN, SELECT_LANGUAGE, CHOOSE_PLATFORM, WAITING_FOR_ID = range(4)
ADMIN_MENU, ADMIN_GET_CONTENT, ADMIN_GET_LINK, ADMIN_GET_BTN_NAME, ADMIN_CONFIRM = range(10, 15)

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

def save_user(user_id):
    if not os.path.exists(USER_FILE): open(USER_FILE, "w").close()
    with open(USER_FILE, "r") as f: users = f.read().splitlines()
    if str(user_id) not in users:
        with open(USER_FILE, "a") as f: f.write(f"{str(user_id)}\n")

def get_users():
    if not os.path.exists(USER_FILE): return []
    with open(USER_FILE, "r") as f: return f.read().splitlines()

async def check_membership(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    try:
        member = await context.bot.get_chat_member(chat_id=REQUIRED_CHANNEL_ID, user_id=user_id)
        return member.status in ['creator', 'administrator', 'member']
    except BadRequest: return False
    except Exception: return False

# =========================
# (user handlers, admin panel, conversation handlers সব আগের কোড এখানে থাকবে ঠিক যেমন আপনি পাঠিয়েছেন)
# =========================

# Flask + Webhook start
if __name__ == '__main__':
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    user_conv = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            CHECK_JOIN: [CallbackQueryHandler(check_join_callback, pattern='^check_join_status$')],
            SELECT_LANGUAGE: [CallbackQueryHandler(set_language, pattern='^lang_')],
            CHOOSE_PLATFORM: [CallbackQueryHandler(platform_choice, pattern='^platform_'), CallbackQueryHandler(wait_and_ask_id, pattern='^account_created$')],
            WAITING_FOR_ID: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_id)],
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )

    admin_conv = ConversationHandler(
        entry_points=[CommandHandler('admin', admin_start)],
        states={
            ADMIN_MENU: [CallbackQueryHandler(admin_mode_select, pattern='^mode_|admin_cancel')],
            ADMIN_GET_CONTENT: [MessageHandler(filters.PHOTO | filters.VIDEO | filters.TEXT, admin_get_content)],
            ADMIN_GET_LINK: [MessageHandler(filters.TEXT, admin_get_link)],
            ADMIN_GET_BTN_NAME: [MessageHandler(filters.TEXT, admin_get_btn_name)],
            ADMIN_CONFIRM: [CallbackQueryHandler(admin_perform_broadcast, pattern='^confirm_')]
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )

    application.add_handler(admin_conv)
    application.add_handler(user_conv)

    app = Flask(__name__)

    @app.route(f"/{BOT_TOKEN}", methods=["POST"])
    async def telegram_webhook():
        data = request.get_json(force=True)
        update = Update.de_json(data, application.bot)
        await application.process_update(update)
        return "ok"

    @app.route("/")
    def home():
        return "Bot is running with Webhook!"

    async def setup():
        await application.initialize()
        await application.bot.set_webhook(f"{WEBHOOK_URL}/{BOT_TOKEN}")
        await application.start()

    loop = asyncio.get_event_loop()
    loop.run_until_complete(setup())

    app.run(host="0.0.0.0", port=PORT)
