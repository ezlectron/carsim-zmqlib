from .base import ZmqBaseMessage

class ZmqRequestMessage(ZmqBaseMessage):

    def __init__(self, status):
        super().__init__(ZmqBaseMessage.MSG_TYPE_REQUEST, status)