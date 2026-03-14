from .base import EngineSimZeroMqBaseMessage

class EngineSimZeroMqRequestMessage(EngineSimZeroMqBaseMessage):

    def __init__(self, status):
        super().__init__(EngineSimZeroMqBaseMessage.MSG_TYPE_REQUEST, status)