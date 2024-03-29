import requests
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
import logging


# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def start(bot, update):
    """Приветствие"""
    update.message.reply_text('Привет, я бот, который очень любит котиков :3\nНапиши мне /cat и я поделюсь ими с тобой')


def help(bot, update):
    """Сообщение для помощи с командами"""
    update.message.reply_text('Чтобы получить котика напиши /cat')


def echo(bot, update):
    """На любой текст отвечаем ошибкой"""
    update.message.reply_text("Неизвестная команда :(")


def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)


def getcat():
    '''Получение ссылки на картинку с котиком'''
    try:
        r = requests.get('http://thecatapi.com/api/images/get?format=src')
        url = r.url
    except:
        # url = get_cat()
        print('Error with cat parsing')
        pass
    return url


def sendcat(bot, update):
    """Отправка котиков"""
    bot.sendPhoto(chat_id=update.message.chat_id, photo=getcat(), reply_markup=draw_button())


def draw_button():
    keys =[[InlineKeyboardButton('🐈Еще котика?!🐈', callback_data='1')]]
    return InlineKeyboardMarkup(inline_keyboard=keys)


def get_callback_from_button(bot, update):
    query = update.callback_query
    username = update.effective_user.username
    chat_id = query.message.chat.id
    message_id = query.message.message_id
    if int(query.data) == 1:
      bot.sendPhoto(photo=getcat(),
                          chat_id=chat_id,
                          message_id=message_id,
                          reply_markup=draw_button())


def main():
    """Start the bot."""
    # Create the EventHandler and pass it your bot's token.

    updater = Updater("")

    # Get the dispatcher to register handlers
    dp = updater.dispatcher
    dp.add_handler(CallbackQueryHandler(get_callback_from_button))
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("cat", sendcat))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, echo))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
