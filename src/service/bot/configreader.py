"""
from : http://stackoverflow.com/questions/2819696/parsing-properties-file-in-python/2819788#2819788
"""
import ConfigParser


class FakeSecHead(object):
    def __init__(self, fp):
        self.fp = fp
        self.sechead = '[asection]\n'

    def readline(self):
        if self.sechead:
            try:
                return self.sechead
            finally:
                self.sechead = None
        else:
            return self.fp.readline()
