from telegram import ParseMode
from telegram.ext import Updater, Filters, MessageHandler
from bot import ApiFunc
from common import config


def bot_app(update, context):
    cmd = update.message.text
    if update.message.chat.id != int(config.config.get('Telegram', 'admin_id')):
        return
    if update.message.document:
        cmd = context.bot.get_file(update.message.document.file_id).file_path
        print(type(cmd))
    api_answ = ApiFunc(cmd)
    update.message.reply_text(api_answ.answer, parse_mode=ParseMode.MARKDOWN, reply_markup=api_answ.reply_markup)


if __name__ == '__main__':
   
    updater = Updater(config.config.get('Telegram', 'token'), request_kwargs=config.get_proxy_settings())
    updater.dispatcher.add_handler(MessageHandler(Filters.all, bot_app))
    updater.start_polling()
    updater.idle()
