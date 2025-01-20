import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
GROUP_ID = os.getenv("GROUP_ID")

async def start(update: Update, context: CallbackContext):
    """Handle the /start command."""
    await update.message.reply_text("Hi! Send me an image or video, and I'll forward it to the group.")

async def forward_media(update: Update, context: CallbackContext):
    """Forward media to the specified group."""
    message = update.message

    if message.photo:
        await context.bot.send_photo(
            chat_id=GROUP_ID,
            photo=message.photo[-1].file_id,
            caption=message.caption or ""
        )
    elif message.video:
        await context.bot.send_video(
            chat_id=GROUP_ID,
            video=message.video.file_id,
            caption=message.caption or ""
        )
    else:
        await update.message.reply_text("Please send an image or a video.")

def main():
    print("🙋‍♀️I'm Alive")

    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.PHOTO | filters.VIDEO, forward_media))

    application.run_polling()

if __name__ == "__main__":
    main()