from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import youtube_bot

# Telegram Bot Token
TELEGRAM_BOT_TOKEN = "7630033744:AAEu7WSycAtC1ZiVDtv5C2clOeSyjd5cTlc"

# Start command
def start(update, context):
    update.message.reply_text("Send a YouTube video URL, and I'll comment on it!")

# Handle YouTube URLs
def handle_message(update, context):
    url = update.message.text
    if "youtube.com" in url or "youtu.be" in url:
        video_id = url.split("v=")[-1].split("&")[0]
        youtube_bot.comment_on_video(video_id)
        update.message.reply_text("Comment posted successfully!")
    else:
        update.message.reply_text("Please send a valid YouTube URL.")

# Setup the bot
updater = Updater(TELEGRAM_BOT_TOKEN, use_context=True)
dp = updater.dispatcher

dp.add_handler(CommandHandler("start", start))
dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

# Start the bot
updater.start_polling()
updater.idle()
