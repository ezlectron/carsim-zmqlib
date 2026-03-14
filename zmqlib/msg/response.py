from .base import EngineSimZeroMqBaseMessage

class EngineSimZeroMqResponseMessage(EngineSimZeroMqBaseMessage):

    def __init__(self, status):
        super().__init__(EngineSimZeroMqBaseMessage.MSG_TYPE_RESPONSE, status)