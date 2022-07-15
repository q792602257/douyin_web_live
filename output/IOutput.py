from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from messages.base import Base
    from messages.chat import ChatMessage
    from messages.control import ControlMessage
    from messages.fansclub import FansclubMessage
    from messages.gift import GiftMessage
    from messages.like import LikeMessage
    from messages.member import MemberMessage
    from messages.roomuserseq import RoomUserSeqMessage
    from messages.social import SocialMessage
    from config import ConfigManager


class IOutput():
    _config_manager: "ConfigManager"

    def __del__(self):
        self.terminate()

    def __init__(self, config_manager: "ConfigManager"):
        self._config_manager = config_manager

    def output(self, message_type: str, message_obj: "Base"):
        ...

    def chat_output(self, message: "ChatMessage"):
        ...

    def like_output(self, message: "LikeMessage"):
        ...

    def member_output(self, message: "MemberMessage"):
        ...

    def social_output(self, message: "SocialMessage"):
        ...

    def gift_output(self, message: "GiftMessage"):
        ...

    def userseq_output(self, message: "RoomUserSeqMessage"):
        ...

    def control_output(self, message: "ControlMessage"):
        ...

    def fansclub_output(self, message: "FansclubMessage"):
        ...

    def other_output(self, message_type: str, message_raw: bytes):
        ...

    def debug_output(self, message_type: str, message_raw: str):
        ...

    def error_output(self, message_type: str, message_raw: bytes, exception: Exception):
        ...

    def terminate(self):
        ...