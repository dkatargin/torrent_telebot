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
            status = t.status
            tor_list.append({'name': t.name, 'u_date': updated_date, 'status': status})
        s_tor_list = sorted(tor_list, key=lambda k: k['u_date'])
        result_str = ''
        for st in reversed(s_tor_list):
            result_str += '_%s_\n*%s* \n\n' % (str(st['u_date']), st['name'])
        return result_str

    def server_info(self):
        size_is = "{0:.2S}".format(SizeConverter(int(self.tc.free_space('/mnt/Public'))))
        result_str = 'Space available: %s' % size_is
        return result_str

if __name__ == '__main__':
    TransmissionCommands().server_info()


