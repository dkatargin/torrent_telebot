import os
import configparser
import emoji

config = configparser.ConfigParser()
config.read('config.cfg')

# Buttons
btn_download_state = emoji.emojize(":traffic_light: Статус закачек", use_aliases=True)
btn_info = emoji.emojize(":information_source: Информация", use_aliases=True)
btn_add_torrent = emoji.emojize(":postbox: Добавить торрент", use_aliases=True)
btn_rm_torrent = emoji.emojize(":wastebasket: Удалить торрент", use_aliases=True)

torrent_types = {
    'music': emoji.emojize(":headphones: Музыка", use_aliases=True),
    'movie': emoji.emojize(":movie_camera: Фильм", use_aliases=True),
    'serial': emoji.emojize(":popcorn: Сериал", use_aliases=True),
    'anime': emoji.emojize(":sushi: Аниме", use_aliases=True),
    'other': emoji.emojize(":basket: Другое", use_aliases=True)
}

def get_type_by_emoji(emoji):
    for n,em in torrent_types.items():
        if emoji == em:
            return n

def get_download_dir(type_name):
    if not torrent_types.get(type_name):
        return
    return os.path.join(config.get("Torrent", "save_dir"), type_name)

def get_proxy_settings():
    proxy_config = {}
    if config.get('Proxy', 'host') and config.get('Proxy', 'port'):
        proxy_config = {'proxy_url': 'socks5://%s:%s/' % (config.get('Proxy', 'host'), config.get('Proxy', 'port')),
                        'urllib3_proxy_kwargs': {'username': config.get('Proxy', 'username'),
                                                 'password': config.get('Proxy', 'password')}}
    return proxy_config
