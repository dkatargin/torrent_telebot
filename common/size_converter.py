import math


class SizeConverter(int):
    def __format__(self, fmt):
        if fmt == "" or fmt[-1] != "S":
            if fmt[-1].tolower() in ['b', 'c', 'd', ' o', 'x', 'n', 'e', 'f', 'g', '%']:
                return int(self).__format__(fmt)
            else:
                return str(self).__format__(fmt)

        val, s = float(self), ["b ", "Kb", "Mb", "Gb", "Tb", "Pb"]
        if val < 1:
            i, v = 0, 0
        else:
            i = int(math.log(val, 1024))+1
            v = val / math.pow(1024, i)
            v, i = (v, i) if v > 0.5 else (v*1024, i-1)
        return ("{0:{1}f}"+s[i]).format(v, fmt[:-1])
