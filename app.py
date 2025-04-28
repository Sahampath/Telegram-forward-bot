import os
import asyncio
from dotenv import load_dotenv
from telegram import Update, InputMediaPhoto, InputMediaVideo, InputMediaAnimation
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
GROUP_ID = os.getenv("GROUP_ID")

media_groups = {}

async def start(update: Update, context: CallbackContext):
    """Handle the /start command."""
    await update.message.reply_text("Hi! Send me an image, video, or GIF, and I'll forward it to the group.")

async def forward_media(update: Update, context: CallbackContext):
    """Forward media to the specified group."""
    message = update.message
    media_group_id = message.media_group_id

    if media_group_id:
        if media_group_id not in media_groups:
            media_groups[media_group_id] = {
                'messages': [],
                'task': asyncio.create_task(send_media_group_later(context, media_group_id))
            }

        if message.photo:
            media = InputMediaPhoto(media=message.photo[-1].file_id, caption=message.caption or None)
        elif message.video:
            media = InputMediaVideo(media=message.video.file_id, caption=message.caption or None)
        elif message.animation:
            media = InputMediaAnimation(media=message.animation.file_id, caption=message.caption or None)
        else:
            return

        media_groups[media_group_id]['messages'].append(media)

    else:
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
        elif message.animation:
            await context.bot.send_animation(
                chat_id=GROUP_ID,
                animation=message.animation.file_id,
                caption=message.caption or ""
            )
        else:
            await update.message.reply_text("Please send an image, video, or GIF.")

async def send_media_group_later(context: CallbackContext, media_group_id):
    """Wait a short time and send the collected media group."""
    await asyncio.sleep(2)
    media_list = media_groups.get(media_group_id, {}).get('messages', [])

    if media_list:
        try:
            await context.bot.send_media_group(
                chat_id=GROUP_ID,
                media=media_list
            )
        except Exception as e:
            print(f"Failed to send media group: {e}")

    media_groups.pop(media_group_id, None)

def main():
    print("🙋‍♀️ I'm Alive")

    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.PHOTO | filters.VIDEO | filters.ANIMATION, forward_media))

    application.run_polling()

if __name__ == "__main__":
    main()
