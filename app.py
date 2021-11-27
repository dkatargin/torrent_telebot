from telegram import ParseMode, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import Updater, Filters, MessageHandler

from common import config, torrent_state
from common.transmission_connector import TransmissionCommands


class ApiFunc:
    def __init__(self, cmd):
        custom_keyboard = [
            [
                KeyboardButton(config.btn_download_state),
                KeyboardButton(config.btn_info),
            ],
            [KeyboardButton(config.btn_add_torrent)],
            [KeyboardButton(config.btn_rm_torrent)],
        ]

        self.reply_markup = ReplyKeyboardMarkup(custom_keyboard)
        torrent_add_state = torrent_state.get("add_torrent_state")
        torrent_rm_state = torrent_state.get("rm_torrent_state")
        if torrent_add_state:
            self.answer = self.add_torrent(state=torrent_add_state, options=cmd)
            return
        if torrent_rm_state:
            self.answer = self.rm_torrent(state=torrent_rm_state, options=cmd)
            return
        cmds_dict = {
            config.btn_download_state: self.torrent_status,
            config.btn_add_torrent: self.add_torrent,
            config.btn_rm_torrent: self.rm_torrent,
            config.btn_info: self.torrent_server_info,
        }

        if cmds_dict.get(cmd, None):
            func = cmds_dict.get(cmd)
            self.answer = func()
        else:
            self.answer = "Command unsupported"

    @staticmethod
    def torrent_status():
        return TransmissionCommands().torrents_list()

    @staticmethod
    def torrent_server_info():
        return TransmissionCommands().server_info()

    def add_torrent(self, state=None, options=None):
        if state == "sel_dir":
            seldir = config.get_type_by_emoji(options)
            if not seldir:
                return "Неизвестный тип загрузки"
            torrent_state["download_dir"] = seldir
            torrent_state["add_torrent_state"] = "sel_url"
            return "Загрузите торрент-файл"
        elif state == "sel_url":
            download_dir_name = config.torrent_state.get("download_dir")
            del torrent_state["download_dir"]
            del torrent_state["add_torrent_state"]
            TransmissionCommands().add_torrent(
                download_dir=config.get_download_dir(download_dir_name), torrent=options
            )
            return "Качаю!"
        else:
            torrent_state["add_torrent_state"] = "sel_dir"
            torrent_type = [
                [
                    KeyboardButton(config.torrent_types.get("music")),
                    KeyboardButton(config.torrent_types.get("movie")),
                ],
                [
                    KeyboardButton(config.torrent_types.get("serial")),
                    KeyboardButton(config.torrent_types.get("anime")),
                ],
                [KeyboardButton(config.torrent_types.get("other"))],
            ]
            self.reply_markup = ReplyKeyboardMarkup(torrent_type)
            return "Выберите тип торрента"

    def rm_torrent(self, state=None, options=None):
        if state == "rm":
            seltorrent = int(options.split("_")[0])
            del torrent_state["rm_torrent_state"]
            TransmissionCommands().rm_torrent(seltorrent)
            return "Удалён!"
        else:
            torrent_state["rm_torrent_state"] = "rm"
            rm_type = [
                ["%i_%s" % (i["id"], i["name"])]
                for i in TransmissionCommands().torrents_list(non_formated=True)
            ]
            self.reply_markup = ReplyKeyboardMarkup(rm_type)
            return "Выберите торрент для удаления"


def bot_app(update, context):
    cmd = update.message.text
    if update.message.chat.id != int(config.config.get("Telegram", "admin_id")):
        return
    if update.message.document:
        cmd = context.bot.get_file(update.message.document.file_id).file_path
        print(type(cmd))
    api_answ = ApiFunc(cmd)
    update.message.reply_text(
        api_answ.answer,
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=api_answ.reply_markup,
    )


if __name__ == "__main__":
    updater = Updater(
        config.config.get("Telegram", "token"),
        request_kwargs=config.get_proxy_settings(),
    )
    updater.dispatcher.add_handler(MessageHandler(Filters.all, bot_app))
    updater.start_polling()
    updater.idle()
