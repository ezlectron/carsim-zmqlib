from .response import EngineSimZeroMqResponseMessage

class EngineSimZeroMqDoorState():

    def __init__(self):
        self._is_door_open = False

    def setDoorState(self, state):
        self._is_door_open = state

    def getDoorIsOpen(self):
        return self._is_door_open

class EngineSimZeroMqCarStateResponseMessage(EngineSimZeroMqResponseMessage):

    def __init__(self, status):
        super().__init__(status)

        #NOTE: Sub objects must be defined in the __init__()
        #  for them to be decoded by jsonpickle
        self.door_driver = EngineSimZeroMqDoorState()