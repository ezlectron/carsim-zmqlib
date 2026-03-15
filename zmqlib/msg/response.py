from .base import ZmqBaseMessage

class ZmqResponseMessage(ZmqBaseMessage):

    def __init__(self, status):
        super().__init__(ZmqBaseMessage.MSG_TYPE_RESPONSE, status)