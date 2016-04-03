from transmission_connector import TransmissionCommands


class ApiFunc:
    def __init__(self, cmd):
        cmds_dict = {
            'tor_status': self.torrent_status,
        }
        run = cmds_dict.get(cmd)
        if run:
            self.answer = run()
        else:
            self.answer = None

    def torrent_status(self):
        return TransmissionCommands().torrents_list()
