from .request import ZmqRequestMessage

#
# Implements all actions that can be performed on a car door
class ZmqDoorActions():

    def __init__(self):
        self.open_door = False
        self.close_door = False

        self.keylock_lock = False
        self.keylock_unlock = False

        self.window_close = False
        self.window_close_auto = False
        self.window_open = False
        self.window_open_auto = False

        # Only used by driver door
        self.central_lock_button = False
        self.central_unlock_button = False

    def doOpenDoor(self):
        self.open_door = True
        self.close_door = False

    def doCloseDoor(self):
        self.open_door = False
        self.close_door = True

    def doResetDoorStateAction(self):
        self.open_door = False
        self.close_door = False

    def doKeyLockLock(self):
        self.keylock_lock = True
        self.keylock_unlock = False

    def doKeyLockUnLock(self):
        self.keylock_lock = False
        self.keylock_unlock = True

    def doResetLockAction(self):
        self.keylock_lock = False
        self.keylock_unlock = False


    # Window actions
    def doCloseWindow(self):
        self.window_close = True
        self.window_close_auto = False
        self.window_open = False
        self.window_open_auto = False

    def doCloseWindowAuto(self):
        self.window_close = False
        self.window_close_auto = True
        self.window_open = False
        self.window_open_auto = False

    def doOpenWindow(self):
        self.window_close = False
        self.window_close_auto = False
        self.window_open = True
        self.window_open_auto = False

    def doOpenWindowAuto(self):
        self.window_close = False
        self.window_close_auto = False
        self.window_open = False
        self.window_open_auto = True

    def doResetWindowAction(self):
        self.window_close = False
        self.window_close_auto = False
        self.window_open = False
        self.window_open_auto = False

    # Actions only performed when it is the driver door
    def doCentralLockButtonActionPress(self):
        self.central_lock_button = True

        # Because the two buttons should never be pressed at the same time
        self.central_unlock_button = False

    def doCentralLockButtonActionRelease(self):
        self.central_lock_button = False

    def doCentralUnlockButtonActionPress(self):
        self.central_unlock_button = True

        # Because the two buttons should never be pressed at the same time
        self.central_lock_button = False

    def doCentralUnlockButtonActionRelease(self):
        self.central_unlock_button = False


    # General statuses
    def isOpenDoorAction(self):
        return self.open_door

    def isCloseDoorAction(self):
        return self.close_door

    def isKeyLockLockAction(self):
        return self.keylock_lock

    def isKeyLockUnLockAction(self):
        return self.keylock_unlock

    def isKeyLockNeutralAction(self):
        return self.keylock_lock and self.keylock_unlock


    # Window statuses
    def isWindowCloseAction(self):
        return self.window_close

    def isWindowAutoCloseAction(self):
        return self.window_close_auto

    def isWindowOpenAction(self):
        return self.window_open

    def isWindowAutoOpenAction(self):
        return self.window_open_auto


    # Door controller statuses
    def isCentralDoorLockAction(self):
        return self.central_lock_button

    def isCentralDoorUnlockAction(self):
        return self.central_unlock_button

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