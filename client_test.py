import logging
import time

from zmqlib import ZeroMqClientController, ZmqCarControlRequestMessage

logging.basicConfig(filename='/tmp/zmqlib-client-test.log', level=logging.INFO)

if __name__ == "__main__":
    controller = ZeroMqClientController("tcp://127.0.0.1:5555")

    send_msg = ZmqCarControlRequestMessage(ZmqCarControlRequestMessage.MSG_STATUS_CODE_OK)

    controller.updateStateSyncMessage(send_msg)

    while True:
        send_msg.closures.door_driver.doOpenDoor()

        state_msg = controller.getStateSyncResponse()
        if state_msg:
            print (controller.getStateSyncResponseJson())

        time.sleep(1)

        send_msg.closures.door_driver.doCloseDoor()

        time.sleep(1)