import configparser
import transmissionrpc
from common.size_converter import SizeConverter


class TransmissionCommands:
    def __init__(self):
        config = configparser.ConfigParser()
        config.read('config.cfg')
        self.tc = transmissionrpc.Client(address=config['TransmissionRPC']['server'],
                                         user=config['TransmissionRPC']['user'],
                                         password=config['TransmissionRPC']['password'])

    def torrents_list(self):
        tor_list = []
        for t in self.tc.get_torrents():
            updated_date = t.date_added
            if t.status == 'downloading':
                status = "(закач. %s%s осталось %s)" % ("{0:.2f}".format(t.progress), '%', t.eta)
            else:
                status = ''
            tor_list.append({'name': t.name, 'u_date': updated_date, 'status': status})
        s_tor_list = sorted(tor_list, key=lambda k: k['u_date'])
        result_str = ''
        for st in reversed(s_tor_list):
            result_str += '_%s_ %s\n*%s* \n\n' % (str(st['u_date']), st['status'], st['name'])
        return result_str

    def server_info(self):
        size_is = "{0:.2S}".format(SizeConverter(int(self.tc.free_space('/mnt/Public'))))
        result_str = 'Space available: %s' % size_is
        return result_str

    def add_torrent(self, download_dir, torrent_url):
        result = self.tc.add_torrent(torrent=torrent_url, download_dir=download_dir)
        return result

if __name__ == '__main__':
    TransmissionCommands().server_info()


