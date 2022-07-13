import logging
import atexit

from core import CoreManager

logging.basicConfig(level=logging.INFO)


def _on_exit():
    c = CoreManager()
    del c


atexit.register(_on_exit)

if __name__ == '__main__':
    c = CoreManager()
    c.proxy_manager.join()
