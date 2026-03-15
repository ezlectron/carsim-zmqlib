from .request import ZmqRequestMessage

#
# Implements all actions that can be performed on a car door
class ZmqDoorActions():

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
class ZmqCarControlRequestMessage(ZmqRequestMessage):

    def __init__(self, status):
        super().__init__(status)

        #NOTE: Sub objects must be defined in the __init__()
        #  for them to be decoded by jsonpickle
        self.door_driver = ZmqDoorActions()
        self.door_passenger = ZmqDoorActions()