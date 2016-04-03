from transmission_connector import TransmissionCommands


class ApiFunc:
    def __init__(self, cmd):
        cmds_dict = {
            'tor_status': self.torrent_status,
            'tor_serv_info': self.torrent_server_info,
        }
        run = cmds_dict.get(cmd)
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
