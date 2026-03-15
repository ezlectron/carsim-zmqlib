from .response import ZmqResponseMessage

#
# Represents the state of a car door and its features (locks, windows, etc.)
class ZmqDoorState():

    def __init__(self, name, position):
        self.name = name
        self.position = position
        self.is_door_open = False
        self.is_lock_locked = False

    def setDoorState(self, state):
        self.is_door_open = state

    def setLockState(self, state):
        self.is_lock_locked = state

    def getDoorIsOpen(self):
        return self.is_door_open

    def getLockIsLocked(self):
        return self.is_lock_locked

#
# Wrapper for the doors, trunk, tank flap and bonnet
class ZmqCarClosuresStateWrapper():
    def __init__(self):
        self.doors = ZmqCarDoorsStateWrapper()

#
# Wrapper for the doors
class ZmqCarDoorsStateWrapper():

    def __init__(self):
        self.door_driver = ZmqDoorState("Driver door", "Front Left")
        self.door_passenger = ZmqDoorState("Passenger door", "Front Right")

#
# Main car state response message
class ZmqCarStateResponseMessage(ZmqResponseMessage):

    def __init__(self, status):
        super().__init__(status)

        #NOTE: Sub objects must be defined in the __init__()
        #  for them to be decoded by jsonpickle
        self.closures = ZmqCarClosuresStateWrapper()