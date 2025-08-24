import os
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# Environment Variables থেকে Token আর Admin ID নিবে
BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))  # না দিলে default = 0

def start(update, context):
    update.message.reply_text("🤖 Bot is running successfully!")

def echo(update, context):
    if update.message.from_user.id == ADMIN_ID:
        update.message.reply_text(f"Admin said: {update.message.text}")
    else:
        update.message.reply_text(f"You said: {update.message.text}")

def main():
    if not BOT_TOKEN:
        print("❌ BOT_TOKEN পাওয়া যায়নি! Railway এ গিয়ে Environment Variable সেট করুন।")
        return

    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
