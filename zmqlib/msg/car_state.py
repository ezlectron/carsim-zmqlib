from .response import ZmqResponseMessage

#
# Represents the state of a car door and its features (locks, windows, etc.)
class ZmqDoorState():

    def __init__(self):
        self._is_door_open = False

    def setDoorState(self, state):
        self._is_door_open = state

    def getDoorIsOpen(self):
        return self._is_door_open

#
# Main car state response message
class ZmqCarStateResponseMessage(ZmqResponseMessage):

    def __init__(self, status):
        super().__init__(status)

        #NOTE: Sub objects must be defined in the __init__()
        #  for them to be decoded by jsonpickle
        self.door_driver = ZmqDoorState()
        self.door_passenger = ZmqDoorState()