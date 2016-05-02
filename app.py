import configparser
import time
import telegram
from api import ApiFunc


class TeleBot:
    def __init__(self):
        config = configparser.ConfigParser()
        config.read('config.cfg')
        self.token = config['Telegram']['token']
        self.admin_user_id = int(config['Telegram']['admin_id'])
        self.bot = telegram.Bot(token=self.token)

    def main_func(self):
        update_id = 0
        for m in self.bot.getUpdates(timeout=20):
            print(str(m.message.text).encode('UTF-8'))
            if m.message.from_user['id'] != self.admin_user_id:
                continue
            chat_id = m.message.chat_id
            update_id = m.update_id
            api_answ = ApiFunc(m.message.text)
            self.bot.sendMessage(chat_id=chat_id, text=api_answ.answer,
                           parse_mode=telegram.ParseMode.MARKDOWN, reply_markup=api_answ.reply_markup)
            self.confirm_updates(update_id)

    def confirm_updates(self, update_id):
        print('confirmed')
        self.bot.getUpdates(offset=update_id+1, timeout=20)


if __name__ == '__main__':
    while True:
        TeleBot().main_func()
        time.sleep(3)
