import logging
from selenium import webdriver
from selenium.webdriver import Proxy, DesiredCapabilities
from selenium.webdriver.common.proxy import ProxyType

from browser.IDriver import IDriver
from selenium.webdriver.chrome.options import Options

_log = logging.getLogger("ChromeDriver")
_log.setLevel(logging.DEBUG)

class ChromeDriver(IDriver):
    def __init__(self, config_manager):
        super(ChromeDriver, self).__init__(config_manager)
        options = Options()
        if self._config_manager.config['webdriver']['headless']:
            options.add_argument("--headless")
            options.add_argument("--window-size=1920,1080")
        options.add_argument('--proxy-server=%s:%s' % (self._config_manager.config['mitm']['host'], self._config_manager.config['mitm']['port']))
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--ignore-ssl-errors')
        options.add_argument('--incognito')
        options.add_experimental_option('excludeSwitches', ['ignore-certificate-errors'])
        if self._config_manager.config['webdriver']['chrome']['no_sandbox']:
            _log.debug("添加启动参数NoSandbox")
            options.add_argument('--no-sandbox')
        proxy = Proxy()
        proxy.proxy_type = ProxyType.MANUAL
        proxy.http_proxy = "%s:%s" % (self._config_manager.config['mitm']['host'], self._config_manager.config['mitm']['port'])
        proxy.ssl_proxy = "%s:%s" % (self._config_manager.config['mitm']['host'], self._config_manager.config['mitm']['port'])
        capabilities = DesiredCapabilities.CHROME
        proxy.add_to_capabilities(capabilities)

        self.browser = webdriver.Chrome(options=options,
                                        desired_capabilities=capabilities,
                                        executable_path=self._config_manager.config['webdriver']['chrome']['bin']
                                        )
        _log.info("浏览器启动完毕")

    def new_tab(self) -> str:
        current_window_handles = self.browser.window_handles
        self.browser.execute_script("window.open('')")
        new_window_handles = self.browser.window_handles
        for _handle in new_window_handles:
            if _handle not in current_window_handles:
                _log.debug("新窗口句柄：%s", _handle)
                return _handle
        _log.warning("打开新窗口，未发现新句柄")
        return ""

    def change_tab(self, tab_handler: str):
        if tab_handler not in self.browser.window_handles:
            return
        self.browser.switch_to.window(tab_handler)

    def close_tab(self, tab_handler: str):
        with self.op_tab(tab_handler):
            self.browser.close()

    def open_url(self, url: str, tab_handler: str = ""):
        with self.op_tab(tab_handler):
            self.browser.get(url)

    def refresh(self, tab_handler: str = ""):
        with self.op_tab(tab_handler):
            self.browser.refresh()

    def screenshot(self, tab_handler: str = "") -> str:
        with self.op_tab(tab_handler):
            return self.browser.get_screenshot_as_base64()
