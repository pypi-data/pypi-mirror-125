import hashlib
from threading import Thread

__all__ = ['md5', 'start']

md5 = lambda b: hashlib.md5(b).hexdigest()
start = lambda func, *args, **kwargs: Thread(target=func, args=args, kwargs=kwargs).start()
