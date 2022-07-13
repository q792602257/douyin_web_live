import contextlib
import logging
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from selenium.webdriver.remote.webdriver import WebDriver
    from config import ConfigManager

_log = logging.getLogger("IDriver")
_log.setLevel(logging.DEBUG)


class IDriver():
    browser: "WebDriver"
    _config_manager: "ConfigManager"

    def __init__(self, config_manager):
        self._config_manager = config_manager

    def terminate(self):
        self.browser.quit()

    def new_tab(self) -> str:
        ...

    def change_tab(self, tab_handler: str):
        ...

    def close_tab(self, tab_handler: str):
        ...

    def open_url(self, url: str, tab_handler: str = ""):
        ...

    @contextlib.contextmanager
    def op_tab(self, tab_handler: str):
        cur_handle = self.browser.current_window_handle
        _log.debug("切换Tab：旧Tab：%s，新Tab：%s", cur_handle, tab_handler)
        if tab_handler == "":
            tab_handler = cur_handle
        try:
            self.change_tab(tab_handler)
            _log.debug("切换至新Tab：%s", tab_handler)
            yield self
        finally:
            self.change_tab(cur_handle)
            _log.debug("切换至旧Tab：%s", cur_handle)

    def refresh(self, tab_handler: str = ""):
        ...

    def screenshot(self, tab_handler: str = "") -> str:
        ...
