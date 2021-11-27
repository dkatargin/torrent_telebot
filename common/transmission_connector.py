import configparser

import transmission_rpc

from common.size_converter import SizeConverter


class TransmissionCommands:
    def __init__(self):
        config = configparser.ConfigParser()
        config.read("config.cfg")
        self.tc = transmission_rpc.Client(
            host=config["TransmissionRPC"]["server"],
            port=config["TransmissionRPC"]["port"],
            username=config["TransmissionRPC"]["user"],
            password=config["TransmissionRPC"]["password"],
        )
        self.download_dir = config["Torrent"]["save_dir"]

    def torrents_list(self, non_formated=False):
        torrents = self.tc.get_torrents()
        if not torrents:
            return "_No torrents found_"
        tor_list = []
        for t in torrents:
            updated_date = t.date_added
            if t.status == "downloading":
                try:
                    status = "(закач. %s%s осталось %s)" % (
                        "{0:.2f}".format(t.progress),
                        "%",
                        t.eta,
                    )
                except:
                    status = str(t.progress)
            else:
                status = ""
            tor_list.append(
                {"name": t.name, "u_date": updated_date, "status": status, "id": t.id}
            )
        s_tor_list = sorted(tor_list, key=lambda k: k["u_date"])
        if non_formated:
            return s_tor_list
        result_str = ""
        for st in reversed(s_tor_list):
            result_str += "_%s_ %s\n*%s* \n\n" % (
                str(st["u_date"]),
                st["status"],
                st["name"],
            )
        return result_str

    def server_info(self):
        size_is = "{0:.2S}".format(
            SizeConverter(int(self.tc.free_space(self.download_dir)))
        )
        result_str = "Space available: %s" % size_is
        return result_str

    def add_torrent(self, download_dir, torrent):
        result = self.tc.add_torrent(torrent, download_dir=download_dir)
        return result

    def rm_torrent(self, torrent_name):
        result = self.tc.remove_torrent(ids=torrent_name, delete_data=True)
        return result


if __name__ == "__main__":
    TransmissionCommands().server_info()
