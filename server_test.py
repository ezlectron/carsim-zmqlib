import logging
import time

from zmqlib import ZeroMqServerController, EngineSimZeroMqCarStateResponseMessage

logging.basicConfig(filename='/tmp/zmqlib-server-test.log', level=logging.INFO)

if __name__ == "__main__":
    resp = EngineSimZeroMqCarStateResponseMessage(EngineSimZeroMqCarStateResponseMessage.MSG_STATUS_CODE_OK)
    controller = ZeroMqServerController("tcp://127.0.0.1:5555")

    while True:
        resp.door_driver.setDoorState(True)
        controller.updateStateSyncResponse(resp)

        time.sleep(5)

        resp.door_driver.setDoorState(False)
        controller.updateStateSyncResponse(resp)

        time.sleep(5)