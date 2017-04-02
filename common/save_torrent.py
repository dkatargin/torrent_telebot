import configparser
import os
from urllib.request import urlopen

config = configparser.ConfigParser()
config.read(os.path.join(os.path.dirname(__file__), '..', 'config.cfg'))


def saver(url):
    tordata = urlopen(url)
    out_dir = config.get('Torrent', 'save_dir')
    with open(os.path.join(out_dir, os.path.basename(url)), 'wb') as torfile:
        torfile.write(tordata.read())


if __name__ == '__main__':
    saver('https://api.telegram.org/file/bot187344981:AAHqVACxMDhm4MT8v6uXrgywzEcvUgppD98/documents/file_40.torrent')
