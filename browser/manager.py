import logging
from typing import TYPE_CHECKING

from browser.chrome import ChromeDriver
from common import Singleton

if TYPE_CHECKING:
    from typing import Type, List, Optional
    from browser.IDriver import IDriver
    from config import ConfigManager
    from common.items import TabInfo

_log = logging.getLogger("BrowserManager")


class BrowserManager(metaclass=Singleton):
    _config_manager: "ConfigManager"
    _mapping: "dict[str, Type[IDriver]]" = {
        "chrome": ChromeDriver,
    }

    def __init__(self, config_manager: "ConfigManager"):
        self._config_manager = config_manager
        _config = self._config_manager.config["webdriver"]["use"]
        if _config not in self._mapping:
            _log.error("不支持的浏览器：%s", _config)
            raise Exception("不支持的浏览器")
        self._driver: IDriver = self._mapping[_config](self._config_manager)
        self._tabs: "List[TabInfo]" = []
        _log.debug("初始化完毕")

    def _check_tab_valid(self, tab_info: "TabInfo") -> "bool":
        if tab_info not in self._tabs:
            for _tab in self._tabs:
                if _tab.tab_handler == tab_info.tab_handler:
                    return True
            return False
        return True

    @property
    def driver(self):
        return self._driver

    def open_tab(self, tab_info: "TabInfo"):
        if not tab_info.tab_handler:
            tab_handler = self._driver.new_tab()
            tab_info.tab_handler = tab_handler
        if not tab_info.tab_type:
            tab_info.tab_type = TabInfo.TAB_TYPE_OTHER
        _log.debug("打开URL：【%s】@%s", tab_info.url, tab_info.tab_handler)
        self.driver.open_url(tab_info.url, tab_info.tab_handler)
        _log.info("打开URL完毕：【%s】@%s", tab_info.url, tab_info.tab_handler)
        if tab_info not in self._tabs:
            self._tabs.append(tab_info)

    def close_tab(self, tab_info: "TabInfo"):
        if self._check_tab_valid(tab_info):
            _log.warning("提供的标签不在标签组中，不予执行")
            return
        _log.debug("关闭标签：%s", tab_info.tab_handler)
        self._driver.close_tab(tab_info.tab_handler)
        _log.info("关闭标签完毕：%s", tab_info.tab_handler)
        self._tabs.remove(tab_info)

    def refresh_tab(self, tab_info: "TabInfo"):
        if self._check_tab_valid(tab_info):
            _log.warning("提供的标签不在标签组中，不予执行")
            return
        _log.debug("刷新标签：%s", tab_info.tab_handler)
        self._driver.refresh(tab_info.tab_handler)

    def terminate(self):
        if self._driver:
            self._driver.terminate()

    def find_tab_handler_by_url(self, url: str) -> "Optional[str]":
        for tab_info in self._tabs:
            if url == tab_info.url:
                return tab_info.tab_handler

    def create_or_refresh(self, tab_info: "TabInfo") -> "str":
        handler = self.find_tab_handler_by_url(tab_info.url)
        if handler is not None:
            tab_info.tab_handler = handler
            self.refresh_tab(tab_info)
        else:
            self.open_tab(tab_info)
        return tab_info.tab_handler