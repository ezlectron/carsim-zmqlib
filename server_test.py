import logging

from zmqlib import ZeroMqServerController

logging.basicConfig(filename='/tmp/zmqlib-server-test.log', level=logging.INFO)

if __name__ == "__main__":
    controller = ZeroMqServerController("tcp://127.0.0.1:5555")