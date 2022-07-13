import logging
from urllib.parse import urlparse

from common import Singleton
from common.items import TabInfo
from config import ConfigManager
from browser import BrowserManager
from proxy import ProxyManager

_log = logging.getLogger("CoreManager")
_log.setLevel(logging.DEBUG)


class CoreManager(metaclass=Singleton):
    config_manager: "ConfigManager"
    browser_manager: "BrowserManager"
    proxy_manager: "ProxyManager"

    def __del__(self):
        """
        析构CoreManager，需要gracefully shutdown
        """
        _log.debug("析构开始")
        try:
            _log.debug("析构浏览器管理器")
            self.browser_manager.terminate()
        except:
            pass
        finally:
            _log.debug("析构浏览器管理器完毕")
        try:
            _log.debug("析构Mitm代理管理器")
            self.proxy_manager.terminate()
        except:
            pass
        finally:
            _log.debug("析构Mitm代理管理器完毕")

    def __init__(self):
        """
        初始化CoreManager，初始化所有模块
        """
        _log.debug("初始化配置管理器")
        self.config_manager = ConfigManager()
        _log.info("初始化配置管理器完毕")
        _log.debug("初始化Mitm代理管理器")
        self.proxy_manager = ProxyManager(self.config_manager)
        self.proxy_manager.start_loop()
        _log.info("初始化Mitm代理管理器完毕")
        _log.debug("初始化浏览器管理器")
        self.browser_manager = BrowserManager(self.config_manager)
        _log.info("初始化浏览器管理器完毕")
        self._open_config_tabs()

    def restart(self):
        """服务有问题？重启一下把"""
        self.__del__()
        self.__init__()

    def open_tab(self, tab_info: "TabInfo"):
        self.browser_manager.open_tab(tab_info)

    def close_tab(self, tab_info: "TabInfo"):
        self.browser_manager.close_tab(tab_info)

    def _open_config_tabs(self):
        rooms = self.config_manager.config["douyin"]["rooms"]
        if type(rooms) is not list:
            rooms = [rooms]
        for room in rooms:
            if not urlparse(room).scheme:
                # 单独的房间号
                live_url = "https://live.douyin.com/" + room
            else:
                live_url = room
            tab_info = TabInfo()
            tab_info.url = live_url
            tab_info.tab_type = TabInfo.TAB_TYPE_LIVE
            self.open_tab(tab_info)
