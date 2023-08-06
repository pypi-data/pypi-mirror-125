import os
import time


def tag():
    return time.strftime('[%Y-%m-%d %H:%M:%S] ')


def unique(p, dash='-'):
    root, ext = os.path.splitext(p)
    n = 0
    while os.path.exists(p):
        n += 1
        p = '%s%s%d%s' % (root, dash, n, ext)
    return p


def log(text):
    pass

