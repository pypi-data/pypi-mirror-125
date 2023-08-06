import os
from functools import partial

_open = open

join = os.path.join
makedirs = partial(os.makedirs, exist_ok=True)
open = partial(open, encoding='u8')


def split(p):
    root, file = os.path.split(p)
    name, ext = os.path.splitext(file)
    return root, name, ext


def walk(path, exts=()):
    for root, folders, files in os.walk(path):
        for file in files:
            if not exts or os.path.splitext(file)[1] in exts:
                yield os.path.join(root, file)


def read(file):
    with open(file) as f:
        return f.read()


def write(file, s):
    with open(file, 'r') as f:
        return f.write(s)

