import gzip
import threading
from typing import TYPE_CHECKING

from common import Singleton
from messages.chat import ChatMessage
from messages.control import ControlMessage
from messages.fansclub import FansclubMessage
from messages.gift import GiftMessage
from messages.like import LikeMessage
from messages.member import MemberMessage
from messages.roomuserseq import RoomUserSeqMessage
from messages.social import SocialMessage
from output.debug import DebugWriter
from output.print import Print
from output.xml import XMLWriter
from protobuf import message_pb2, wss_pb2
from proxy.queues import MESSAGE_QUEUE

if TYPE_CHECKING:
    from typing import Type, Optional, List
    from output.IOutput import IOutput
    from proxy.common import MessagePayload
    from config import ConfigManager


class OutputManager(metaclass=Singleton):
    _config_manager: "ConfigManager"
    _mapping: "dict[str, Type[IOutput]]" = {
        "print": Print,
        "xml": XMLWriter,
        "debug": DebugWriter,
    }
    _writer: "List[IOutput]" = []
    _thread: "Optional[threading.Thread]"= None
    _should_exit = threading.Event()

    def __init__(self, config_manager: "ConfigManager"):
        self._config_manager = config_manager
        _config = self._config_manager.config['output']['use']
        if type(_config) != list:
            _config = [_config]
        for _c in _config:
            if _c not in self._mapping:
                raise Exception("不支持的输出方式")
            self._writer.append(self._mapping[_c](self._config_manager))

    def __del__(self):
        self.terminate()

    def decode_payload(self, message: "MessagePayload"):
        try:
            response = message_pb2.Response()
            wss = wss_pb2.WssResponse()
            wss.ParseFromString(message.body)
            decompressed = gzip.decompress(wss.data)
            response.ParseFromString(decompressed)
            self.decode_message(response.messages)
        except Exception as e:
            for writer in self._writer:
                writer.error_output("ParseError", message.body, e)

    def decode_message(self, message_list: "List[message_pb2.Message]"):
        for message in message_list:
            try:
                if message.method == 'WebcastMemberMessage':
                    member_message = MemberMessage()
                    member_message.set_payload(message.payload)
                    for writer in self._writer:
                        writer.member_output(member_message)
                elif message.method == 'WebcastSocialMessage':
                    social_message = SocialMessage()
                    social_message.set_payload(message.payload)
                    for writer in self._writer:
                        writer.social_output(social_message)
                elif message.method == 'WebcastChatMessage':
                    chat_message = ChatMessage()
                    chat_message.set_payload(message.payload)
                    for writer in self._writer:
                        writer.chat_output(chat_message)
                elif message.method == 'WebcastLikeMessage':
                    like_message = LikeMessage()
                    like_message.set_payload(message.payload)
                    for writer in self._writer:
                        writer.like_output(like_message)
                elif message.method == 'WebcastGiftMessage':
                    gift_message = GiftMessage()
                    gift_message.set_payload(message.payload)
                    for writer in self._writer:
                        writer.gift_output(gift_message)
                elif message.method == 'WebcastRoomUserSeqMessage':
                    room_user_seq_message = RoomUserSeqMessage()
                    room_user_seq_message.set_payload(message.payload)
                    for writer in self._writer:
                        writer.userseq_output(room_user_seq_message)
                elif message.method == 'WebcastControlMessage':
                    control_message = ControlMessage()
                    control_message.set_payload(message.payload)
                    for writer in self._writer:
                        writer.control_output(control_message)
                elif message.method == 'WebcastFansclubMessage':
                    fansclub_message = FansclubMessage()
                    fansclub_message.set_payload(message.payload)
                    for writer in self._writer:
                        writer.fansclub_output(fansclub_message)
                else:
                    for writer in self._writer:
                        writer.other_output(message.method, message.payload)
            except Exception as e:
                for writer in self._writer:
                    writer.error_output(message.method, message.payload, e)

    def start_loop(self):
        self._should_exit.clear()
        self._thread = threading.Thread(target=self._handle)
        self._thread.start()

    def _handle(self):
        while True:
            message = MESSAGE_QUEUE.get()
            if self._should_exit.is_set():
                break
            if message is None:
                continue
            self.decode_payload(message)

    def terminate(self):
        if not self._should_exit.is_set():
            self._should_exit.set()
        MESSAGE_QUEUE.put(None)

        for writer in self._writer:
            writer.terminate()
