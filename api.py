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


class ApiFunc:
    def __init__(self, cmd):
        print('Torrent INFO', getattr(self, 'add_torrent_info', None))
        cmds_dict = {
            b'\xf0\x9f\x93\xb0\xd0\xa1\xd1\x82\xd0\xb0\xd1\x82\xd1\x83\xd1\x81 \xd0\xb7\xd0\xb0\xd0\xba\xd0\xb0\xd1\x87\xd0\xb5\xd0\xba': self.torrent_status,
            b'\xf0\x9f\x93\xae\xd0\x94\xd0\xbe\xd0\xb1\xd0\xb0\xd0\xb2\xd0\xb8\xd1\x82\xd1\x8c \xd1\x82\xd0\xbe\xd1\x80\xd1\x80\xd0\xb5\xd0\xbd\xd1\x82': self.add_torrent,
            'tor_serv_info': self.torrent_server_info,
        }
        run = cmds_dict.get(cmd.encode('UTF-8'))
        custom_keyboard = [[telegram.KeyboardButton(telegram.Emoji.NEWSPAPER + 'Статус закачек'),
                            telegram.KeyboardButton(telegram.Emoji.POSTBOX + "Добавить торрент"),
                            telegram.KeyboardButton(
                                telegram.Emoji.BLACK_UNIVERSAL_RECYCLING_SYMBOL + "Удалить торрент")]]

        self.reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard)
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

    def add_torrent(self):

        setattr(self, 'add_torrent_info', 'HasInfo')

        torrent_type = [[telegram.KeyboardButton(telegram.Emoji.MUSICAL_NOTE + 'Музыка'),
                              telegram.KeyboardButton(telegram.Emoji.CINEMA + "Фильм"),
                              telegram.KeyboardButton(telegram.Emoji.FAMILY + "Сериал"),
                              telegram.KeyboardButton(
                                  telegram.Emoji.JAPANESE_DOLLS + "Аниме")
                              ]]
        self.reply_markup = telegram.ReplyKeyboardMarkup(torrent_type)
        return 'Выберите тип торрента'

