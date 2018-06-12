FNAME = 'log.txt'

import os

if os.path.exists(FNAME):
    os.remove(FNAME)

def log(msg):
    with open('log.txt', 'a') as fp:
        fp.write(msg)
