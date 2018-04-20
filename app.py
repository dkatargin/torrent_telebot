import configparser
from telegram import ParseMode
from telegram.ext import Updater, Filters, MessageHandler
from bot import ApiFunc

config = configparser.ConfigParser()
config.read('config.cfg')


def tele_bot(bot, m):
    if m.message.document:
        botfile = bot.getFile(m.message.document.file_id)
        m.message.text = botfile.file_path
    if m.message.from_user['id'] != int(config['Telegram']['admin_id']):
        return
    chat_id = m.message.chat_id
    api_answ = ApiFunc(m.message.text)
    bot.sendMessage(chat_id=chat_id, text=api_answ.answer,
                    parse_mode=ParseMode.MARKDOWN, reply_markup=api_answ.reply_markup)


if __name__ == '__main__':
    updater = Updater(config.get('Telegram', 'token'),
                      request_kwargs={'proxy_url': config.get('Proxy', 'address'),
                                      'urllib3_proxy_kwargs': {'username': config.get('Proxy', 'username'),
                                                               'password': config.get('Proxy', 'password')}}
                      )
    updater.dispatcher.add_handler(MessageHandler(Filters.all, tele_bot))
    updater.start_polling()
    updater.idle()
