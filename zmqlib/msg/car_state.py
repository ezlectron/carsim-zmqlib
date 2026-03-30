from .response import ZmqResponseMessage

#
# Represents the state of a car door and its features (locks, windows, etc.)
class ZmqDoorState():

    DOOR_DRIVER     = "Driver door"
    DOOR_PASSENGER  = "Passenger door"

    def __init__(self, name, position):
        self.name = name
        self.position = position
        self.is_door_open = False
        self.is_lock_locked = False

        # Only defined when driver door
        if self.name == self.DOOR_DRIVER:
            self.central_door_lock_active = False

    def setDoorState(self, state):
        self.is_door_open = state

    def setLockState(self, state):
        self.is_lock_locked = state

    def getDoorIsOpen(self):
        return self.is_door_open

    def getLockIsLocked(self):
        return self.is_lock_locked

    # Driver door st ates

    def setCentralDoorLockState(self, state):
        self.central_door_lock_active = state

    def getCentralDoorLockState(self):
        return self.central_door_lock_active

#
# Wrapper for the doors, trunk, tank flap and bonnet
class ZmqCarClosuresStateWrapper():
    def __init__(self):
        self.doors = ZmqCarDoorsStateWrapper()

#
# Wrapper for the doors
class ZmqCarDoorsStateWrapper():

    DOOR_DRIVER     = "Driver door"
    DOOR_PASSENGER  = "Passenger door"

    def __init__(self):
        self.door_driver = ZmqDoorState(self.DOOR_DRIVER, "Front Left")
        self.door_passenger = ZmqDoorState(self.DOOR_PASSENGER, "Front Right")

#
# Main car state response message
class ZmqCarStateResponseMessage(ZmqResponseMessage):

    def __init__(self, status):
        super().__init__(status)

        #NOTE: Sub objects must be defined in the __init__()
        #  for them to be decoded by jsonpickle
        self.closures = ZmqCarClosuresStateWrapper()