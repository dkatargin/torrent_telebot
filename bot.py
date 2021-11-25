import telegram
from transmission_connector import TransmissionCommands
from common import config

class TorrentState:
    pass


class ApiFunc:
    def __init__(self, cmd):
        custom_keyboard = [[telegram.KeyboardButton(config.btn_download_state),
                            telegram.KeyboardButton(config.btn_info)],
                           [telegram.KeyboardButton(config.btn_add_torrent)],
                           [telegram.KeyboardButton(config.btn_rm_torrent)]
                           ]

        self.reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard)
        torrent_add_state = getattr(TorrentState, 'add_torrent_state', None)
        torrent_rm_state = getattr(TorrentState, 'rm_torrent_state', None)
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
            self.answer = 'Command unsupported'

    @staticmethod
    def torrent_status():
        return TransmissionCommands().torrents_list()

    @staticmethod
    def torrent_server_info():
        return TransmissionCommands().server_info()

    def add_torrent(self, state=None, options=None):
        if state == 'sel_dir':
            seldir = config.get_type_by_emoji(options)
            if not seldir:
                return 'Неизвестный тип загрузки'
            setattr(TorrentState, 'download_dir', seldir)
            setattr(TorrentState, 'add_torrent_state', 'sel_url')
            return 'Загрузите торрент-файл'
        elif state == 'sel_url':
            download_dir_name = getattr(TorrentState, 'download_dir')
            delattr(TorrentState, 'download_dir')
            delattr(TorrentState, 'add_torrent_state')
            TransmissionCommands().add_torrent(download_dir=config.get_download_dir(download_dir_name), torrent=options)
            return 'Качаю!'
        else:
            setattr(TorrentState, 'add_torrent_state', 'sel_dir')
            torrent_type = [[telegram.KeyboardButton(config.torrent_types.get("music")),
                             telegram.KeyboardButton(config.torrent_types.get("movie"))],
                            [telegram.KeyboardButton(config.torrent_types.get("serial")),
                             telegram.KeyboardButton(config.torrent_types.get("anime"))
                             ],
                             [telegram.KeyboardButton(config.torrent_types.get("other"))]
                             ]
            self.reply_markup = telegram.ReplyKeyboardMarkup(torrent_type)
            return 'Выберите тип торрента'

    def rm_torrent(self, state=None, options=None):
        if state == 'rm':
            seltorrent = int(options.split('_')[0])
            delattr(TorrentState, 'rm_torrent_state')
            TransmissionCommands().rm_torrent(seltorrent)
            return 'Удалён!'
        else:
            setattr(TorrentState, 'rm_torrent_state', 'rm')
            rm_type = [["%i_%s" % (i['id'], i['name'])] for i in
                       TransmissionCommands().torrents_list(non_formated=True)]
            self.reply_markup = telegram.ReplyKeyboardMarkup(rm_type)
            return 'Выберите торрент для удаления'
