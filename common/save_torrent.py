import configparser
import os
from urllib3.contrib.socks import SOCKSProxyManager

config = configparser.ConfigParser()
config.read(os.path.join(os.path.dirname(__file__), '..', 'config.cfg'))


def saver(url):
    mgr = SOCKSProxyManager('socks5://%s:%s/' % (config.get('Proxy', 'host'),
                                                 config.get('Proxy', 'port')),
                            **{'username': config.get('Proxy', 'username'),
                               'password': config.get('Proxy', 'password')}
                            )
    tordata = mgr.request('GET', url, headers={'connection': 'keep-alive'}).data
    out_dir = config.get('Torrent', 'save_dir')
    with open(os.path.join(out_dir, os.path.basename(url)), 'wb') as torfile:
        torfile.write(tordata)
    return tordata


if __name__ == '__main__':
    saver('https://api.telegram.org/file/bot187344981:AAHqVACxMDhm4MT8v6uXrgywzEcvUgppD98/documents/file_40.torrent')
