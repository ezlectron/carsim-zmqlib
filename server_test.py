import logging
import time

from zmqlib import ZeroMqServerController, ZmqCarControlRequestMessage, ZmqCarStateResponseMessage

logging.basicConfig(filename='/tmp/zmqlib-server-test.log', level=logging.INFO)

def callback_func(msg : ZmqCarControlRequestMessage):
    print (msg)

if __name__ == "__main__":
    resp = ZmqCarStateResponseMessage(ZmqCarStateResponseMessage.MSG_STATUS_CODE_OK)
    controller = ZeroMqServerController("tcp://127.0.0.1:5555")

    controller.registerActionMessageCallBack(callback_func)

    while True:
        resp.door_driver.setDoorState(True)
        controller.updateStateSyncResponse(resp)

        time.sleep(5)

        resp.door_driver.setDoorState(False)
        controller.updateStateSyncResponse(resp)

        if controller.getStateSyncRequest() is not None:
            print (controller.getStateSyncRequest().door_driver.isOpenDoorAction())

        time.sleep(5)