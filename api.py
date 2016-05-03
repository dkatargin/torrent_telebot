from transmission_connector import TransmissionCommands
import telegram


torrent_types = {b'\xf0\x9f\x8e\xb5\xd0\x9c\xd1\x83\xd0\xb7\xd1\x8b\xd0\xba\xd0\xb0': 'music',
                 b'\xf0\x9f\x8e\xa6\xd0\xa4\xd0\xb8\xd0\xbb\xd1\x8c\xd0\xbc': 'movie',
                 b'\xf0\x9f\x91\xaa\xd0\xa1\xd0\xb5\xd1\x80\xd0\xb8\xd0\xb0\xd0\xbb': 'serial',
                 b'\xf0\x9f\x8e\x8e\xd0\x90\xd0\xbd\xd0\xb8\xd0\xbc\xd0\xb5': 'anime'}

torrent_dirs = {
    'music': '/mnt/Public/Shared Music/',
    'movie': '/mnt/Public/Shared Videos/Movies',
    'serial': '/mnt/Public/Shared Videos/Serials',
    'anime': '/mnt/Public/Shared Videos/Anime',
}


class TorrentState:
    pass


class ApiFunc:
    def __init__(self, cmd):
        custom_keyboard = [[telegram.KeyboardButton(telegram.Emoji.NEWSPAPER + 'Статус закачек'),
                            telegram.KeyboardButton(telegram.Emoji.INFORMATION_SOURCE + "Информация")],
                           [telegram.KeyboardButton(telegram.Emoji.POSTBOX + "Добавить торрент")],
                           [telegram.KeyboardButton(
                               telegram.Emoji.BLACK_UNIVERSAL_RECYCLING_SYMBOL + "Удалить торрент")]
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
            b'\xf0\x9f\x93\xb0\xd0\xa1\xd1\x82\xd0\xb0\xd1\x82\xd1\x83\xd1\x81 \xd0\xb7\xd0\xb0\xd0\xba\xd0\xb0\xd1\x87\xd0\xb5\xd0\xba': self.torrent_status,
            b'\xf0\x9f\x93\xae\xd0\x94\xd0\xbe\xd0\xb1\xd0\xb0\xd0\xb2\xd0\xb8\xd1\x82\xd1\x8c \xd1\x82\xd0\xbe\xd1\x80\xd1\x80\xd0\xb5\xd0\xbd\xd1\x82': self.add_torrent,
            b'\xe2\x99\xbb\xd0\xa3\xd0\xb4\xd0\xb0\xd0\xbb\xd0\xb8\xd1\x82\xd1\x8c \xd1\x82\xd0\xbe\xd1\x80\xd1\x80\xd0\xb5\xd0\xbd\xd1\x82': self.rm_torrent,
            b'\xe2\x84\xb9\xd0\x98\xd0\xbd\xd1\x84\xd0\xbe\xd1\x80\xd0\xbc\xd0\xb0\xd1\x86\xd0\xb8\xd1\x8f': self.torrent_server_info,
        }
        run = cmds_dict.get(cmd.encode('UTF-8'))

        if run:
            self.answer = run()
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
            seldir = torrent_types[options.encode('UTF-8')]
            setattr(TorrentState, 'download_dir', seldir)
            setattr(TorrentState, 'add_torrent_state', 'sel_url')
            return 'Загрузите торрент-файл'
        elif state == 'sel_url':
            download_dir = getattr(TorrentState, 'download_dir')
            delattr(TorrentState, 'download_dir')
            delattr(TorrentState, 'add_torrent_state')
            TransmissionCommands().add_torrent(download_dir=torrent_dirs[download_dir], torrent_url=options)
            return 'Качаю!'
        else:
            setattr(TorrentState, 'add_torrent_state', 'sel_dir')
            torrent_type = [[telegram.KeyboardButton(telegram.Emoji.MUSICAL_NOTE + 'Музыка'),
                                  telegram.KeyboardButton(telegram.Emoji.CINEMA + "Фильм")],
                            [telegram.KeyboardButton(telegram.Emoji.FAMILY + "Сериал"),
                             telegram.KeyboardButton(telegram.Emoji.JAPANESE_DOLLS + "Аниме")
                                  ]]
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
            rm_type = [["%i_%s" % (i['id'], i['name'])] for i in TransmissionCommands().torrents_list(non_formated=True)]
            self.reply_markup = telegram.ReplyKeyboardMarkup(rm_type)
            return 'Выберите торрент для удаления'
