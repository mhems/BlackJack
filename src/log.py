"""
Provide simple logging mechanism
"""

import os

FNAME = 'log.txt'

if os.path.exists(FNAME):
    os.remove(FNAME)

def log(msg):
    """Logs message to log file"""
    with open('log.txt', 'a') as fp:
        fp.write(msg)
