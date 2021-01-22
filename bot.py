import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext, MessageHandler, Filters, commandhandler
import os
from instaloader import Instaloader, Profile
import time

L = Instaloader()
TOKEN = "<Your telegram Token>"

welcome_msg = '''<b>Welcome To the Bot</b>🖐🖐
 <i>Send me anyones instagram username to get their DP</i>
 ex : <b>virat.kohli</b> , <b>thenameisyash</b> etc'''

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)


def acc_type(val):
    if(val):
        return "🔒Private🔒"
    else:
        return "🔓Public🔓"


# Start the Bot
def start(update, context):
    update.message.reply_html(welcome_msg)


def help_msg(update, context):
    update.message.reply_text("Nothing to help ,this is Way to Simple 😂😂")


def contact(update, context):
    keyboard = [[InlineKeyboardButton(
        "Contact", url="<your contact url>")], ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text('Contact The Maker:', reply_markup=reply_markup)

# Get the username and send the DP


def username(update, context):
    msg = update.message.reply_text("Downloading...")
    query = update.message.text
    chat_id = update.message.chat_id
    try:
        user = Profile.from_username(L.context, query)
        caption_msg = f'''📛*Name*📛: {user.full_name} \n😁*Followers*😁: {user.followers} \n🤩*Following*🤩: {user.followees}\
         \n🧐*Account Type*🧐: {acc_type(user.is_private)} \n\nThank You For Using The bot 😀😀'''
        context.bot.send_photo(
            chat_id=chat_id, photo=user.profile_pic_url,
            caption=caption_msg, parse_mode='MARKDOWN')
        msg.edit_text("finished.")
        time.sleep(5)
    except Exception:
        msg.edit_text("Try again 😕😕 Check the username correctly")


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    # Create the Updater and pass it your bot's token.
    updater = Updater(TOKEN, use_context=True)
    PORT = int(os.environ.get('PORT', '8443'))
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help_msg))
    dp.add_handler(CommandHandler("contact", contact))
    dp.add_handler(MessageHandler(Filters.text, username))
    # log all errors
    dp.add_error_handler(error)
    # Start the Bot
    updater.start_webhook(listen="0.0.0.0", port=PORT, url_path=TOKEN)
    updater.bot.set_webhook(
        "https://<your app name>.herokuapp.com/" + TOKEN)

    updater.idle()


if __name__ == '__main__':
    main()
