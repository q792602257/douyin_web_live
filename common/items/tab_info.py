class TabInfo(object):
    TAB_TYPE_OTHER = "other"
    TAB_TYPE_USER = "user"
    TAB_TYPE_LIVE = "live"

    def __init__(self):
        self.tab_handler: str = ""
        """WebDriver中，该标签的句柄ID"""
        self.url: str = ""
        """标签地址"""
        self.tab_type: str = self.TAB_TYPE_OTHER
        """标签类型，展示用"""
        self.tab_keep: bool = False
        """关闭标签时，避免被误关"""
