from .request import ZmqRequestMessage

#
# Implements all actions that can be performed on a car door
class ZmqDoorActions():

    def __init__(self):
        self.open_door = False
        self.close_door = False

    def doOpenDoor(self):
        self.open_door = True
        self.close_door = False

    def doCloseDoor(self):
        self.open_door = False
        self.close_door = True

    def isOpenDoorAction(self):
        return self.open_door

    def isCloseDoorAction(self):
        return self.close_door

#
# Wrapper for the doors, trunk, tank flap and bonnet
class ZmqClosuresActionWrapper():

    def __init__(self):
        self.doors = ZmqDoorsActionWrapper()

#
# Wrapper for the doors
class ZmqDoorsActionWrapper():
    def __init__(self):
        self.door_driver = ZmqDoorActions()
        self.door_passenger = ZmqDoorActions()

#
# Main car control message
class ZmqCarControlRequestMessage(ZmqRequestMessage):

    def __init__(self, status):
        super().__init__(status)

        #NOTE: Sub objects must be defined in the __init__()
        #  for them to be decoded by jsonpickle
        self.closures = ZmqClosuresActionWrapper()