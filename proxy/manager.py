import asyncio
import logging
import threading
from typing import TYPE_CHECKING

from mitmproxy.options import Options
from mitmproxy.tools.dump import DumpMaster

from common import Singleton
from proxy.addon.danmaku_ws import DanmakuWebsocketAddon
from proxy.queues import MESSAGE_QUEUE

if TYPE_CHECKING:
    from config import ConfigManager

_log = logging.getLogger("ProxyManager")


class ProxyManager(metaclass=Singleton):
    _config_manager: "ConfigManager"

    def __init__(self, config_manager):
        self._config_manager = config_manager
        self._mitm_instance = None
        self._loop: "asyncio.AbstractEventLoop" = asyncio.new_event_loop()
        opts = Options(
            listen_host=self._config_manager.config['mitm']['host'],
            listen_port=self._config_manager.config['mitm']['port'],
        )

        async def _init_mitm_instance():
            _log.debug("初始化Mitm实例")
            self._mitm_instance = DumpMaster(options=opts)
            self._load_addon()
            opts.update_defer(
                flow_detail=0,
                termlog_verbosity="error",
            )
            _log.debug("初始化Mitm实例完毕")

        self._loop.run_until_complete(_init_mitm_instance())
        self._thread = None

    def terminate(self):
        if self._mitm_instance:
            _log.debug("关闭mitm实例")
            self._mitm_instance.shutdown()
            _log.info("关闭mitm实例完成")
        if self._loop:
            if self._loop.is_running():
                self._loop.stop()

    def _load_addon(self):
        self._mitm_instance.addons.add(DanmakuWebsocketAddon(MESSAGE_QUEUE))

    def _start(self):
        asyncio.set_event_loop(self._loop)
        if self._mitm_instance:
            self._loop.run_until_complete(self._mitm_instance.run())

    def start_loop(self):
        _log.debug("新建进程，运行mitm")
        self._thread = threading.Thread(target=self._start, args=())
        self._thread.start()
        _log.debug("新建进程，已运行mitm")

    def join(self):
        if self._thread:
            self._thread.join()
