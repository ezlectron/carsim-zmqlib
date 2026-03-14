import jsonpickle
import logging
import threading
import time
import zmq

from zmqlib.msg import EngineSimZeroMqRequestMessage, EngineSimZeroMqResponseMessage

logger = logging.getLogger("zmqctrl")

class ZeroMqServerController(object):

    _instance = None
    _running = False

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)

        return cls._instance

    def __init__(self, bind_spec):
        self._context = zmq.Context()
        self._socket = self._context.socket(zmq.REP)
        self._socket.bind(bind_spec)

        logging.info("ZMQ Controller is now listening on {}".format(bind_spec))

        self._msg_received = None

        self._running = True
        self._zmq_listener = threading.Thread(target=self._listener_thread)
        self._zmq_listener.start()

    def _listener_thread(self):
        while self._running:
            req_msg_json = self._socket.recv_json()
            req_msg_object = jsonpickle.decode(req_msg_json)

            print("Received request: %s" % req_msg_object)
            print ("ZMQ Message: Type {}, Status {}".format(req_msg_object.getMessageType(), req_msg_object.getStatusCode()))

            resp_msg_object = EngineSimZeroMqResponseMessage(EngineSimZeroMqResponseMessage.MSG_STATUS_CODE_OK)

            resp_msg_json = jsonpickle.encode(resp_msg_object)
            self._socket.send_json(resp_msg_json)
