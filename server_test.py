import logging
import time

from zmqlib import ZeroMqServerController, ZmqCarControlRequestMessage, ZmqCarStateResponseMessage

logging.basicConfig(filename='/tmp/zmqlib-server-test.log', level=logging.INFO)

def callback_func(msg : ZmqCarControlRequestMessage):
    #print (msg)
    pass

if __name__ == "__main__":
    resp = ZmqCarStateResponseMessage(ZmqCarStateResponseMessage.MSG_STATUS_CODE_OK)
    controller = ZeroMqServerController("tcp://127.0.0.1:5555")

    controller.registerActionMessageCallBack(callback_func)

    while True:
        resp.closures.doors.door_driver.setDoorState(True)
        resp.closures.doors.door_driver.setWindowPosition(75)
        resp.closures.doors.door_passenger.setWindowPosition(100)
        controller.updateStateSyncResponse(resp)

        time.sleep(5)

        resp.closures.doors.door_driver.setDoorState(False)
        resp.closures.doors.door_driver.setWindowPosition(15)
        resp.closures.doors.door_passenger.setWindowPosition(45)
        controller.updateStateSyncResponse(resp)

        if controller.getStateSyncRequest() is not None:
            #print ("Door open action:")
            #print (controller.getStateSyncRequest().closures.doors.door_driver.isOpenDoorAction())

            #print ("Central lock action")
            #print (controller.getStateSyncRequest().closures.doors.door_driver.isCentralDoorLockAction())

            print ("Window Action")
            print (controller.getStateSyncRequest().closures.doors.door_driver.isWindowOpenAction())

        time.sleep(5)