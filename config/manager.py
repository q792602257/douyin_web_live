import logging
import os

from ruamel.yaml import YAML

from common import Singleton

_log = logging.getLogger("ConfigManager")


class ConfigManager(metaclass=Singleton):
    """默认配置"""
    _default_config = {
        "mitm": {
            "host": "127.0.0.1",
            "port": 8080,
        },
        "webdriver": {
            "headless": False,
            "use": "chrome",
            "chrome": {
                "bin": "chromedriver",
                "no_sandbox": True
            }
        },
        "output": {
            "use": [],
            "xml": {
                "save_path": "./",
                "file_pattern": "{room_id}_{ts}.xml"
            },
            "debug": {
                "save_path": "./debug",
                "known": False
            },
        },
        "douyin": {
            "rooms": [],
            "users": [],
        },
    }
    """配置文件路径"""
    _config_file: "os.PathLike[str] || str"
    """当前实例中，配置文件内容"""
    _current_config: "dict" = {}

    def __init__(self, config_file="settings.yml"):
        _log.debug("配置文件路径：%s", config_file)
        self._config_file = config_file
        if not os.path.exists(config_file):
            _log.warning("配置文件不存在，写入初始化配置")
            self._current_config = self._default_config
            self.save_config()
        else:
            self.load_config()

    def load_config(self):
        _log.debug("读取文件%s的配置内容", self._config_file)
        with open(self._config_file, "r", encoding="UTF8") as _f:
            yaml = YAML(typ="unsafe", pure=True)
            self._current_config = yaml.load(_f)
        _log.debug("读取文件%s的配置内容完毕", self._config_file)

    def save_config(self):
        _log.debug("向文件%s写入配置", self._config_file)
        with open(self._config_file, "w", encoding="UTF8") as _f:
            _log.debug("配置内容：", self._current_config)
            yaml = YAML(typ="unsafe", pure=True)
            yaml.dump(self._current_config, _f)
        _log.debug("向文件%s写入配置完毕", self._config_file)

    @property
    def config(self):
        return self._current_config

    def get(self, key: str, default: str = None):
        ...
