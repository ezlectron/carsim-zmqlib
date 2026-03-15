from .request import EngineSimZeroMqRequestMessage

#
# Implements all actions that can be performed on a car door
class EngineSimZeroMqDoorActions():

    def __init__(self):
        self._open_door = False
        self._close_door = False

    def doOpenDoor(self):
        self._open_door = True
        self._close_door = False

    def doCloseDoor(self):
        self._open_door = False
        self._close_door = True

    def isOpenDoorAction(self):
        return self._open_door

    def isCloseDoorAction(self):
        return self._close_door

#
# Main car control message
class EngineSimZeroMqCarControlRequestMessage(EngineSimZeroMqRequestMessage):

    def __init__(self, status):
        super().__init__(status)

        #NOTE: Sub objects must be defined in the __init__()
        #  for them to be decoded by jsonpickle
        self.door_driver = EngineSimZeroMqDoorActions()
        self.door_passenger = EngineSimZeroMqDoorActions()