import configparser
import os
import socket
import socks
from urllib.request import urlopen

config = configparser.ConfigParser()
config.read(os.path.join(os.path.dirname(__file__), '..', 'config.cfg'))


def saver(url):
    default_socket = socket.socket
    socks.set_default_proxy(socks.SOCKS5, addr=config.get('Proxy', 'host'), port=config.get('Proxy', 'port'),
                            username=config.get('Proxy', 'username'),
                            password=config.get('Proxy', 'password'))
    socket.socket = socks.socksocket

    tordata = urlopen(url)
    out_dir = config.get('Torrent', 'save_dir')
    with open(os.path.join(out_dir, os.path.basename(url)), 'wb') as torfile:
        torfile.write(tordata.read())


if __name__ == '__main__':
    saver('https://api.telegram.org/file/bot187344981:AAHqVACxMDhm4MT8v6uXrgywzEcvUgppD98/documents/file_40.torrent')
