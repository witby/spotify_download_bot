import logging
import os

from command_handlers import send_spotify_songs
from telegram import Update
from telegram.ext import CallbackContext, CommandHandler, Updater

logger = logging.getLogger(__name__)


def setup_logging():
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )


def start(update: Update, context: CallbackContext):
    update.effective_message.reply_text("Hello, this is a bot for enjoying spotify music!")
    context.bot.send_message(
        chat_id=update.effective_chat.id, text="/spotify [url]"
    )


def error(update: Update, context: CallbackContext, error):
    logger.warning('Update "%s" caused error "%s"', update, error)


def main():
    TOKEN = os.environ.get('TOKEN')
    APP_NAME = os.environ.get('APP_NAME')

    # Port is given by Heroku
    PORT = os.environ.get('PORT')

    # Set up the Updater

    updater = Updater(
        TOKEN,
        use_context=True,
    )
    dp = updater.dispatcher
    # Add handlers
    dp.add_handler(CommandHandler('start', start))
    dp.add_error_handler(error)

    dp.add_handler(
        CommandHandler(
            'spotify',
            send_spotify_songs.send_spotify_songs,
            pass_args=True,
            pass_job_queue=True,
            pass_chat_data=True
        )
    )

    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
