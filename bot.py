import emoji
import telegram
from transmission_connector import TransmissionCommands
from common import save_torrent

# Buttons
download_state = emoji.emojize(":traffic_light: Статус закачек", use_aliases=True)
info = emoji.emojize(":information_source: Информация", use_aliases=True)
add_torrent = emoji.emojize(":postbox: Добавить торрент", use_aliases=True)
rm_torrent = emoji.emojize(":wastebasket: Удалить торрент", use_aliases=True)

torrent_types = {emoji.emojize(":headphones: Музыка", use_aliases=True): 'music',
                 emoji.emojize(":movie_camera: Фильм", use_aliases=True): 'movie',
                 emoji.emojize(":popcorn: Сериал", use_aliases=True): 'serial',
                 emoji.emojize(":sushi: Аниме", use_aliases=True): 'anime'}

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
        custom_keyboard = [[telegram.KeyboardButton(download_state),
                            telegram.KeyboardButton(info)],
                           [telegram.KeyboardButton(add_torrent)],
                           [telegram.KeyboardButton(rm_torrent)]
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
            download_state: self.torrent_status,
            add_torrent: self.add_torrent,
            rm_torrent: self.rm_torrent,
            info: self.torrent_server_info,
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
            seldir = torrent_types[options]
            setattr(TorrentState, 'download_dir', seldir)
            setattr(TorrentState, 'add_torrent_state', 'sel_url')
            return 'Загрузите торрент-файл'
        elif state == 'sel_url':
            download_dir = getattr(TorrentState, 'download_dir')
            delattr(TorrentState, 'download_dir')
            delattr(TorrentState, 'add_torrent_state')
            save_torrent.saver(options)
            TransmissionCommands().add_torrent(download_dir=torrent_dirs[download_dir], torrent_url=options)
            return 'Качаю!'
        else:
            setattr(TorrentState, 'add_torrent_state', 'sel_dir')
            torrent_type = [[telegram.KeyboardButton(emoji.emojize(":headphones: Музыка", use_aliases=True)),
                             telegram.KeyboardButton(emoji.emojize(":movie_camera: Фильм", use_aliases=True))],
                            [telegram.KeyboardButton(emoji.emojize(":popcorn: Сериал", use_aliases=True)),
                             telegram.KeyboardButton(emoji.emojize(":sushi: Аниме", use_aliases=True))
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
            rm_type = [["%i_%s" % (i['id'], i['name'])] for i in
                       TransmissionCommands().torrents_list(non_formated=True)]
            self.reply_markup = telegram.ReplyKeyboardMarkup(rm_type)
            return 'Выберите торрент для удаления'
