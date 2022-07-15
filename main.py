import logging
import atexit
from flask import Flask

from core import CoreManager
from core.controller.manager_blueprint import blueprint as manager_blueprint

app = Flask(__name__)
app.register_blueprint(manager_blueprint)


def _on_exit():
    c = CoreManager()
    del c


atexit.register(_on_exit)

if __name__ == '__main__':
    c = CoreManager()
    app.run()
