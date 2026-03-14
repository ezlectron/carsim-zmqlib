import logging

from zmqlib import ZeroMqClientController, EngineSimZeroMqRequestMessage

logging.basicConfig(filename='/tmp/zmqlib-client-test.log', level=logging.INFO)

if __name__ == "__main__":
    controller = ZeroMqClientController("tcp://127.0.0.1:5555")

    send_msg = EngineSimZeroMqRequestMessage(EngineSimZeroMqRequestMessage.MSG_STATUS_CODE_OK)

    controller.sendMessage(send_msg)