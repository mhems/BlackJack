####################
#
# Logger.py
#
####################

import os

from src.Utilities.Utilities import LINE_END

class Logger:
    """Mechanism for central logging and data aggregation"""

    # Yes this is ugly and possibly incorrect

    def __init__(self, location, append=False):
        d = os.path.dirname(location)
        if not os.path.exists(d):
            os.makedirs(d)
        self.logfile = open(location, 'a' if append else 'w')

    def __enter__(self):
        return self

    def __exit__(self, exctype, value, tb):
        self.close()
        return False

    def log(self, msg='', *args):
        self.logfile.write(str(msg) % args)

    def close(self):
        self.logfile.close()
