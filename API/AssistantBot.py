import os
import logging
import directories
from dotenv import load_dotenv, find_dotenv
from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from BaseClass import BaseClass


# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)
helper = BaseClass()

# Define a few command handlers. These usually take the two arguments update and
# context.
def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    update.message.reply_text('Hello dear manager')

def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')


def echo(update: Update, context: CallbackContext) -> None:
    """Echo the user message."""
    user = update.message.from_user
    logger.info("User %s writes url: %s", user.first_name, update.message.text)

    if 'www.trendyol.com' in update.message.text or 'ty.gl' in update.message.text:
        response=helper.InsertProductByURL(update.message.text)
        
        for url in response[2]:
            update.message.reply_photo(photo=url)
        
        update.message.reply_text('Код: {}'.format(response[1]))
    else:
        update.message.reply_text('You have entered incorrect URL: {}'.format('asdfs'))


def main() -> None:
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    load_dotenv(find_dotenv())
    directories.init()
    updater = Updater(os.environ.get('TOKEN'))
    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))

    # on non command i.e message - echo the message on Telegram
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()