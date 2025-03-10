import logging
from urllib.parse import urlparse

from common import Singleton
from common.items import TabInfo
from config import ConfigManager
from browser import BrowserManager
from proxy import ProxyManager
from output import OutputManager

_log = logging.getLogger("CoreManager")
_log.setLevel(logging.DEBUG)


class CoreManager(metaclass=Singleton):
    config_manager: "ConfigManager"
    browser_manager: "BrowserManager"
    proxy_manager: "ProxyManager"
    output_manager: "OutputManager"

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
        try:
            _log.debug("析构输出管理器")
            self.output_manager.terminate()
        except:
            pass
        finally:
            _log.debug("析构输出管理器完毕")

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
        _log.debug("初始化输出管理器")
        self.output_manager = OutputManager(self.config_manager)
        self.output_manager.start_loop()
        _log.info("初始化输出管理器完毕")
        self._open_config_tabs()

    def restart(self):
        """服务有问题？重启一下把"""
        self.__del__()
        self.__init__()

    def open_tab(self, url: "str", tab_type: "int" = TabInfo.TAB_TYPE_OTHER):
        tab_info = TabInfo()
        tab_info.url = url
        tab_info.tab_type = TabInfo.TAB_TYPE_LIVE
        self.browser_manager.open_tab(tab_info)

    def close_tab(self, url):
        handler = self.browser_manager.find_tab_handler_by_url(url)
        if handler is not None:
            tab_info = TabInfo()
            tab_info.tab_handler = handler
            self.browser_manager.close_tab(tab_info)

    def refresh_tab(self, tab_info):
        ...

    def on_broadcast(self, room_id: str):
        live_url = "https://live.douyin.com/" + room_id
        tab_info = TabInfo()
        tab_info.url = live_url
        tab_info.tab_type = TabInfo.TAB_TYPE_LIVE
        self.browser_manager.create_or_refresh(tab_info)

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
            self.open_tab(live_url, TabInfo.TAB_TYPE_LIVE)
